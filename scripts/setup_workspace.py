#!/usr/bin/env python3
"""Setup script to configure epiagent MCP in any workspace."""

import json
import os
import sys
from pathlib import Path


def find_epiagent_path():
    """Find the epiagent installation path."""
    # This script should be in epiagent/scripts/
    script_path = Path(__file__).resolve()
    epiagent_root = script_path.parent.parent
    python_path = epiagent_root / ".venv" / "bin" / "python"
    
    if not python_path.exists():
        print(f"❌ Error: Python executable not found at {python_path}")
        print("   Make sure epiagent is installed with: uv sync")
        sys.exit(1)
    
    return epiagent_root, python_path


def setup_workspace(target_dir):
    """Configure epiagent MCP in the target workspace."""
    target_path = Path(target_dir).resolve()
    
    if not target_path.is_dir():
        print(f"❌ Error: {target_dir} is not a valid directory")
        sys.exit(1)
    
    # Find epiagent installation
    epiagent_root, python_path = find_epiagent_path()
    
    # Create .vscode directory if it doesn't exist
    vscode_dir = target_path / ".vscode"
    vscode_dir.mkdir(exist_ok=True)
    
    # Create mcp.json
    mcp_config = {
        "inputs": [],
        "servers": {
            "epiagent": {
                "command": str(python_path),
                "args": ["-m", "epiagent"]
            }
        }
    }
    
    mcp_json_path = vscode_dir / "mcp.json"
    with open(mcp_json_path, "w") as f:
        json.dump(mcp_config, f, indent=2)
    print(f"✅ Created {mcp_json_path}")
    
    # Create or update settings.json
    settings_json_path = vscode_dir / "settings.json"
    
    if settings_json_path.exists():
        with open(settings_json_path, "r") as f:
            settings = json.load(f)
    else:
        settings = {}
    
    # Add/update MCP settings
    settings["github.copilot.chat.mcp.enabled"] = True
    if "github.copilot.chat.mcp.servers" not in settings:
        settings["github.copilot.chat.mcp.servers"] = {}
    
    settings["github.copilot.chat.mcp.servers"]["epiagent"] = {
        "command": str(python_path),
        "args": ["-m", "epiagent"],
        "cwd": str(epiagent_root)
    }
    
    with open(settings_json_path, "w") as f:
        json.dump(settings, f, indent=2)
    print(f"✅ Updated {settings_json_path}")
    
    # Success message
    print(f"\n🎉 Epiagent MCP configured for {target_path.name}")
    print(f"\n📍 Configuration:")
    print(f"   Epiagent: {epiagent_root}")
    print(f"   Python:   {python_path}")
    print(f"\n⚡ Next steps:")
    print(f"   1. Reload VS Code window (Cmd+Shift+P → 'Developer: Reload Window')")
    print(f"   2. Verify with: {python_path} -m epiagent --help")
    print(f"   3. Try asking your AI assistant an epidemiology question!")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python setup_workspace.py <target-directory>")
        print("\nExample:")
        print("  python setup_workspace.py ~/Documents/Work/my-analysis")
        print("  python setup_workspace.py .  # Current directory")
        sys.exit(1)
    
    target_dir = sys.argv[1]
    setup_workspace(target_dir)


if __name__ == "__main__":
    main()
