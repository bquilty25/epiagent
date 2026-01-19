# epiagent

> **🚧 Work in Progress**

A Model Context Protocol (MCP) server that enables AI agents to use [Epiverse Trace](https://epiverse-trace.github.io/) R packages for epidemiological analysis.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/bquilty25/epiagent.git
   cd epiagent
   ```

2. **Create virtual environment and install:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e ".[dev]"
   ```

3. **Configure MCP in VS Code:**
   - The `.vscode/mcp.json` file is already included
   - Reload VS Code: `Cmd+Shift+P` → "Developer: Reload Window"
   - Open Copilot Chat
   - Click "Configure tools" (icon in chat interface)
   - Search for "epiagent"
   - Check the box to enable the tools

4. **Start using:**
   Ask Copilot questions like:
   ```
   @workspace What Epiverse packages can help estimate CFR?
   ```

## Usage with GitHub Copilot

After installation, the MCP server exposes 4 tools to Copilot:

- **list_packages**: List available Epiverse tools
- **call_function**: Execute R functions
- **find_tools**: Semantic search for relevant packages
- **ingest_git_repo**: Analyse external codebases

See [docs/ebola-outbreak-analysis.md](docs/ebola-outbreak-analysis.md) for a complete vignette.

### Troubleshooting

If tools don't appear in Copilot Chat:

1. Reload VS Code: `Cmd+Shift+P` → "Developer: Reload Window"
2. In Copilot Chat, click "Configure tools" and enable "epiagent"
3. Check `.vscode/mcp.json` has the correct Python path
4. Check Output panel: `Cmd+Shift+U` → "GitHub Copilot Chat"

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
