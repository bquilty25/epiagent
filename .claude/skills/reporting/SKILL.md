---
name: reporting
description: Create publication-ready Quarto reports with standard academic structure incorporating all outbreak analysis results
---

# Reporting Skill: Publication-Ready Outbreak Analysis Reports

> [!IMPORTANT]
> **PRIMARY WORKFLOW**: When the user requests an analysis, create **ONE Quarto document** (`.qmd` file) that contains:
> - All code chunks for data cleaning, parameter retrieval, analysis, and visualization
> - Narrative text with inline R code explaining each step and presenting results
> - Standard academic structure (Background, Methods, Results, Discussion)
>
> **Do NOT create separate R scripts**. The Quarto document is both the analysis script AND the publication-ready report. When rendered, it executes all code and generates the final document.

> [!IMPORTANT]
> **Use the Introspection Protocol**: See [epiverse-overview](../epiverse-overview/SKILL.md) skill for the protocol when working with R packages.

## Overview

This skill provides guidance for creating a **single Quarto document** that contains the complete outbreak analysis workflow embedded within a standard academic report structure.

### The Complete Pipeline → Report

```
Data Intake → Parameters → Simulation/Analysis → Visualization → REPORT (end goal)
```

## Critical Style Guidelines

### 1. Inline R Code for Numbers (MANDATORY)

**ALWAYS use inline R code for any numbers in text.** Never hardcode numbers.

**Good**:
```markdown
The outbreak included `r nrow(linelist)` cases with CFR of `r sprintf("%.1f%%", cfr * 100)`
(95% CI: `r sprintf("%.1f%%", cfr_lower * 100)`–`r sprintf("%.1f%%", cfr_upper * 100)`).
```

**Bad**:
```markdown
The outbreak included 5,130 cases with CFR of 9.97% (95% CI: 9.2%–10.8%).
```

**Why**: Ensures numbers update automatically, prevents errors, maintains full reproducibility.

### 2. UK English Spelling (MANDATORY)

**ALWAYS use UK English spelling:**
- Analyse (not Analyze)
- Characterise (not Characterize)
- Centre (not Center)
- Colour (not Color)
- Programme (not Program, except "computer program")
- Standardise (not Standardize)
- Visualisation (not Visualization)

### 3. Collapsed Code for Detailed Methods

**Use `code-fold: true` for detailed methods code:**

```r
#| label: data-cleaning
#| code-fold: true
#| code-summary: "Show data cleaning code"

cleaned_data <- raw_data |>
  standardize_dates() |>
  remove_duplicates()
```

**When to use**:
- Data cleaning pipelines
- Complex statistical procedures
- Sensitivity analyses
- Diagnostic plots

**When NOT to use**:
- Setup chunks (use `echo: false`)
- Simple results display
- Final visualizations

## Standard Report Structure

### 1. Executive Summary
2-3 sentences summarizing key findings for stakeholders (~100-150 words)

### 2. Background
Disease context, outbreak setting, why analysis is needed (~300-500 words)

### 3. Objectives
Bulleted list of specific analysis questions

### 4. Data
Data sources, quality, sample size, completeness

### 5. Methods
- One subsection per major analysis component
- Use `code-fold: true` for detailed code
- Document packages and parameters

### 6. Results
- Present findings objectively
- Use inline R code for ALL numbers
- Cross-reference figures and tables

### 7. Discussion
- Interpret results in context
- Compare to literature
- Acknowledge limitations
- State implications

### 8. Conclusions
2-4 sentences with main takeaways

### 9. Computational Environment
- Session information
- Package versions
- Reproduction instructions

### 10. References
BibTeX citations for all sources

## Essential YAML Header

```yaml
---
title: "Analysis Title"
author: "Name / Organization"
date: today
format:
  html:
    toc: true
    toc-depth: 3
    code-fold: true
    code-tools: true
    embed-resources: true
    theme: cosmo
    fig-width: 8
    fig-height: 5
  pdf:
    toc: true
    number-sections: true
execute:
  echo: false
  warning: false
  message: false
bibliography: references.bib
---
```

## Chunk Options

```r
#| label: descriptive-name
#| echo: false              # Hide code, show output (default)
#| code-fold: true          # Show collapsed code (methods)
#| code-summary: "Show code"
#| fig-cap: "Figure caption"
#| fig-width: 8
#| fig-height: 5
#| tbl-cap: "Table caption"
```

## Setup Chunk Template

