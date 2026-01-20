# epiagent

> **🚧 Work in Progress**

A Model Context Protocol (MCP) server that enables AI agents to use [Epiverse Trace](https://epiverse-trace.github.io/) R packages for epidemiological analysis.

## Open Standards

This project is built on two powerful open standards for agentic AI:

1.  **[Model Context Protocol (MCP)](https://modelcontextprotocol.io/)**: An open standard that enables AI agents to connect to data and tools. `epiagent` is a fully compliant MCP server, making it compatible with any MCP client (VS Code, Claude Desktop, formatting_agents, etc.).

2.  **[Agent Skills](https://antigravity.google/docs/skills)**: A standard for defining portable, structured capabilities for agents. The "Standard Operating Procedure" for this project is implemented as a formal **Skill** (`.agent/skills/epidemiological_analysis`), ensuring the agent has persistent, explicit instructions on how to conduct high-quality analysis.

## Installation & Getting Started

### 1. Zero-Config Setup (Recommended)
This method is fastest and ensures all dependencies are correctly locked.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/bquilty25/epiagent.git
   cd epiagent
   ```
2. **Install with `uv`**:
   ```bash
   uv sync
   ```
3. **Open in VS Code**:
   ```bash
   code .
   ```
   The `.vscode/mcp.json` is pre-configured to work immediately.

### 2. Manual Setup
If you prefer standard pip:

1. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Reload VS Code (`Cmd+Shift+P` → "Developer: Reload Window").

### 3. Usage with GitHub Copilot
Once installed:
1. Open Copilot Chat.
2. Ensure the **epiagent** tool is enabled (click "Configure tools").
3. Ask natural language questions like:
   > `@workspace What Epiverse packages can help estimate CFR?`

### 4. Usage with Claude Desktop / Claude Code
To use `epiagent` with Anthropic's Claude Desktop app or CLI:

1. Open your Claude configuration file:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add the `epiagent` server configuration (using the absolute path to your repo):

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
3. Restart Claude Desktop. The 🛠️ icon will appear, listing the Epiverse tools.

### Using Epiagent in Other Repositories

You can use `epiagent` while working in *any* other project (e.g., your specific analysis repo) by pointing VS Code to this installation.

1. **Open your analysis project** in VS Code.
2. Create or edit `.vscode/mcp.json`.
3. Add the `epiagent` configuration, pointing to the absolute path where you installed `epiagent`:

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

This allows you to access all Epiverse tools and the Standard Operating Procedure regardless of which folder you have open.

For user-level configuration (optional), add to VS Code User Settings:

```json
{
  "github.copilot.chat.mcp.enabled": true,
  "github.copilot.chat.mcp.servers": {
    "epiagent": {
      "command": "/FULL/PATH/TO/epiagent/.venv/bin/python",
      "args": ["-m", "epiagent"],
      "cwd": "/FULL/PATH/TO/epiagent"
    }
  }
}
```

## Python API Usage

```python
from epiagent import find_relevant_packages, call_epiverse_function

# 1. Find relevant Epiverse package
matches = find_relevant_packages("estimate CFR for COVID-19")
# → cfr (score=10.5), serofoi (4.0), ...

# 2. Call R function
result = call_epiverse_function("epiparameter", "epiparameter_db", 
    kwargs={"disease": "COVID-19", "epi_name": "incubation period"})
# → 15 COVID-19 incubation period distributions
```

## Tools

| Function                          | Description                         |
| --------------------------------- | ----------------------------------- |
| `find_relevant_packages(query)`   | Match queries to Epiverse packages  |
| `list_epiverse_packages()`        | List all 67+ packages with metadata |
| `call_epiverse_function(pkg, fn)` | Execute R function via rpy2         |
| `ingest_repository(url)`          | Create AI-readable codebase digest  |
