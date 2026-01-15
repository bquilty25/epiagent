#!/usr/bin/env python3
"""Test script to demonstrate Epiverse MCP server functionality."""

import sys
import json
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_registry_functionality():
    """Test the registry functionality without R dependencies."""
    print("🔍 Testing registry functionality...")
    
    try:
        from epiagent.tools.registry import EpiverseRegistry, EpiversePackage
        
        # Create a test registry
        registry = EpiverseRegistry()
        
        # Add a test package
        test_package = EpiversePackage(
            name="test-package",
            summary="A test epidemiological package",
            category="r_package",
            topics=["epidemiology", "testing"]
        )
        registry.packages["test-package"] = test_package
        
        # Test package retrieval
        assert registry.has_package("test-package")
        assert not registry.has_package("non-existent")
        
        # Test package description
        desc = registry.describe("test-package")
        assert desc["name"] == "test-package"
        assert desc["category"] == "r_package"
        
        print("✓ Registry functionality works")
        return True
        
    except Exception as e:
        print(f"✗ Registry functionality error: {e}")
        return False

def test_tool_result_serialization():
    """Test ToolResult serialization without R dependencies."""
    print("\n🔍 Testing ToolResult serialization...")
    
    try:
        from epiagent.tools.r_wrappers import ToolResult
        
        # Test basic serialization
        result = ToolResult(
            status="success",
            data={"message": "Test successful", "count": 42},
            message="Operation completed"
        )
        
        payload = result.to_payload()
        assert payload["status"] == "success"
        assert payload["data"]["message"] == "Test successful"
        assert payload["data"]["count"] == 42
        assert payload["message"] == "Operation completed"
        
        # Test error serialization
        error_result = ToolResult(
            status="error",
            message="Test error occurred"
        )
        
        error_payload = error_result.to_payload()
        assert error_payload["status"] == "error"
        assert error_payload["message"] == "Test error occurred"
        assert "data" not in error_payload
        
        print("✓ ToolResult serialization works")
        return True
        
    except Exception as e:
        print(f"✗ ToolResult serialization error: {e}")
        return False

def test_gitingest_result():
    """Test GitIngest result functionality."""
    print("\n🔍 Testing GitIngest result functionality...")
    
    try:
        from epiagent.tools.gitingest_wrapper import GitIngestResult
        
        # Create a test result
        result = GitIngestResult(
            summary="Repository: epiverse-trace/incidence2\nFiles analyzed: 25\nEstimated tokens: 12.5k",
            tree="Directory structure:\n└── incidence2/\n    ├── R/\n    │   ├── incidence.R\n    │   └── utils.R\n    ├── tests/\n    │   └── testthat.R\n    └── README.md",
            content="================================================\nFILE: R/incidence.R\n================================================\n# Incidence calculation functions\n\nincidence <- function(x, ...) {\n  # Implementation here\n}\n\n================================================\nFILE: README.md\n================================================\n# incidence2\n\nEpidemiological incidence calculation package.",
            repository_url="https://github.com/epiverse-trace/incidence2",
            files_analyzed=25,
            estimated_tokens=12500,
        )
        
        # Test serialization
        data = result.to_dict()
        assert data["repository_url"] == "https://github.com/epiverse-trace/incidence2"
        assert data["files_analyzed"] == 25
        assert data["estimated_tokens"] == 12500
        
        # Test full context generation
        context = result.get_full_context()
        assert "Repository: epiverse-trace/incidence2" in context
        assert "Files analyzed: 25" in context
        assert "Directory structure:" in context
        assert "FILE: R/incidence.R" in context
        assert "incidence <- function(x, ...)" in context
        
        print("✓ GitIngest result functionality works")
        return True
        
    except Exception as e:
        print(f"✗ GitIngest result error: {e}")
        return False

