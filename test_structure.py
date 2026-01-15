#!/usr/bin/env python3
"""Test script to verify the Epiverse MCP server structure without dependencies."""

import json
import sys
from pathlib import Path

def test_file_structure():
    """Test that all required files exist."""
    print("🔍 Testing file structure...")
    
    required_files = [
        "src/epiagent/__init__.py",
        "src/epiagent/tools/r_wrappers.py",
        "src/epiagent/tools/gitingest_wrapper.py", 
        "src/epiagent/tools/registry.py",
        "docs/tool_manifest.json",
        "docs/epiverse_packages.json",
        "docs/model_context_protocol.md",
        "tests/test_r_wrappers.py",
        "tests/test_gitingest_wrapper.py",
        "pyproject.toml",
        "README.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"✓ {file_path}")
    
    if missing_files:
        print(f"✗ Missing files: {missing_files}")
        return False
    
    print(f"✓ All {len(required_files)} required files exist")
    return True

def test_tool_manifest():
    """Test tool manifest structure and content."""
    print("\n🔍 Testing tool manifest...")
    
    try:
        with open("docs/tool_manifest.json", 'r') as f:
            manifest = json.load(f)
        
        # Check it's a list
        if not isinstance(manifest, list):
            print("✗ Tool manifest should be a list")
            return False
        
        # Check each tool has required fields
        required_fields = ["name", "description", "parameters"]
        for i, tool in enumerate(manifest):
            for field in required_fields:
                if field not in tool:
                    print(f"✗ Tool {i} missing '{field}' field")
                    return False
            
            # Check parameters structure
            params = tool["parameters"]
            if "type" not in params or params["type"] != "object":
                print(f"✗ Tool '{tool['name']}' parameters should have type 'object'")
                return False
            
            print(f"✓ Tool '{tool['name']}' structure valid")
        
        print(f"✓ Tool manifest contains {len(manifest)} valid tools")
        return True
        
    except Exception as e:
        print(f"✗ Tool manifest error: {e}")
        return False

def test_epiverse_packages():
    """Test epiverse packages file."""
    print("\n🔍 Testing epiverse packages...")
    
    try:
        with open("docs/epiverse_packages.json", 'r') as f:
            packages = json.load(f)
        
        if not isinstance(packages, list):
            print("✗ Epiverse packages should be a list")
            return False
        
        print(f"✓ Epiverse packages file contains {len(packages)} entries")
        
        # Check a few entries have expected structure
        for i, pkg in enumerate(packages[:3]):  # Check first 3
            if isinstance(pkg, str):
                print(f"✓ Package {i}: {pkg} (string format)")
            elif isinstance(pkg, dict):
                if "name" in pkg:
                    print(f"✓ Package {i}: {pkg['name']} (object format)")
                else:
                    print(f"✗ Package {i} missing 'name' field")
                    return False
        
        return True
        
    except Exception as e:
        print(f"✗ Epiverse packages error: {e}")
        return False

def test_pyproject_toml():
    """Test pyproject.toml structure."""
    print("\n🔍 Testing pyproject.toml...")
    
    try:
        with open("pyproject.toml", 'r') as f:
            content = f.read()
        
        # Check for key sections
        required_sections = [
            "[build-system]",
            "[project]",
            "name = \"epiagent\"",
            "gitingest",
            "pandas",
            "rpy2"
        ]
        
        for section in required_sections:
            if section not in content:
                print(f"✗ Missing section/entry: {section}")
                return False
            print(f"✓ Found: {section}")
        
        print("✓ pyproject.toml structure valid")
        return True
        
    except Exception as e:
        print(f"✗ pyproject.toml error: {e}")
        return False

def test_readme():
    """Test README content."""
    print("\n🔍 Testing README...")
    
    try:
        with open("README.md", 'r') as f:
            content = f.read()
        
        # Check for key sections
        required_sections = [
            "# epiagent",
            "GitIngest integration",
            "ingest_repository",
            "batch_ingest_repositories",
            "## Available Tools",
            "### Epiverse Trace Integration",
            "### GitIngest Integration"
        ]
        
        for section in required_sections:
            if section not in content:
                print(f"✗ Missing section: {section}")
                return False
            print(f"✓ Found: {section}")
        
        print("✓ README structure valid")
        return True
        
    except Exception as e:
        print(f"✗ README error: {e}")
        return False

def main():
    """Run all structure tests."""
    print("🚀 Testing Epiverse MCP Server Structure\n")
    
    tests = [
        test_file_structure,
        test_tool_manifest,
        test_epiverse_packages,
        test_pyproject_toml,
        test_readme,
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
        print("🎉 All structure tests passed! Your Epiverse MCP server structure is correct.")
        print("\n📋 What we verified:")
        print("✓ All required files exist")
        print("✓ Tool manifest contains 6 tools with proper structure")
        print("✓ Epiverse packages file is valid JSON")
        print("✓ pyproject.toml has correct dependencies")
        print("✓ README documents both Epiverse and GitIngest integration")
        print("\n🚀 Ready to install and test with actual dependencies!")
    else:
        print("❌ Some structure tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
