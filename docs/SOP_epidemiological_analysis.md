# Standard Operating Procedure: Agentic Epidemiological Analysis with Epiverse

## 1. Objective and Principles

This SOP defines the protocol for AI agents (the "Analyst") to conduct epidemiological analyses using the Epiverse-TRACE ecosystem.

**Core Principles:**
1.  **Reproducibility**: All analyses must be fully reproducible from raw data to final report.
2.  **Epistemic Awareness**: Uncertainty must be quantified and communicated at every step (parameter, model, and data uncertainty).
3.  **Epiverse-First**: Prioritise validated Epiverse-TRACE packages over ad-hoc code.
4.  **Provenance**: All parameters and data must have explicit citations.

## 2. Analysis Workflow

### Phase 1: Task Decomposition & Tool Discovery

**Protocol:**
1.  **Semantic Search**: Do not guess package names. Use `find_relevant_packages(query)` to map the user's natural language request to specific Epiverse tools.
    *   *Example*: "Estimate Rt from incidence" -> `EpiNow2`, `incidence2`
    *   *Example*: "Find incubation period for MERS" -> `epiparameter`
2.  **Package Verification**: If a package is unknown to the Analyst, use `list_epiverse_packages()` to verify availability and `ingest_git_repo()` (if necessary and authorised) to understand its API.

### Phase 2: Data Acquisition & Parameterisation

**Protocol:**
1.  **Parameter Retrieval**: Use `call_epiverse_function("epiparameter", "epiparameter_db", ...)` to retrieve epidemiological parameters.
    *   **CRITICAL**: Never hardcode parameters (e.g., "mean=5.2"). Always fetch distribution objects.
    *   **Selection**: If multiple studies exist, select the most relevant based on context (e.g., matching virus variant or geographic region) or pool them if appropriate to reflect uncertainty.
2.  **Citation**: Record the citation/DOI for every parameter used.

### Phase 3: Analytical Execution

**Protocol:**
1.  **Environment**: All code must be valid R code, compatible with the user's environment.
2.  **Coding Standards**:
    *   **Style**: Use `tidyverse` style for data manipulation (readability).
    *   **Vectorisation**: Use vectorised functions over loops for performance.
    *   **Piping**: Use the base pipe `|>` or magrittr `%>%` consistently.
3.  **Handling Uncertainty**:
    *   **Distributions**: Pass `epiparameter` distribution objects directly to downstream functions where supported.
    *   **Bootstrapping**: When estimating metrics (e.g., CFR), use bootstrapping or Bayesian methods to generate Confidence/Credible Intervals (CIs).
    *   **Propagation**: Ensure CIs are propagated through the analysis (e.g., if Rt is uncertain, the projection must show the confidence ribbon).

### Phase 4: Reporting & Output

**Protocol:**
1.  **Format**: The final output **MUST** be a Quarto (`.qmd`) document.
2.  **Reproducible Rendering**:
    *   Use inline R code (`` `r mean(x)` ``) for all reported numbers to ensure text matches results.
    *   Set global chunk options: `knitr::opts_chunk$set(echo = TRUE, warning = FALSE, message = FALSE)`.
3.  **Structure**:
    *   **YAML Header**: Include title, author, date, and output format (html/pdf/docx).
    *   **Introduction**: Research question and data sources.
    *   **Methods**: Specific Epiverse packages used (with citations).
    *   **Results**: Tables and Figures with captions. Uncertainty intervals must be explicitly stated (e.g., "CFR: 12% [95% CrI: 10-14%]") and visualised (error bars/ribbons).
    *   **References**: Automatically generated bibliography.

## 3. Example Agent Prompt / Behaviour

When receiving a request like *"Analyse this MERS outbreak data"*, the Analyst shall:

1.  **Plan**: "I will use `readepi` to load data, `cleanepi` to standardise it, `epiparameter` to get the serial interval for MERS, and `EpiNow2` to estimate Rt."
2.  **Execute Tools**:
    *   `find_relevant_packages("clean data")` -> `cleanepi`
    *   `call_epiverse_function("epiparameter", "epiparameter_db", kwargs={"disease": "MERS", "epi_name": "serial interval"})`
3.  **Write Code**: Generate the `.qmd` file content.

## 4. Checklist for Quality Assurance

- [ ] Are all external R packages declared?
- [ ] Is every parameter source cited?
- [ ] Is uncertainty shown for key estimates (Rt, CFR, projections)?
- [ ] Does the code run without errors in a clean session?
- [ ] Are Epiverse packages used where applicable instead of custom implementations?