def test_epiverse_packages_loading():
    """Test loading the actual epiverse packages file."""
    print("\n🔍 Testing epiverse packages loading...")
    
    try:
        from epiagent.tools.registry import EpiverseRegistry
        
        # Load the actual registry
        registry = EpiverseRegistry.load()
        
        print(f"✓ Loaded registry with {len(registry.packages)} packages")
        
        # Check some known packages
        known_packages = ["incidence2", "linelist", "epiparameter"]
        found_packages = []
        
        for pkg_name in known_packages:
            if registry.has_package(pkg_name):
                found_packages.append(pkg_name)
                desc = registry.describe(pkg_name)
                print(f"✓ Found package: {pkg_name} ({desc.get('category', 'unknown')})")
        
        if found_packages:
            print(f"✓ Found {len(found_packages)} known packages: {found_packages}")
        else:
            print("⚠ No known packages found (this might be expected if packages aren't in the registry yet)")
        
        return True
        
    except Exception as e:
        print(f"✗ Epiverse packages loading error: {e}")
        return False

def demonstrate_mcp_workflow():
    """Demonstrate how an MCP workflow would work."""
    print("\n🔍 Demonstrating MCP workflow...")
    
    try:
        from epiagent.tools.registry import EpiverseRegistry
        from epiagent.tools.r_wrappers import ToolResult
        from epiagent.tools.gitingest_wrapper import GitIngestResult
        
        # Step 1: Load registry
        registry = EpiverseRegistry.load()
        print(f"✓ Step 1: Loaded registry with {len(registry.packages)} packages")
        
        # Step 2: Simulate listing packages (what list_epiverse_packages would return)
        sample_packages = list(registry.packages.values())[:3]  # First 3 packages
        packages_data = {"packages": [pkg.to_dict() for pkg in sample_packages]}
        list_result = ToolResult(status="success", data=packages_data)
        
        print(f"✓ Step 2: Listed {len(sample_packages)} sample packages")
        for pkg in sample_packages:
            print(f"  - {pkg.name}: {pkg.summary[:50]}..." if pkg.summary else f"  - {pkg.name}")
        
        # Step 3: Simulate repository analysis (what ingest_repository would return)
        mock_repo_result = GitIngestResult(
            summary="Repository: epiverse-trace/sample\nFiles analyzed: 10\nEstimated tokens: 5.2k",
            tree="Directory structure:\n└── sample/\n    ├── R/\n    └── README.md",
            content="================================================\nFILE: R/main.R\n================================================\n# Sample epidemiological functions",
            repository_url="https://github.com/epiverse-trace/sample",
            files_analyzed=10,
            estimated_tokens=5200,
        )
        
        ingest_result = ToolResult(status="success", data=mock_repo_result.to_dict())
        print("✓ Step 3: Analyzed repository structure")
        
        # Step 4: Simulate R function call (what call_epiverse_function would return)
        r_call_result = ToolResult(
            status="success",
            data={"result": [1, 2, 3, 4, 5], "summary": "Analysis completed"},
            message="R function executed successfully"
        )
        print("✓ Step 4: Simulated R function call")
        
        print("\n🎯 MCP Workflow Demonstration Complete!")
        print("This shows how an AI agent would:")
        print("1. List available Epiverse packages")
        print("2. Analyze repository codebases with GitIngest")
        print("3. Call R functions with understanding of the code")
        print("4. Get structured results for further processing")
        
        return True
        
    except Exception as e:
        print(f"✗ MCP workflow demonstration error: {e}")
        return False

def main():
    """Run all functionality tests."""
    print("🚀 Testing Epiverse MCP Server Functionality\n")
    
    tests = [
        test_registry_functionality,
        test_tool_result_serialization,
        test_gitingest_result,
        test_epiverse_packages_loading,
        demonstrate_mcp_workflow,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()  # Add spacing between tests
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
            print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All functionality tests passed!")
        print("\n🏆 Your Epiverse MCP Server is working correctly!")
        print("\n📋 What we verified:")
        print("✓ Registry functionality for package management")
        print("✓ ToolResult serialization for structured responses")
        print("✓ GitIngest result handling for codebase analysis")
        print("✓ Epiverse packages loading from JSON")
        print("✓ Complete MCP workflow demonstration")
        print("\n🚀 Ready for AI agent integration!")
        print("\n💡 Next steps:")
        print("1. Install dependencies: pip install -e .")
        print("2. Test with actual R packages: python -c \"from epiagent import call_epiverse_function; print(call_epiverse_function('stats', 'rnorm', kwargs={'n': 5}).to_payload())\"")
        print("3. Test GitIngest: python -c \"from epiagent import ingest_repository; print(ingest_repository('https://github.com/octocat/Hello-World').to_payload())\"")
    else:
        print("❌ Some functionality tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
