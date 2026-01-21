
import json
import pytest
from pathlib import Path
import sys

# Ensure we can import from src if not installed in editable mode
# (Check if standard installation covers this, otherwise simpler to rely on pytest pythonpath)

def test_imports():
    """Test that all core modules can be imported."""
    try:
        from epiagent import (
            ToolResult,
            call_epiverse_function,
            list_epiverse_packages,
            ingest_repository,
        )
    except ImportError as e:
        pytest.fail(f"Import error: {e}")

def test_tool_manifest():
    """Test that the tool manifest is valid JSON and contains expected tools."""
    manifest_path = Path("docs/tool_manifest.json")
    if not manifest_path.exists():
        pytest.skip("Tool manifest not found at docs/tool_manifest.json")
    
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    
    expected_tools = [
        "list_epiverse_packages",
        "call_epiverse_function", 
        "ingest_repository",
        # names might vary slightly in implementation vs manifest, checking key ones
    ]
    
    tool_names = [tool["name"] for tool in manifest]
    
    for expected in expected_tools:
        assert expected in tool_names, f"Tool '{expected}' missing from manifest"

def test_registry():
    """Test the Epiverse registry functionality."""
    from epiagent.tools.registry import get_registry, EpiversePackage
    
    # Test registry loading
    registry = get_registry()
    assert len(registry.packages) > 0, "Registry should not be empty"
    
    # Test package creation
    package = EpiversePackage(
        name="test-package",
        summary="Test package for validation",
        category="r_package",
        topics=["test", "validation"]
    )
    
    data = package.to_dict()
    assert data["name"] == "test-package"
    assert data["category"] == "r_package"

def test_gitingest_wrapper():
    """Test GitIngest wrapper functionality."""
    from epiagent.tools.gitingest_wrapper import GitIngestResult
    
    # Test result creation
    result = GitIngestResult(
        summary="Repository: test/repo\nFiles analyzed: 5\nEstimated tokens: 1.2k",
        tree="Directory structure:\n└── test-repo/\n    └── README.md",
        content="================================================\nFILE: README.md\n================================================\n# Test",
        repository_url="https://github.com/test/repo",
        files_analyzed=5,
        estimated_tokens=1200,
    )
    
    # Test serialization
    data = result.to_dict()
    assert data["repository_url"] == "https://github.com/test/repo"
    assert data["files_analyzed"] == 5
    
    # Test context generation
    context = result.get_full_context()
    assert "Repository: test/repo" in context
    assert "Directory structure:" in context

def test_tool_result():
    """Test ToolResult class."""
    from epiagent.tools.r_wrappers import ToolResult
    
    # Test success result
    result = ToolResult(
        status="success",
        data={"test": "data"},
        message="Test successful"
    )
    
    payload = result.to_payload()
    assert payload["status"] == "success"
    assert payload["data"]["test"] == "data"
    assert payload["message"] == "Test successful"
    
    # Test error result
    error_result = ToolResult(
        status="error",
        message="Test error"
    )
    
    error_payload = error_result.to_payload()
    assert error_payload["status"] == "error"
    assert error_payload["message"] == "Test error"
