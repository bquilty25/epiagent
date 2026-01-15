"""Package router for matching user queries to relevant Epiverse packages.

This module provides "Epiverse-first" routing: given a user query about
epidemiological analysis, it finds the most relevant Epiverse packages
before the agent attempts to write custom code.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from .registry import EpiversePackage, EpiverseRegistry, get_registry

__all__ = ["find_relevant_packages", "PackageMatch", "TASK_KEYWORDS"]

# Map common epidemiological tasks to relevant keywords/topics
TASK_KEYWORDS: Dict[str, List[str]] = {
    # Data handling
    "linelist": ["linelist", "case-data", "data-structures", "structured-data"],
    "data cleaning": ["data-cleaning", "cleanepi", "data-validation", "standardize"],
    "data import": ["data-import", "readepi", "health-information-systems"],
    
    # Epidemiological parameters
    "incubation period": ["epiparameter", "probability-distribution", "epidemiological", "delay"],
    "serial interval": ["epiparameter", "probability-distribution", "delay", "transmission"],
    "generation time": ["epiparameter", "generation", "transmission", "delay"],
    "delay distribution": ["epiparameter", "probability-distribution", "delay"],
    
    # Transmission metrics
    "reproduction number": ["reproduction-number", "transmission", "rt", "r0"],
    "Rt": ["reproduction-number", "transmission", "real-time-analysis"],
    "R0": ["reproduction-number", "transmission", "epidemic-modelling"],
    "superspreading": ["superspreading", "transmission", "individual-level"],
    "transmission chains": ["transmission-chain", "epichains", "branching-processes"],
    
    # Severity & outcomes
    "CFR": ["case-fatality-rate", "cfr", "severity", "health-outcomes"],
    "case fatality": ["case-fatality-rate", "cfr", "severity", "under-reporting"],
    "severity": ["severity", "cfr", "case-fatality-rate", "health-outcomes"],
    "IFR": ["infection-fatality", "severity", "under-reporting"],
    
    # Incidence & epidemic curves
    "incidence": ["incidence", "incidence2", "epidemic-curves", "time-series"],
    "epidemic curve": ["incidence", "epidemic-curves", "time-series", "visualization"],
    
    # Modelling
    "epidemic model": ["epidemic-modelling", "epidemic-simulations", "compartmental"],
    "SIR model": ["epidemic-modelling", "compartmental", "sir", "infectious-disease-dynamics"],
    "scenario": ["scenario-analysis", "scenario-modelling", "epidemic-simulations"],
    "final size": ["finalsize", "epidemic-modelling", "sir"],
    "forecast": ["forecasting", "real-time-analysis", "prediction"],
    
    # Vaccination & interventions
    "vaccine": ["vaccination", "vaccine-effectiveness", "non-pharmaceutical-interventions"],
    "vaccine effectiveness": ["vaccine-effectiveness", "vaccineff"],
    "NPI": ["non-pharmaceutical-interventions", "interventions"],
    
    # Serological
    "seroprevalence": ["serological-surveys", "serofoi", "antibodies"],
    "force of infection": ["serofoi", "force-of-infection", "foi"],
    
    # Contact data
    "contact matrix": ["contact-matrices", "contact-matrix", "social-contacts"],
    "contact data": ["contact-matrices", "social-contacts"],
    
    # Simulation
    "simulate": ["epidemic-simulations", "outbreak-simulator", "simulist"],
    "simulation": ["epidemic-simulations", "outbreak-simulator", "simulist"],
}


@dataclass
class PackageMatch:
    """Result of matching a query to an Epiverse package."""
    
    package: EpiversePackage
    score: float
    matched_keywords: List[str]
    
    def to_dict(self) -> Dict:
        return {
            "name": self.package.name,
            "summary": self.package.summary,
            "score": round(self.score, 2),
            "matched_keywords": self.matched_keywords,
            "homepage": self.package.homepage,
            "topics": self.package.topics,
        }


def _normalize(text: str) -> str:
    """Normalize text for matching."""
    return re.sub(r"[^a-z0-9\s]", "", text.lower())


def _compute_match_score(
    query: str,
    package: EpiversePackage,
    task_keywords: Dict[str, List[str]],
) -> Tuple[float, List[str]]:
    """Compute relevance score between a query and a package.
    
    Scoring:
    - Direct name match: +3.0
    - Summary contains query terms: +2.0 per term
    - Topic overlap with task keywords: +1.5 per topic
    - Summary keyword overlap: +0.5 per keyword
    """
    score = 0.0
    matched: List[str] = []
    
    query_normalized = _normalize(query)
    query_terms = query_normalized.split()
    
    name_normalized = _normalize(package.name)
    summary_normalized = _normalize(package.summary)
    topics_normalized = [_normalize(t) for t in package.topics]
    
    # Direct name match
    if query_normalized in name_normalized or name_normalized in query_normalized:
        score += 3.0
        matched.append(f"name:{package.name}")
    
    # Query terms in summary
    for term in query_terms:
        if len(term) > 2 and term in summary_normalized:
            score += 2.0
            matched.append(f"summary:{term}")
    
    # Find relevant task keywords
    relevant_keywords: set = set()
    for task, keywords in task_keywords.items():
        task_normalized = _normalize(task)
        if any(t in query_normalized for t in task_normalized.split()):
            relevant_keywords.update(keywords)
    
    # Match topics against task keywords
    for topic in package.topics:
        topic_normalized = _normalize(topic)
        if topic_normalized in relevant_keywords or topic in relevant_keywords:
            score += 1.5
            matched.append(f"topic:{topic}")
        # Also check if query terms appear in topics
        for term in query_terms:
            if len(term) > 2 and term in topic_normalized:
                score += 1.0
                if f"topic:{topic}" not in matched:
                    matched.append(f"topic:{topic}")
    
    # Keywords in summary
    for keyword in relevant_keywords:
        if keyword in summary_normalized:
            score += 0.5
            matched.append(f"keyword:{keyword}")
    
    return score, matched


def find_relevant_packages(
    query: str,
    *,
    top_k: int = 5,
    min_score: float = 1.0,
    category_filter: Optional[str] = None,
    registry: Optional[EpiverseRegistry] = None,
) -> List[PackageMatch]:
    """Find Epiverse packages relevant to a user query.
    
    Args:
        query: Natural language description of the epidemiological task
        top_k: Maximum number of packages to return
        min_score: Minimum relevance score to include
        category_filter: Optional filter by category (e.g., "r_package")
        registry: Registry to search (uses default if not provided)
    
    Returns:
        List of PackageMatch objects, sorted by relevance score
    
    Example:
        >>> matches = find_relevant_packages("estimate CFR for COVID-19")
        >>> for m in matches:
        ...     print(f"{m.package.name}: {m.score}")
        cfr: 6.5
        epiparameter: 3.0
        ...
    """
    if registry is None:
        registry = get_registry()
    
    matches: List[PackageMatch] = []
    
    for package in registry.sorted_packages:
        # Apply category filter
        if category_filter and package.category != category_filter:
            continue
        
        # Skip infrastructure/docs packages for analysis queries
        if package.category in ("infrastructure", "documentation", "repository"):
            continue
        
        score, matched_keywords = _compute_match_score(query, package, TASK_KEYWORDS)
        
        if score >= min_score:
            matches.append(PackageMatch(
                package=package,
                score=score,
                matched_keywords=matched_keywords,
            ))
    
    # Sort by score descending
    matches.sort(key=lambda m: m.score, reverse=True)
    
    return matches[:top_k]
