---
name: epiverse-overview
description: Master orchestrator for Epiverse-TRACE infectious disease epidemiology skills. Use this skill FIRST to understand the ecosystem and route tasks to the correct specialized skill.
---

# Epiverse-TRACE Overview & Orchestrator

> [!IMPORTANT]
> **CRITICAL: The Introspection Protocol**
> Before generating any analysis code using these packages, you MUST execute the following discovery commands in R to verify the API and available data. Do NOT rely on your training data, as package versions and functions may have changed.
>
> 1. **List Functions & Reference**: Run `ls("package:pkg_name")` and `help(package = "pkg_name")` to see what functions exist and read the index.
> 2. **Read README**: Run `try(print(readLines(system.file("README.md", package = "pkg_name"))))` to understand the package scope and basic usage.
> 3. **Check Vignettes**: Run `vignette(package = "pkg_name")` to list available vignettes. Then read relevant vignettes using `vignette("vignette_name", package = "pkg_name")` to see standard workflows.
> 4. **Read Signatures**: Run `args(function_name)` or `str(function_name)` on the specific functions you plan to use.
> 5. **Check Documentation**: Read the internal help file using `tools::Rd2txt(utils::.getHelpFile(utils::help("function_name", package = "pkg_name")))`.
>
> **Only after confirming the function signatures, reading the documentation, and understanding the workflows should you generate the final R code.**

## The Epiverse-TRACE Philosophy

Epiverse-TRACE provides a pipeline for outbreak analytics:

1. **Data Intake** → Reading data from HIS and cleaning it
2. **Parameters** → Retrieving epidemiological parameters from literature
3. **Simulation** → Generating synthetic data for testing
4. **Analysis** → Estimating severity, transmissibility, and other metrics
5. **Visualisation** → Creating standardised, publication-ready plots
6. **Reporting** → Synthesizing results into publication-ready documents

> [!IMPORTANT]
> **START WITH THE END IN MIND**: The goal is always a **single Quarto document** containing the complete workflow. When the user asks for an analysis, create ONE `.qmd` file that includes all code chunks for data cleaning, parameter retrieval, analysis, and visualization, with narrative text explaining each step. Do not create separate R scripts - embed everything in the Quarto document.

## Skill Routing Guide

| User Goal | Relevant Packages | Target Skill |
|-----------|-------------------|--------------|
| Clean/standardize data | `cleanepi`, `linelist`, `readepi` | `data-intake` |
| Get epidemiological parameters | `epiparameter`, `epiparameterDB` | `parameters` |
| Simulate outbreak/contacts | `simulist`, `epichains` | `simulation` |
| Estimate CFR/Rt/final size | `cfr`, `finalsize`, `epidemics` | `analysis` |
| Create plots with Epiverse theme | `tracetheme`, `ggplot2` | `visualisation` |
| Generate publication report | Quarto, `gt`, `knitr` | `reporting` |

## Skill Dependencies

```
data_intake → parameters → simulation/analysis → visualisation → REPORT (end goal)
```

**Pipeline Flow**: All skills ultimately feed into `reporting`, which is the final deliverable.

## Common Task Mappings

| User Goal | Primary Skill | Notes |
|-----------|--------------|-------|
| Clean messy line list | data-intake | - |
| Estimate outbreak severity | analysis | Requires cleaned data from data-intake |
| Compare interventions | analysis | Use epidemics package |
| Create epidemic curve | visualisation | Use cleaned data |
| Generate test data | simulation | Use parameters for realism |
| Find disease parameters | parameters | - |
| Complete outbreak analysis | epiverse-overview | Chain all skills → reporting |

## General Conventions

- **Style**: Use tidyverse style (snake_case, `|>`)
- **Paths**: Use `here::here()` for all file paths
- **Reproducibility**: Set seeds (`set.seed()`) for stochastic operations
- **Dates**: Always use ISO 8601 (YYYY-MM-DD)
- **Visualisation**: Use `ggplot2` with `tracetheme::theme_trace()`

## Decision Tree

```
┌─ User Request ─┐
│                │
├─ "Clean/Import data" ────────────► data-intake skill
│
├─ "Get parameters" ───────────────► parameters skill
│
├─ "Simulate outbreak" ────────────► simulation skill
│
├─ "Estimate CFR/Rt/Final Size" ──► analysis skill
│
├─ "Create plot" ──────────────────► visualisation skill
│
├─ "Generate report" ──────────────► reporting skill
│
└─ "Complete analysis" ────────────► Use pipeline (multiple skills) → REPORT
```

> [!NOTE]
> **The Default Goal**: Unless the user explicitly says otherwise, assume they want a **complete publication-ready report** as the final deliverable.
