# epiagent

This repository sketches a model context protocol that allows a language-model
agent to interact with Epiverse Trace R packages through Python.

Key components:

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

Use the `list_epiverse_packages` tool with `refresh=true` to ensure the registry
tracks newly published Epiverse Trace repositories before calling
`call_epiverse_function`. The returned metadata makes it easy to map user
requests (for example “clean a linelist” versus “estimate Rt”) to the relevant
Epiverse package prior to execution. Keep the manifest lightweight—link out to
package READMEs or vignettes rather than embedding every repository's
documentation in the MCP assets.
