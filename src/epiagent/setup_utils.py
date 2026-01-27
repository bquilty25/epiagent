"""Workspace setup utilities for epiagent MCP."""

import json
import sys
from pathlib import Path


def find_epiagent_installation():
    """Find the epiagent installation path.
    
    Returns:
        tuple: (epiagent_root, python_path)
    """
    # This module is in src/epiagent/
    module_path = Path(__file__).resolve()
    epiagent_root = module_path.parent.parent.parent
    python_path = epiagent_root / ".venv" / "bin" / "python"
    
    if not python_path.exists():
        print(f"❌ Error: Python executable not found at {python_path}")
        print("   Make sure epiagent is installed with: uv sync")
        sys.exit(1)
    
    return epiagent_root, python_path


def setup_workspace(target_dir):
    """Configure epiagent MCP in the target workspace.
    
    Args:
        target_dir: Path to the workspace directory to configure
    """
    target_path = Path(target_dir).resolve()
    
    if not target_path.is_dir():
        print(f"❌ Error: {target_dir} is not a valid directory")
        sys.exit(1)
    
    # Find epiagent installation
    epiagent_root, python_path = find_epiagent_installation()
    
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
