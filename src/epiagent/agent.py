"""Lightweight agent orchestration utilities for Epiverse Trace tooling."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Sequence

import math
import re

from .tools.registry import EpiverseRegistry, get_registry

__all__ = [
    "ShortlistedPackage",
    "PlannedToolCall",
    "EpiAgent",
    "plan_epiverse_goal",
]


TOKEN_PATTERN = re.compile(r"[A-Za-z0-9_]+")


def _tokenise(text: str) -> List[str]:
    return [token.lower() for token in TOKEN_PATTERN.findall(text or "")]


def _score_overlap(goal_tokens: Sequence[str], candidate_tokens: Sequence[str]) -> float:
    if not goal_tokens or not candidate_tokens:
        return 0.0
    goal_counts: Dict[str, int] = {}
    for token in goal_tokens:
        goal_counts[token] = goal_counts.get(token, 0) + 1
    overlap = 0
    for token in candidate_tokens:
        if token in goal_counts and goal_counts[token] > 0:
            overlap += 1
            goal_counts[token] -= 1
    return overlap / math.sqrt(len(goal_tokens) * len(candidate_tokens))


@dataclass
class ShortlistedPackage:
    """Represents a ranked package suggestion for a particular task."""

    name: str
    score: float
    reason: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PlannedToolCall:
    """A single tool invocation suggested by :class:`EpiAgent`."""

    package: str
    function: str
    description: str
    args: Sequence[Any] = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)


@dataclass
class _PlanRule:
    keywords: Sequence[str]
    package: str
    function: str
    description: str


DEFAULT_PLAN_RULES: Sequence[_PlanRule] = (
    _PlanRule(
        keywords=("incidence", "case", "count"),
        package="incidence2",
        function="incidence",
        description="Compute incidence curves from linelist data.",
    ),
    _PlanRule(
        keywords=("reproduction", "rt", "estimate"),
        package="EpiEstim",
        function="estimate_R",
        description="Estimate time-varying reproduction numbers.",
    ),
    _PlanRule(
        keywords=("clean", "linelist", "standardise"),
        package="linelist",
        function="clean_variable_names",
        description="Standardise column names in linelist style datasets.",
    ),
    _PlanRule(
        keywords=("contact", "network", "epicontacts"),
        package="epicontacts",
        function="make_epicontacts",
        description="Build an epicontacts object from contact tracing data.",
    ),
)


class EpiAgent:
    """Minimal reasoning-and-act loop for Epiverse Trace tooling."""

    def __init__(
        self,
        *,
        registry: Optional[EpiverseRegistry] = None,
        planning_rules: Sequence[_PlanRule] = DEFAULT_PLAN_RULES,
    ) -> None:
        self.registry = registry or get_registry()
        self._planning_rules = planning_rules

    def shortlist_packages(self, goal: str, *, top_k: int = 5) -> List[ShortlistedPackage]:
        goal_tokens = _tokenise(goal)
        ranked: List[ShortlistedPackage] = []
        for package in self.registry.sorted_packages:
            metadata_tokens = _tokenise(" ".join(
                filter(
                    None,
                    [
                        package.name,
                        package.summary,
                        package.category,
                        " ".join(package.topics),
                    ],
                )
            ))
            score = _score_overlap(goal_tokens, metadata_tokens)
            if score <= 0:
                continue
            matched = sorted(set(goal_tokens).intersection(metadata_tokens))
            reason = (
                f"Matched keywords {', '.join(matched)} against package metadata." if matched else "Related metadata match."
            )
            ranked.append(
                ShortlistedPackage(
                    name=package.name,
                    score=score,
                    reason=reason,
                    metadata=package.to_dict(),
                )
            )
        ranked.sort(key=lambda item: item.score, reverse=True)
        return ranked[:top_k]

    def plan(self, goal: str) -> List[PlannedToolCall]:
        """Propose a sequence of tool invocations for a goal."""

        goal_tokens = set(_tokenise(goal))
        plan: List[PlannedToolCall] = []
        for rule in self._planning_rules:
            if goal_tokens.intersection(rule.keywords):
                plan.append(
                    PlannedToolCall(
                        package=rule.package,
                        function=rule.function,
                        description=rule.description,
                    )
                )
        return plan

    def execute(self, plan: Iterable[PlannedToolCall]) -> List[Dict[str, Any]]:
        """Execute a plan sequentially using the dynamic wrappers."""

        results: List[Dict[str, Any]] = []
        try:
            from .tools import r_wrappers
        except ImportError as err:
            raise RuntimeError(
                "Epiverse R tooling is unavailable. Ensure rpy2 and R are installed before executing plans."
            ) from err

        for step in plan:
            tool_result = r_wrappers.call_epiverse_function(
                package=step.package,
                function=step.function,
                args=step.args,
                kwargs=step.kwargs,
            )
            results.append(
                {
                    "package": step.package,
                    "function": step.function,
                    "description": step.description,
                    "status": tool_result.status,
                    "message": tool_result.message,
                    "data": tool_result.data,
                }
            )
        return results

    def run(self, goal: str) -> Dict[str, Any]:
        """Convenience helper that shortlists packages, plans, and executes."""

        shortlist = self.shortlist_packages(goal)
        plan = self.plan(goal)
        execution = self.execute(plan) if plan else []
        return {
            "goal": goal,
            "shortlist": [package.__dict__ for package in shortlist],
            "plan": [
                {
                    "package": step.package,
                    "function": step.function,
                    "description": step.description,
                }
                for step in plan
            ],
            "execution": execution,
        }


def plan_epiverse_goal(goal: str, *, top_k: int = 5) -> Dict[str, Any]:
    """Convenience helper to obtain a shortlist and plan without execution."""

    agent = EpiAgent()
    shortlist = agent.shortlist_packages(goal, top_k=top_k)
    plan = agent.plan(goal)
    return {
        "goal": goal,
        "shortlist": [package.__dict__ for package in shortlist],
        "plan": [
            {
                "package": step.package,
                "function": step.function,
                "description": step.description,
            }
            for step in plan
        ],
    }