```r
#| label: setup
#| message: false
#| warning: false

# Configure repositories
options(repos = c(
  epiverse = "https://epiverse-trace.r-universe.dev",
  CRAN = "https://cloud.r-project.org"
))

# Core Epiverse-TRACE packages
library(simulist)
library(cleanepi)
library(linelist)
library(cfr)
library(epiparameter)

# Data manipulation and visualization
library(tidyverse)
library(here)
library(gt)
library(patchwork)

# Set reproducibility
set.seed(42)

# Create output directories
dir.create(here::here("outputs", "plots"), recursive = TRUE, showWarnings = FALSE)
dir.create(here::here("outputs", "tables"), recursive = TRUE, showWarnings = FALSE)
```

## Integrating Analysis Results

### Pattern: Analyze → Store → Display → Save

#### 1. Perform Analysis
```r
#| label: estimate-cfr
#| code-fold: true
#| code-summary: "Show CFR estimation code"

cfr_results <- cfr_rolling(
  data = cleaned_data,
  delay_density = delay_func
)

# Store for inline reporting
cfr_estimate <- cfr_results$severity_estimate
cfr_lower <- cfr_results$severity_low
cfr_upper <- cfr_results$severity_high
```

**In narrative (use inline R code)**:
```markdown
The estimated CFR was `r sprintf("%.1f%%", cfr_estimate * 100)`
(95% CI: `r sprintf("%.1f%%", cfr_lower * 100)`–`r sprintf("%.1f%%", cfr_upper * 100)`).
```

#### 2. Create Visualization
```r
#| label: plot-cfr
#| echo: false
#| fig-cap: "Rolling CFR estimates with 95% CI"
#| fig-width: 8
#| fig-height: 5

cfr_plot <- cfr_results |>
  ggplot(aes(x = date)) +
  geom_ribbon(aes(ymin = severity_low, ymax = severity_high),
              fill = "darkred", alpha = 0.2) +
  geom_line(aes(y = severity_estimate), color = "darkred") +
  scale_y_continuous(labels = scales::percent) +
  labs(title = "Rolling CFR Estimates", x = "Date", y = "CFR") +
  theme_minimal()

cfr_plot

# Save for external use
ggsave(here::here("outputs", "plots", "cfr_rolling.png"),
       cfr_plot, width = 8, height = 5, dpi = 300, bg = "white")
```

#### 3. Create Summary Table
```r
#| label: table-cfr
#| echo: false
#| tbl-cap: "CFR estimates with 95% CI"

tibble(
  Metric = c("Naive CFR", "Delay-corrected CFR", "Observation period"),
  Value = c(
    sprintf("%.1f%%", naive_cfr * 100),
    sprintf("%.1f%% (%.1f%% - %.1f%%)",
            cfr_estimate * 100, cfr_lower * 100, cfr_upper * 100),
    sprintf("%d days", outbreak_duration)
  )
) |>
  gt() |>
  tab_header(title = "CFR Estimation Results")
```

## Publication-Quality Figures

### Multi-Panel with Patchwork
```r
#| label: fig-combined
#| fig-cap: "Overview. (A) Epidemic curve. (B) Rolling CFR."
#| fig-width: 10
#| fig-height: 8

plot_a <- epicurve_plot + labs(tag = "A")
plot_b <- cfr_plot + labs(tag = "B")

combined <- plot_a / plot_b
combined

ggsave(here::here("outputs", "plots", "figure_combined.png"),
       combined, width = 10, height = 8, dpi = 300, bg = "white")
```

### Cross-Referencing
```markdown
As shown in @fig-combined, the outbreak peaked around day 45.
```

## Publication-Quality Tables

```r
#| label: tbl-summary
#| tbl-cap: "Outbreak summary statistics"

summary_stats <- tibble(
  Metric = c("Total Cases", "Total Deaths", "Attack Rate"),
  Value = c(
    format(total_cases, big.mark = ","),
    format(total_deaths, big.mark = ","),
    sprintf("%.1f%%", attack_rate * 100)
  )
)

summary_stats |>
  gt() |>
  tab_header(
    title = "Outbreak Summary",
    subtitle = sprintf("Period: %s to %s",
                      format(min_date, "%Y-%m-%d"),
                      format(max_date, "%Y-%m-%d"))
  )
```

## Citations

### BibTeX File (references.bib)
```bibtex
@article{barry2018outbreak,
  title={Outbreak of Ebola virus disease},
  author={Barry, Ahmadou and others},
  journal={The Lancet},
  year={2018}
}
```

### Citing in Text
```markdown
The delay-corrected CFR method [@barry2018outbreak] accounts for
right-censoring bias. All analyses used Epiverse-TRACE [@epiverse2024].
```

### Package Citations
```r
#| label: package-citations
#| echo: false

citation("cfr")
citation("simulist")
```

## Reproducibility Section

### Session Information
```r
#| label: session-info
#| echo: false

sessionInfo()
```

### Package Versions
```r
#| label: pkg-versions
#| tbl-cap: "Package versions"

key_packages <- c("simulist", "cleanepi", "cfr", "epiparameter")

tibble(
  Package = key_packages,
  Version = sapply(key_packages, function(pkg) {
    as.character(packageVersion(pkg))
  })
) |> gt()
```

