"""Top-level package for the epiagent project."""

from importlib import import_module

from .agent import EpiAgent, PlannedToolCall, ShortlistedPackage, plan_epiverse_goal

__all__ = [
    "EpiAgent",
    "PlannedToolCall",
    "ShortlistedPackage",
    "plan_epiverse_goal",
    "ToolResult",
    "call_epiverse_function",
    "list_epiverse_packages",
]


def __getattr__(name):  # pragma: no cover - trivial delegator
    if name in {"ToolResult", "call_epiverse_function", "list_epiverse_packages"}:
        module = import_module("epiagent.tools.r_wrappers")
        return getattr(module, name)
    raise AttributeError(f"module 'epiagent' has no attribute '{name}'")
