"""GitIngest wrapper for AI agent codebase analysis."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Union

try:  # pragma: no cover - optional dependency
    from gitingest import ingest, ingest_async
except ImportError as exc:  # pragma: no cover - optional dependency
    raise ImportError(
        "gitingest is required to use the GitIngest wrapper. Install it via pip."
    ) from exc

from .r_wrappers import ToolResult


@dataclass
class GitIngestResult:
    """Structured response from GitIngest analysis."""
    
    summary: str
    tree: str
    content: str
    repository_url: str
    files_analyzed: int
    estimated_tokens: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "summary": self.summary,
            "tree": self.tree,
            "content": self.content,
            "repository_url": self.repository_url,
            "files_analyzed": self.files_analyzed,
            "estimated_tokens": self.estimated_tokens,
        }
    
    def get_full_context(self) -> str:
        """Get the complete formatted context for AI processing."""
        return f"{self.summary}\n\n{self.tree}\n\n{self.content}"


def ingest_repository(
    repository_url: str,
    *,
    include_patterns: Optional[Sequence[str]] = None,
    exclude_patterns: Optional[Sequence[str]] = None,
    max_file_size: Optional[int] = None,
    branch: Optional[str] = None,
    token: Optional[str] = None,
    output_path: Optional[Union[str, Path]] = None,
) -> ToolResult:
    """
    Ingest a Git repository for AI analysis.
    
    Args:
        repository_url: URL of the Git repository to analyze
        include_patterns: Unix shell-style patterns for files to include
        exclude_patterns: Unix shell-style patterns for files to exclude
        max_file_size: Maximum file size in bytes to process
        branch: Specific branch to analyze (defaults to repository's default)
        token: GitHub personal access token for private repositories
        output_path: Path to save the digest (if None, returns structured data)
    
    Returns:
        ToolResult containing the GitIngest analysis or error information
    """
    try:
        # Prepare parameters for gitingest
        kwargs = {}
        if include_patterns:
            kwargs["include_patterns"] = list(include_patterns)
        if exclude_patterns:
            kwargs["exclude_patterns"] = list(exclude_patterns)
        if max_file_size:
            kwargs["max_file_size"] = max_file_size
        if branch:
            kwargs["branch"] = branch
        if token:
            kwargs["token"] = token
        
        # Call gitingest
        summary, tree, content = ingest(repository_url, **kwargs)
        
        # Parse summary to extract metadata
        files_analyzed = 0
        estimated_tokens = 0
        
        for line in summary.split('\n'):
            if line.startswith('Files analyzed:'):
                try:
                    files_analyzed = int(line.split(':')[1].strip())
                except (ValueError, IndexError):
                    pass
            elif line.startswith('Estimated tokens:'):
                try:
                    val = line.split(':')[1].strip()
                    if 'k' in val:
                        estimated_tokens = int(float(val.replace('k', '')) * 1000)
                    else:
                        estimated_tokens = int(val)
                except (ValueError, IndexError):
                    pass
        
        # Create structured result
        result = GitIngestResult(
            summary=summary,
            tree=tree,
            content=content,
            repository_url=repository_url,
            files_analyzed=files_analyzed,
            estimated_tokens=estimated_tokens,
        )
        
        # Save to file if output_path is specified
        if output_path:
            output_path = Path(output_path)
            output_path.write_text(result.get_full_context(), encoding='utf-8')
            return ToolResult(
                status="success",
                data=result.to_dict(),
                message=f"Repository analysis saved to {output_path}",
                artifact_path=output_path,
            )
        
        return ToolResult(
            status="success",
            data=result.to_dict(),
        )
        
    except Exception as err:
        return ToolResult(
            status="error",
            message=f"Failed to ingest repository '{repository_url}': {err}",
        )


async def ingest_repository_async(
    repository_url: str,
    *,
    include_patterns: Optional[Sequence[str]] = None,
    exclude_patterns: Optional[Sequence[str]] = None,
    max_file_size: Optional[int] = None,
    branch: Optional[str] = None,
    token: Optional[str] = None,
    output_path: Optional[Union[str, Path]] = None,
) -> ToolResult:
    """
    Asynchronously ingest a Git repository for AI analysis.
    
    This is recommended for batch processing or when integrating with async AI services.
    
    Args:
        repository_url: URL of the Git repository to analyze
        include_patterns: Unix shell-style patterns for files to include
        exclude_patterns: Unix shell-style patterns for files to exclude
        max_file_size: Maximum file size in bytes to process
        branch: Specific branch to analyze (defaults to repository's default)
        token: GitHub personal access token for private repositories
        output_path: Path to save the digest (if None, returns structured data)
    
    Returns:
        ToolResult containing the GitIngest analysis or error information
    """
    try:
        # Prepare parameters for gitingest
        kwargs = {}
        if include_patterns:
            kwargs["include_patterns"] = list(include_patterns)
        if exclude_patterns:
            kwargs["exclude_patterns"] = list(exclude_patterns)
        if max_file_size:
            kwargs["max_file_size"] = max_file_size
        if branch:
            kwargs["branch"] = branch
        if token:
            kwargs["token"] = token
        
        # Call gitingest asynchronously
        summary, tree, content = await ingest_async(repository_url, **kwargs)
        
        # Parse summary to extract metadata
        files_analyzed = 0
        estimated_tokens = 0
        
        for line in summary.split('\n'):
            if line.startswith('Files analyzed:'):
                try:
                    files_analyzed = int(line.split(':')[1].strip())
                except (ValueError, IndexError):
                    pass
            elif line.startswith('Estimated tokens:'):
                try:
                    val = line.split(':')[1].strip()
                    if 'k' in val:
                        estimated_tokens = int(float(val.replace('k', '')) * 1000)
                    else:
                        estimated_tokens = int(val)
                except (ValueError, IndexError):
                    pass
        
        # Create structured result
        result = GitIngestResult(
            summary=summary,
            tree=tree,
            content=content,
            repository_url=repository_url,
            files_analyzed=files_analyzed,
            estimated_tokens=estimated_tokens,
        )
        
        # Save to file if output_path is specified
        if output_path:
            output_path = Path(output_path)
            output_path.write_text(result.get_full_context(), encoding='utf-8')
            return ToolResult(
                status="success",
                data=result.to_dict(),
                message=f"Repository analysis saved to {output_path}",
                artifact_path=output_path,
            )
        
        return ToolResult(
            status="success",
            data=result.to_dict(),
        )
        
    except Exception as err:
        return ToolResult(
            status="error",
            message=f"Failed to ingest repository '{repository_url}': {err}",
        )


def batch_ingest_repositories(
    repository_urls: Sequence[str],
    *,
    include_patterns: Optional[Sequence[str]] = None,
    exclude_patterns: Optional[Sequence[str]] = None,
    max_file_size: Optional[int] = None,
    branch: Optional[str] = None,
    token: Optional[str] = None,
    output_dir: Optional[Union[str, Path]] = None,
) -> ToolResult:
    """
    Ingest multiple repositories in batch.
    
    Args:
        repository_urls: List of repository URLs to analyze
        include_patterns: Unix shell-style patterns for files to include
        exclude_patterns: Unix shell-style patterns for files to exclude
        max_file_size: Maximum file size in bytes to process
        branch: Specific branch to analyze (defaults to repository's default)
        token: GitHub personal access token for private repositories
        output_dir: Directory to save individual digest files
    
    Returns:
        ToolResult containing batch analysis results
    """
    results = []
    errors = []
    
    for repo_url in repository_urls:
        output_path = None
        if output_dir:
            # Create safe filename from URL
            safe_name = repo_url.replace('https://github.com/', '').replace('/', '_')
            output_path = Path(output_dir) / f"{safe_name}_digest.txt"
        
        result = ingest_repository(
            repo_url,
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns,
            max_file_size=max_file_size,
            branch=branch,
            token=token,
            output_path=output_path,
        )
        
        if result.status == "success":
            results.append(result.data)
        else:
            errors.append({"repository": repo_url, "error": result.message})
    
    return ToolResult(
        status="success" if not errors else "partial",
        data={
            "successful_ingests": results,
            "errors": errors,
            "total_repositories": len(repository_urls),
            "successful_count": len(results),
            "error_count": len(errors),
        },
        message=f"Processed {len(repository_urls)} repositories: {len(results)} successful, {len(errors)} errors",
    )


async def batch_ingest_repositories_async(
    repository_urls: Sequence[str],
    *,
    include_patterns: Optional[Sequence[str]] = None,
    exclude_patterns: Optional[Sequence[str]] = None,
    max_file_size: Optional[int] = None,
    branch: Optional[str] = None,
    token: Optional[str] = None,
    output_dir: Optional[Union[str, Path]] = None,
    max_concurrent: int = 5,
) -> ToolResult:
    """
    Asynchronously ingest multiple repositories in batch with concurrency control.
    
    Args:
        repository_urls: List of repository URLs to analyze
        include_patterns: Unix shell-style patterns for files to include
        exclude_patterns: Unix shell-style patterns for files to exclude
        max_file_size: Maximum file size in bytes to process
        branch: Specific branch to analyze (defaults to repository's default)
        token: GitHub personal access token for private repositories
        output_dir: Directory to save individual digest files
        max_concurrent: Maximum number of concurrent ingestions
    
    Returns:
        ToolResult containing batch analysis results
    """
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def ingest_single(repo_url: str) -> tuple[str, ToolResult]:
        async with semaphore:
            output_path = None
            if output_dir:
                # Create safe filename from URL
                safe_name = repo_url.replace('https://github.com/', '').replace('/', '_')
                output_path = Path(output_dir) / f"{safe_name}_digest.txt"
            
            result = await ingest_repository_async(
                repo_url,
                include_patterns=include_patterns,
                exclude_patterns=exclude_patterns,
                max_file_size=max_file_size,
                branch=branch,
                token=token,
                output_path=output_path,
            )
            return repo_url, result
    
    # Process all repositories concurrently
    tasks = [ingest_single(repo_url) for repo_url in repository_urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    successful_results = []
    errors = []
    
    for result in results:
        if isinstance(result, Exception):
            errors.append({"repository": "unknown", "error": str(result)})
        else:
            repo_url, tool_result = result
            if tool_result.status == "success":
                successful_results.append(tool_result.data)
            else:
                errors.append({"repository": repo_url, "error": tool_result.message})
    
    return ToolResult(
        status="success" if not errors else "partial",
        data={
            "successful_ingests": successful_results,
            "errors": errors,
            "total_repositories": len(repository_urls),
            "successful_count": len(successful_results),
            "error_count": len(errors),
        },
        message=f"Processed {len(repository_urls)} repositories: {len(successful_results)} successful, {len(errors)} errors",
    )


__all__ = [
    "GitIngestResult",
    "ingest_repository",
    "ingest_repository_async",
    "batch_ingest_repositories",
    "batch_ingest_repositories_async",
]
