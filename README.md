# epiagent

This repository sketches a model context protocol that allows a language-model
agent to interact with Epiverse Trace R packages through Python.

Key components:

* `src/epiagent/agent.py` provides a lightweight `EpiAgent` class that can
  shortlist relevant Epiverse packages, plan suggested tool calls, and execute
  them through the wrappers.
* `src/epiagent/tools/r_wrappers.py` exposes dynamic wrappers that can call any
  Epiverse Trace function via `rpy2` while handling argument/result
  serialisation for agents.
* `src/epiagent/tools/registry.py` maintains a synchronisable catalogue of
  Epiverse Trace repositories backed by `docs/epiverse_packages.json`, including
  GitHub-sourced summaries, topical tags and coarse categories to help the
  agent pick the right package.
* `docs/tool_manifest.json` supplies structured metadata describing the
  high-level tools available to an agent.
* `docs/model_context_protocol.md` summarises the end-to-end workflow for
  curation, manifest construction and agentic orchestration.

Use the `EpiAgent` helper when you need a quick end-to-end loop:

```python
from epiagent import EpiAgent, plan_epiverse_goal

agent = EpiAgent()
report = agent.run("estimate Rt from this linelist and clean the variable names")
print(report["plan"])

planning = plan_epiverse_goal("estimate Rt from this linelist and clean the variable names")
print(planning["shortlist"])
```

Under the hood the agent calls `list_epiverse_packages` to surface candidate
packages, matches keywords from the request against registry metadata, and then
executes the corresponding `call_epiverse_function` steps. Use the
`list_epiverse_packages` tool with `refresh=true` to ensure the registry tracks
newly published Epiverse Trace repositories before calling the wrappers. Keep
the manifest lightweight—link out to package READMEs or vignettes rather than
embedding every repository's documentation in the MCP assets.

## Example: running on Epi R Handbook data

The repository ships with `examples/handbook_workflow.py`, a small script that
downloads the flu H7N9 linelist from the Epi R Handbook and lets the reference
agent plan and execute the steps it can handle without a full R toolchain. The
dynamic wrappers now include Python fallbacks for
`linelist::clean_variable_names` and `incidence2::incidence`, so you can see the
workflow in action even if `rpy2`/R are not installed.

```bash
pip install pandas  # optional if you have not already installed it
python -m examples.handbook_workflow
```

When R and the Epiverse packages are available the same script will call the
true R implementations; otherwise it produces incidence curves and cleaned
columns via the fallbacks and explains how to enable the remaining steps.
