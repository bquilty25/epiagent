# Model Context Protocol for Epiverse Agents

This document outlines how to expose Epiverse R functionality to a language-model
agent using a three-phase workflow:

1. **Tool curation and wrapping** – dynamically expose Epiverse Trace
   functionality to Python via `rpy2`.
2. **Tool manifest construction** – describe each wrapper using JSON schemas so
   the agent can understand their capabilities and argument requirements.
3. **Agentic workflow orchestration** – wire the tools into a Reason-Act loop so
   the agent can plan multi-step epidemiological analyses.

## Phase 1 – Tool curation and wrapping

* Use the Epiverse Trace catalogue maintained in
  [`docs/epiverse_packages.json`](epiverse_packages.json) to understand which
  repositories are currently available. Each entry now ships with the GitHub
  summary, topical tags and a coarse category (for example `r_package`,
  `training`, or `application`) so the agent can quickly shortlist suitable
  tooling. When refreshing from GitHub the registry will merge any new topics or
  descriptions into the local cache.
* Rather than building bespoke wrappers for each package, expose a generic
  entry point (see [`src/epiagent/tools/r_wrappers.py`](../src/epiagent/tools/r_wrappers.py))
  that can import any Epiverse Trace package, convert Python arguments into R
  objects, and return structured payloads for the agent. The exported
  `call_epiverse_function` helper supports positional and keyword arguments plus
  automatic pandas/R data-frame conversion.
* Retain defensive error handling so agents can recover gracefully and consider
  persisting artefacts (plots, RDS files) when needed for downstream tools.

## Phase 2 – Tool manifest

* Provide manifest entries for the generic wrappers (`list_epiverse_packages`
  and `call_epiverse_function`), including guidance on which packages exist and
  how to refresh the registry from GitHub. Surface the curated metadata in the
  manifest description so the model knows that `list_epiverse_packages`
  returns summaries, categories and topical tags that it can use to reason over
  which package to call next.
* The [`tool_manifest.json`](tool_manifest.json) file can be loaded into an
  agent framework (e.g. LangChain) to register the tools.
* Rich descriptions improve tool selection reliability; include domain context,
  expected data formats and defaults.
* **Do not attempt to inline every package manual.** The manifest should remain
  lightweight and focus on describing the wrapper surface. Package-specific
  context can be surfaced on demand by pointing the agent to upstream
  documentation URLs or pre-curated notes, while the registry keeps the full
  list of callable packages discoverable.

## Phase 3 – Agentic workflow

1. Accept user instructions and supporting data.
2. Let the agent deliberate over the manifest to select the next tool.
3. Execute the corresponding Python wrapper and capture the structured result.
4. Feed observations back to the agent so it can iterate, plan further actions
   and compose a final report with figures or tables.

### Operational guidance

* **Sandboxing** – package the environment in Docker with pinned R/epiverse
  dependencies.
* **Data privacy** – ensure PHI never leaves secure infrastructure.
* **Observability** – log tool invocations, inputs and outputs for auditing and
  debugging.
* **Prompting** – prime the agent with epidemiological expertise and highlight
  how to interpret tool responses.
* **Registry maintenance** – periodically run the `list_epiverse_packages`
  tool with `refresh=true` to pull new repositories from GitHub so that
  `call_epiverse_function` can access the latest Epiverse Trace utilities.
* **Documentation strategy** – reference upstream READMEs, vignettes or
  curated cheat-sheets instead of embedding the entire package documentation in
  the MCP artefacts. Summaries or links are sufficient for the agent to choose
  tools, and keep the protocol assets maintainable.
* **Package selection** – encourage the agent (via system prompt examples or
  additional documentation) to first call `list_epiverse_packages` and inspect
  the returned metadata before invoking a specific Epiverse function. The
  combination of package summaries, topical tags and categories provides enough
  signal for the model to map user requests (e.g. “estimate Rt from daily
  incidence”) to the correct package (such as `EpiEstim` or `incidence2`).

#### Example: choosing the right package

1. The agent receives: “Clean this linelist and build a quick contact chain
   view.”
2. It first calls `list_epiverse_packages` and filters for entries with the
   `r_package` category whose summaries mention “clean” or “contact”.
3. The metadata highlights `cleanepi` for linelist hygiene and `epichains` for
   transmission exploration, prompting a plan to run `call_epiverse_function`
   twice—once per package—before synthesising the response.
