# epiagent

[![Lifecycle: Experimental](https://img.shields.io/badge/lifecycle-experimental-orange.svg)](https://lifecycle.r-lib.org/articles/stages.html#experimental)


**A Model Context Protocol (MCP) server that empowers AI agents to perform high-quality epidemiological analysis using the [Epiverse-TRACE](https://epiverse-trace.github.io/), [Epiforecasts](https://epiforecasts.io/), and [RECON](https://www.repidemicsconsortium.org/) ecosystems.**

`epiagent` connects Large Language Models to R-based epidemiological tools. It gives agents semantic access to packages (like `linelist` and `epiparameter`) and guides their workflow using Standard Operating Procedures (Agent Skills).

## Installation

### 1. Zero-Config Setup (Recommended)
Fastest method using `uv`.

```bash
git clone https://github.com/bquilty25/epiagent.git
cd epiagent
uv sync
code .  # Opens VS Code with pre-configured settings
```

### 2. Manual Setup
Standard pip installation.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
# Reload VS Code window to apply changes
```

## Usage

### GitHub Copilot (VS Code)
1.  **Open Copilot Chat** in VS Code.
2.  Enable the **epiagent** tool (via "Configure tools").
3.  Ask: *"@workspace Which Epiverse package handles contact tracing data?"*

### Remote / Cross-Repo Usage

#### Method 1: Built-in Setup Command (Recommended) 🚀

Use the built-in `setup` command from anywhere:

```bash
# From your epiagent directory:
/path/to/epiagent/.venv/bin/python -m epiagent setup /path/to/your-workspace

# Or setup the current directory:
cd /path/to/your-workspace
/path/to/epiagent/.venv/bin/python -m epiagent setup .
```

**Real example:**
```bash
/Users/yourname/epiagent/.venv/bin/python -m epiagent setup ~/my-analysis
```

The command will:
- ✅ Auto-detect the epiagent installation path
- ✅ Create both `.vscode/mcp.json` and `.vscode/settings.json`
- ✅ Use correct absolute paths automatically
- ✅ Preserve existing VS Code settings
- ✅ Work from any directory

**Then:** Reload VS Code (`Cmd+Shift+P` → "Developer: Reload Window") and you're done!

---

#### Method 2: Manual Setup
To use `epiagent` while working in *another* analysis repository:

#### 1. Find Your Epiagent Installation Path
First, locate where epiagent is installed:
```bash
# Navigate to your epiagent directory
cd /path/to/epiagent

# Get the full path to the Python executable
pwd  # This shows the epiagent directory
# The Python path will be: <that-path>/.venv/bin/python
```

#### 2. Create Configuration Files
In your **other workspace**, create or update these two files:

**`.vscode/mcp.json`** (create this file):
```json
{
  "inputs": [],
  "servers": {
    "epiagent": {
      "command": "/ABSOLUTE/PATH/TO/epiagent/.venv/bin/python",
      "args": ["-m", "epiagent"]
    }
  }
}
```

**`.vscode/settings.json`** (create or merge with existing):
```json
{
  "github.copilot.chat.mcp.enabled": true,
  "github.copilot.chat.mcp.servers": {
    "epiagent": {
      "command": "/ABSOLUTE/PATH/TO/epiagent/.venv/bin/python",
      "args": ["-m", "epiagent"],
      "cwd": "/ABSOLUTE/PATH/TO/epiagent"
    }
  }
}
```

> **🔧 Important**: Replace `/ABSOLUTE/PATH/TO/epiagent` with your actual path (e.g., `/Users/yourname/epiagent`)

#### 3. Reload VS Code
**Critical**: Press `Cmd+Shift+P` (or `Ctrl+Shift+P` on Windows/Linux), type "Developer: Reload Window", and press Enter.

#### 4. Verify It Works
Test the connection by running this command in your terminal:
```bash
/ABSOLUTE/PATH/TO/epiagent/.venv/bin/python -m epiagent --help
```

If you see the FastMCP banner, epiagent is working! Now try asking your AI assistant an epidemiology question.

#### Troubleshooting
- **"Command not found"**: Double-check the Python path exists: `ls -la /path/to/epiagent/.venv/bin/python`
- **Still not working**: Check VS Code's Output panel (View → Output) and select "MCP" from the dropdown
- **Wrong format error**: Ensure you're using `"servers"` (not `"mcpServers"`) in `mcp.json`


## Features

| Function                              | Description                                                                       |
| :------------------------------------ | :-------------------------------------------------------------------------------- |
| **`find_relevant_packages(query)`**   | Semantically matches user questions to the most relevant Epiverse TRACE packages. |
| **`list_epiverse_packages()`**        | Provides metadata on all available Epiverse tools. (Alias: `get_packages`)        |
| **`refresh_packages()`**              | Refreshes the package registry from GitHub.                                       |
| **`call_epiverse_function(pkg, fn)`** | Safely executes R functions from Python via `rpy2`.                               |
| **`ingest_repository(url)`**          | Creates AI-optimized digests of external codebases.                               |

## Open Standards

This project is built on:
*   **[Model Context Protocol (MCP)](https://modelcontextprotocol.io/)**: For universal tool connectivity.
*   **[Agent Skills](https://agentskills.io)**: For defining portable, professional analytical workflows (see `.agent/skills/epidemiological_analysis`).
