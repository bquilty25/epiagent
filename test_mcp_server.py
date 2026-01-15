#!/usr/bin/env python3
"""Test script to verify the Epiverse MCP server functionality."""

import sys
import json
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test that all modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        from epiagent import (
            ToolResult,
            call_epiverse_function,
            list_epiverse_packages,
            GitIngestResult,
            ingest_repository,
            batch_ingest_repositories,
        )
        print("✓ All core imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_tool_manifest():
    """Test that the tool manifest is valid JSON and contains expected tools."""
    print("\n🔍 Testing tool manifest...")
    
    try:
        manifest_path = Path("docs/tool_manifest.json")
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
            if expected in tool_names:
                print(f"✓ Tool '{expected}' found in manifest")
            else:
                print(f"✗ Tool '{expected}' missing from manifest")
                return False
        
        print(f"✓ Tool manifest contains {len(manifest)} tools")
        return True
        
    except Exception as e:
        print(f"✗ Tool manifest error: {e}")
        return False

def test_registry():
    """Test the Epiverse registry functionality."""
    print("\n🔍 Testing registry...")
    
    try:
        from epiagent.tools.registry import get_registry, EpiversePackage
        
        # Test registry loading
        registry = get_registry()
        print(f"✓ Registry loaded with {len(registry.packages)} packages")
        
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
        print("✓ Package creation and serialization works")
        
        return True
        
    except Exception as e:
        print(f"✗ Registry error: {e}")
        return False

def test_gitingest_wrapper():
    """Test GitIngest wrapper functionality."""
    print("\n🔍 Testing GitIngest wrapper...")
    
    try:
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
        
        print("✓ GitIngest wrapper functionality works")
        return True
        
    except Exception as e:
        print(f"✗ GitIngest wrapper error: {e}")
        return False

def test_tool_result():
    """Test ToolResult class."""
    print("\n🔍 Testing ToolResult...")
    
    try:
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
        
        print("✓ ToolResult serialization works")
        return True
        
    except Exception as e:
        print(f"✗ ToolResult error: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Testing Epiverse MCP Server\n")
    
    tests = [
        test_imports,
        test_tool_manifest,
        test_registry,
        test_gitingest_wrapper,
        test_tool_result,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your Epiverse MCP server is ready to use.")
        print("\n📋 Next steps:")
        print("1. Install dependencies: pip install -e .")
        print("2. Test with actual data: python -c \"from epiagent import list_epiverse_packages; print(list_epiverse_packages().to_payload())\"")
        print("3. Test GitIngest: python -c \"from epiagent import ingest_repository; print(ingest_repository('https://github.com/octocat/Hello-World').to_payload())\"")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
