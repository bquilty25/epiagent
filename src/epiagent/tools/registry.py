"""Utility helpers for discovering Epiverse Trace packages."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional
import urllib.request

__all__ = ["EpiverseRegistry", "get_registry", "EpiversePackage"]

ORG = "epiverse-trace"
DEFAULT_REGISTRY_PATH = Path(__file__).resolve().parents[2] / "docs" / "epiverse_packages.json"


@dataclass
class EpiversePackage:
    """Represents a single Epiverse Trace repository with optional metadata."""

    name: str
    summary: str = ""
    category: str = "unknown"
    homepage: Optional[str] = None
    topics: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, object]:
        payload: Dict[str, object] = {
            "name": self.name,
            "category": self.category,
        }
        if self.summary:
            payload["summary"] = self.summary
        if self.homepage:
            payload["homepage"] = self.homepage
        if self.topics:
            payload["topics"] = sorted(set(self.topics))
        return payload

    def merge(self, *, summary: Optional[str] = None, topics: Optional[Iterable[str]] = None, homepage: Optional[str] = None) -> "EpiversePackage":
        if summary and not self.summary:
            self.summary = summary.strip()
        if topics:
            merged = set(self.topics)
            merged.update(topic for topic in topics if topic)
            self.topics = sorted(merged)
        if homepage and not self.homepage:
            self.homepage = homepage
        return self


@dataclass
class EpiverseRegistry:
    """In-memory catalogue of Epiverse Trace repositories."""

    packages: Dict[str, EpiversePackage] = field(default_factory=dict)
    source: Optional[Path] = None

    @classmethod
    def load(cls, path: Path = DEFAULT_REGISTRY_PATH) -> "EpiverseRegistry":
        packages: Dict[str, EpiversePackage] = {}
        if path.exists():
            raw = json.loads(path.read_text(encoding="utf-8"))
            for entry in raw:
                if isinstance(entry, str):
                    package = EpiversePackage(name=entry)
                else:
                    package = EpiversePackage(
                        name=entry.get("name"),
                        summary=entry.get("summary", ""),
                        category=entry.get("category", "unknown"),
                        homepage=entry.get("homepage"),
                        topics=list(entry.get("topics", [])),
                    )
                packages[package.name] = package
        return cls(packages=packages, source=path)

    def save(self, path: Optional[Path] = None) -> None:
        target = path or self.source
        if target is None:
            raise ValueError("No target path supplied for saving the registry")
        serialised = [pkg.to_dict() for pkg in self.sorted_packages]
        target.write_text(json.dumps(serialised, indent=2) + "\n", encoding="utf-8")

    def refresh_from_github(self, *, per_page: int = 100) -> List[EpiversePackage]:
        """Refresh the package list using the GitHub API."""

        url = f"https://api.github.com/orgs/{ORG}/repos?per_page={per_page}"
        repos = self._fetch_repo_page(url)
        next_url = repos.next_url
        all_repos = list(repos.items)
        while next_url:
            repos = self._fetch_repo_page(next_url)
            all_repos.extend(repos.items)
            next_url = repos.next_url
        refreshed: Dict[str, EpiversePackage] = {}
        for repo in all_repos:
            if repo.get("archived"):
                continue
            name = repo["name"]
            package = self.packages.get(name, EpiversePackage(name=name))
            package.category = package.category or "unknown"
            package.merge(
                summary=repo.get("description"),
                topics=repo.get("topics"),
                homepage=repo.get("html_url"),
            )
            refreshed[name] = package
        self.packages = refreshed
        if self.source:
            self.save(self.source)
        return self.sorted_packages

    @property
    def sorted_packages(self) -> List[EpiversePackage]:
        return [self.packages[key] for key in sorted(self.packages)]

    def _fetch_repo_page(self, url: str) -> "_RepoPage":
        request = urllib.request.Request(
            url,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "epiagent-registry",
            },
        )
        with urllib.request.urlopen(request) as response:  # nosec - controlled URL
            items = json.load(response)
            next_url: Optional[str] = None
            link_header = response.headers.get("Link")
            if link_header and "rel=\"next\"" in link_header:
                for part in link_header.split(","):
                    if "rel=\"next\"" in part:
                        next_url = part[part.find("<") + 1 : part.find(">")]  # noqa: E203
                        break
        return _RepoPage(items=items, next_url=next_url)

    def has_package(self, name: str) -> bool:
        return name in self.packages

    def ensure_packages(self, packages: Iterable[str]) -> List[str]:
        """Return the subset of *packages* that exist in the registry."""

        return sorted(set(packages).intersection(self.packages))

    def describe(self, name: str) -> Optional[Dict[str, object]]:
        package = self.packages.get(name)
        return package.to_dict() if package else None


@dataclass
class _RepoPage:
    items: List[dict]
    next_url: Optional[str]


_registry: Optional[EpiverseRegistry] = None


def get_registry() -> EpiverseRegistry:
    global _registry
    if _registry is None:
        _registry = EpiverseRegistry.load()
    return _registry