### Reproduction Instructions
```markdown
## Reproducibility

**Requirements**: R ≥ 4.3.0, Quarto ≥ 1.3.0

**Steps**:
```bash
git clone https://github.com/your/repo.git
cd repo
quarto render analysis.qmd
```

**Random Seeds**: All operations use `set.seed(42)`

**Analysis Date**: `r format(Sys.time(), "%Y-%m-%d %H:%M:%S %Z")`
```

## Report Templates

### Quick Start
Use [ebola_analysis.qmd](../../../examples/ebola_outbreak/ebola_analysis.qmd) as template:

```bash
cp examples/ebola_outbreak/ebola_analysis.qmd my_analysis.qmd
cp examples/ebola_outbreak/references.bib my_references.bib
```

Then customize for your analysis.

## Rendering and Publishing

```bash
# HTML (self-contained)
quarto render analysis.qmd

# PDF (requires LaTeX)
quarto render analysis.qmd --to pdf

# Word
quarto render analysis.qmd --to docx

# Publish to GitHub Pages
quarto publish gh-pages analysis.qmd
```

## Common Patterns

### Pattern 1: Simulated Outbreak Report
- Background → Define disease
- Methods → Describe simulation parameters
- Results → Show dynamics
- Discussion → Compare to historical outbreaks

### Pattern 2: Real Data Analysis
- Background → Outbreak context
- Data → Sources and quality
- Methods → Cleaning and analysis
- Results → Estimates with uncertainty
- Discussion → Implications for response

### Pattern 3: Scenario Comparison
- Background → Decision context
- Methods → Scenarios tested
- Results → Comparative analysis
- Discussion → Recommendations

## Troubleshooting

### "Quarto not found"
```bash
brew install quarto  # macOS
# Or download from https://quarto.org/
```

### "Package not found"
```r
install.packages(c("gt", "knitr", "patchwork"))
```

### "Path errors"
```r
# Use here::here() for portable paths
source(here::here("R", "functions.R"))
```

### "Figures not showing"
- Check chunk produces output
- Verify fig-width and fig-height
- Use `echo: true` to debug

## Best Practices Checklist

- [ ] Title and metadata complete
- [ ] Executive summary clear
- [ ] All sections follow structure
- [ ] Code chunks have labels
- [ ] Figures have captions
- [ ] Tables formatted with gt
- [ ] **ALL numbers use inline R code**
- [ ] **UK English spelling throughout**
- [ ] **Detailed methods in collapsed chunks**
- [ ] Citations complete
- [ ] Session info included
- [ ] Renders without errors

## Integration with Other Skills

All skills are integrated **within the Quarto document**, not as separate scripts:

### Analysis in Quarto
```r
#| label: estimate-cfr
#| code-fold: true

# Use cfr package directly in code chunk
cfr_results <- cfr_rolling(
  data = cleaned_data,
  delay_density = delay_func
)

# Store values for inline reporting
cfr_estimate <- cfr_results$severity_estimate
```

Then use inline R code in narrative: `` The CFR was `r sprintf("%.1f%%", cfr_estimate * 100)`. ``

### Visualization in Quarto
```r
#| label: plot-epicurve
#| echo: false
#| fig-cap: "Epidemic curve"

# Create plot directly in code chunk
epicurve <- ggplot(cleaned_data, aes(x = date_onset)) +
  geom_histogram(binwidth = 7) +
  theme_trace()

epicurve  # Display plot inline
```

**Note**: Optionally save outputs with `ggsave()` or `write_csv()` for reuse, but the Quarto document should be self-contained and executable from start to finish.

## Summary

**When the user requests an analysis, create ONE Quarto document that:**

1. **Contains the complete workflow**: All data cleaning, parameter retrieval, analysis, and visualization code in code chunks
2. **Is executable**: Running `quarto render analysis.qmd` executes all code and generates the report
3. **Follows standard structure**: Executive summary → Background → Methods → Results → Discussion → Conclusion
4. **Is reproducible**: Seeds, versions, clear instructions embedded in the document
5. **Is publication-ready**: Professional figures, tables, inline R code for all numbers
6. **Is self-contained**: Single HTML/PDF file with everything needed

**Critical Requirements:**
- **ONE `.qmd` file** containing all code and narrative (not separate R scripts)
- Inline R code for ALL numbers (`` `r variable` ``)
- UK English spelling (analyse, characterise, visualisation)
- Collapsed code for detailed methods (`code-fold: true`)

**Remember**: The Quarto document is both the analysis script AND the final report. Review [ebola_analysis.qmd](../../../examples/ebola_outbreak/ebola_analysis.qmd) for a complete example.
