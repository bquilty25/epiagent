"""Top-level package for the epiagent project."""

from .tools.r_wrappers import (
    ToolResult,
    call_epiverse_function,
    list_epiverse_packages,
)
from .tools.gitingest_wrapper import (
    GitIngestResult,
    ingest_repository,
    ingest_repository_async,
    batch_ingest_repositories,
    batch_ingest_repositories_async,
)
from .tools.router import (
    find_relevant_packages,
    PackageMatch,
)

__all__ = [
    "__version__",
    "ToolResult",
    "call_epiverse_function",
    "list_epiverse_packages",
    "GitIngestResult",
    "ingest_repository",
    "ingest_repository_async",
    "batch_ingest_repositories",
    "batch_ingest_repositories_async",
    "find_relevant_packages",
    "PackageMatch",
]

__version__ = "0.1.0"

