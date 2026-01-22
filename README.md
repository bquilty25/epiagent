# epiagent

[![Lifecycle: Experimental](https://img.shields.io/badge/lifecycle-experimental-orange.svg)](https://lifecycle.r-lib.org/articles/stages.html#experimental)


**A Model Context Protocol (MCP) server that empowers AI agents to perform high-quality epidemiological analysis using the [Epiverse-TRACE](https://epiverse-trace.github.io/) ecosystem.**

`epiagent` bridges the gap between Large Language Models and rigorous epidemiological tools. It provides agents with semantic access to R packages (like `linelist` and `epiparameter`) and safeguards their workflow with professional Standard Operating Procedures (Agent Skills).

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

### GitHub Copilot
1.  **Open Copilot Chat** in VS Code.
2.  Enable the **epiagent** tool (via "Configure tools").
3.  Ask: *"@workspace Which Epiverse package handles contact tracing data?"*

### Claude Desktop / CLI
Add to your Claude config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "epiagent": {
      "command": "/ABSOLUTE/PATH/TO/epiagent/.venv/bin/python",
      "args": ["-m", "epiagent"]
    }
  }
}
```

### Remote / Cross-Repo Usage
To use `epiagent` while working in *another* analysis repository, configure that repo's `.vscode/mcp.json` to point here:

```json
{
  "mcpServers": {
    "epiagent": {
      "command": "/ABSOLUTE/PATH/TO/epiagent/.venv/bin/python",
      "args": ["-m", "epiagent"],
      "enabled": true
    }
  }
}
```

## Features

| Function                              | Description                                                                       |
| :------------------------------------ | :-------------------------------------------------------------------------------- |
| **`find_relevant_packages(query)`**   | Semantically matches user questions to the most relevant Epiverse TRACE packages. |
| **`list_epiverse_packages()`**        | Provides metadata on all available Epiverse tools.                                |
| **`call_epiverse_function(pkg, fn)`** | Safely executes R functions from Python via `rpy2`.                               |
| **`ingest_repository(url)`**          | Creates AI-optimized digests of external codebases.                               |

## Open Standards

This project is built on:
*   **[Model Context Protocol (MCP)](https://modelcontextprotocol.io/)**: For universal tool connectivity.
*   **[Agent Skills](https://agentskills.io)**: For defining portable, professional analytical workflows (see `.agent/skills/epidemiological_analysis`).
