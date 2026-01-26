
import json
from pathlib import Path
import pytest

def test_tool_manifest_exists():
    """Test that the tool manifest file exists."""
    # Assuming the test is run from project root, or we find the root relative to this file
    # This file is in tests/
    project_root = Path(__file__).parent.parent
    manifest_path = project_root / "docs" / "tool_manifest.json"
    assert manifest_path.exists(), f"Manifest not found at {manifest_path}"

def test_tool_manifest_content():
    """Test that the tool manifest contains expected tools."""
    project_root = Path(__file__).parent.parent
    manifest_path = project_root / "docs" / "tool_manifest.json"
    
    if not manifest_path.exists():
        pytest.skip("Tool manifest not found")
        
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    
    expected_tools = [
        "list_epiverse_packages",
        "call_epiverse_function", 
        "ingest_repository",
        "ingest_repository_async",
        "batch_ingest_repositories",
        "batch_ingest_repositories_async"
    ]
    
    tool_names = [tool["name"] for tool in manifest]
    
    for expected in expected_tools:
        assert expected in tool_names, f"Tool '{expected}' missing from manifest"
