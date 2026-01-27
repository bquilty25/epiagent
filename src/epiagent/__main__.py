"""MCP Server entry point for epiagent."""

import sys
import os
from contextlib import contextmanager

# Disable FastMCP banners and output that breaks JSON-RPC
os.environ["FASTMCP_DISABLE_BANNER"] = "1"
os.environ["FASTMCP_QUIET"] = "1"

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout

# Aggressively suppress stdout during imports and initialization
# This prevents FastMCP (and other libs) from printing banners that break JSON-RPC
with suppress_stdout():
    from fastmcp import FastMCP
    
    from . import (
        call_epiverse_function,
        find_relevant_packages,
        ingest_repository,
        list_epiverse_packages,
    )
    from pathlib import Path

    # Initialize FastMCP server
    mcp = FastMCP("epiagent")
    
    # Path to SOP document
    SOP_PATH = Path(__file__).resolve().parents[2] / "docs" / "SOP_epidemiological_analysis.md"

@mcp.resource("epiagent://sop")
def get_analysis_sop() -> str:
    """Return the Standard Operating Procedure for epidemiological analysis."""
    if SOP_PATH.exists():
        return SOP_PATH.read_text(encoding="utf-8")
    return "SOP document not found."

@mcp.prompt("standard_operating_procedure")
def sop_prompt() -> list:
    """Return the Standard Operating Procedure for epidemiological analysis as a prompt."""
    return [{
        "role": "user",
        "content": {
            "type": "text",
            "text": f"Please follow the Standard Operating Procedure for this analysis:\n\n{get_analysis_sop()}"
        }
    }]


@mcp.tool()
def list_packages(refresh: bool = False) -> dict:
    """List all available Epiverse-TRACE, Epiforecasts, and RECON packages.
    
    Args:
        refresh: Whether to refresh the package registry from GitHub.
    """
    result = list_epiverse_packages(refresh=refresh)
    return result.to_payload()


@mcp.tool()
def get_packages() -> dict:
    """Get all available Epiverse-TRACE, Epiforecasts, and RECON packages.
    
    Alias for list_packages.
    """
    return list_packages(refresh=False)


@mcp.tool()
def refresh_packages() -> str:
    """Refresh the package registry from GitHub and return a summary.
    
    This connects to GitHub to fetch the latest list of packages from 
    Epiverse-TRACE, Epiforecasts, and RECON.
    """
    result = list_epiverse_packages(refresh=True)
    if result.status == "success":
        count = len(result.data.get("packages", []))
        return f"Registry refreshed. Found {count} packages."
    else:
        return f"Failed to refresh registry: {result.message}"


@mcp.tool()
def call_function(
    package: str,
    function: str,
    args: list = None,
    kwargs: dict = None,
) -> dict:
    """Call a function from an Epiverse, Epiforecasts, or RECON package.
    
    Args:
        package: Name of the R package (e.g., 'epiparameter').
        function: Name of the function to call.
        args: List of positional arguments.
        kwargs: Dictionary of keyword arguments.
    """
    result = call_epiverse_function(package, function, args, kwargs)
    return result.to_payload()


@mcp.tool()
def find_tools(query: str) -> list:
    """Find relevant Epiverse, Epiforecasts, or RECON packages for a specific epidemiological task.
    
    Args:
        query: Natural language description of the task (e.g. "estimate incubation period").
    """
    matches = find_relevant_packages(query)
    return [m.to_dict() for m in matches]


@mcp.tool()
def ingest_git_repo(
    url: str,
    max_file_size: int = None,
    include_patterns: list = None,
    exclude_patterns: list = None,
) -> dict:
    """Ingest a GitHub repository to understand its codebase.
    
    Args:
        url: URL of the GitHub repository.
        max_file_size: Maximum file size in bytes to process.
        include_patterns: Glob patterns for files to include.
        exclude_patterns: Glob patterns for files to exclude.
    """
    result = ingest_repository(
        url,
        max_file_size=max_file_size,
        include_patterns=include_patterns,
        exclude_patterns=exclude_patterns,
    )
    return result.to_payload()


if __name__ == "__main__":
    # Check if this is a setup command
    if len(sys.argv) > 1 and sys.argv[1] == "setup":
        from .setup_utils import setup_workspace
        
        if len(sys.argv) < 3:
            print("Usage: python -m epiagent setup <target-directory>")
            print("\nExamples:")
            print("  python -m epiagent setup ~/Documents/Work/my-analysis")
            print("  python -m epiagent setup .  # Current directory")
            sys.exit(1)
        
        target_dir = sys.argv[2]
        setup_workspace(target_dir)
    elif len(sys.argv) > 1 and sys.argv[1] in ["--help", "-h"]:
        print("Epiagent MCP Server")
        print("\nUsage:")
        print("  python -m epiagent              # Start MCP server")
        print("  python -m epiagent setup <dir>  # Configure workspace for MCP")
        print("\nOptions:")
        print("  -h, --help                      # Show this help message")
    else:
        # Run the MCP server (default behavior)
        mcp.run()
