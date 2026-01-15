# epiagent

> **🚧 Work in Progress**

A Model Context Protocol (MCP) server that enables AI agents to use [Epiverse Trace](https://epiverse-trace.github.io/) R packages for epidemiological analysis.

## Roadmap

- [x] **Package registry** – 67+ Epiverse packages with metadata, tags, categories
- [x] **Epiverse-first routing** – `find_relevant_packages()` matches queries to packages
- [x] **R function execution** – Call any R function via `rpy2` with structured I/O
- [x] **Codebase analysis** – GitIngest creates AI-readable digests of repos
- [ ] **Agentic orchestration** – Context management and multi-step reasoning
- [ ] **Evaluation framework** – Benchmarks for epidemiological tasks

## Quick Start

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
```

## Usage

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
