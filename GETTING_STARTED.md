# Getting Started with EpiAgent Skills

## Quick Start: Your First Analysis Report

The goal of EpiAgent Skills is to help you produce **publication-ready outbreak analysis reports**. This guide walks you through creating your first report from start to finish.

### Prerequisites

1. **R** ≥ 4.3.0 ([Download](https://cran.r-project.org/))
2. **Quarto** ≥ 1.3.0 ([Download](https://quarto.org/docs/get-started/))
3. **Claude Code** CLI ([Download](https://claude.ai/download))

### Step 1: Install Epiverse-TRACE Packages

```r
# Configure repositories
options(repos = c(
  epiverse = "https://epiverse-trace.r-universe.dev",
  CRAN = "https://cloud.r-project.org"
))

# Install core packages
install.packages(c(
  "simulist", "cleanepi", "linelist", "cfr", "epiparameter",
  "tidyverse", "here", "qs", "gt", "knitr", "quarto"
))
```

### Step 2: Clone and Explore the Repository

```bash
git clone https://github.com/your-username/epiagent_skills.git
cd epiagent_skills

# Explore the structure
ls -R .agent/skills/    # 7 specialized skills
ls examples/            # Example analyses
```

### Step 3: Run the Example Report

The fastest way to understand the workflow is to render the included Ebola outbreak analysis:

```bash
# Render the example
quarto render examples/ebola_outbreak/ebola_analysis.qmd

# Open the HTML report
open examples/ebola_outbreak/ebola_analysis.html
```

This will:
1. ✅ Simulate an Ebola outbreak (300+ cases)
2. ✅ Clean and validate the data
3. ✅ Estimate CFR with delay correction
4. ✅ Generate epidemic curves and CFR plots
5. ✅ Produce a comprehensive 50+ page HTML report

**Time**: ~30 seconds

### Step 4: Understand the Report Structure

Open [examples/ebola_outbreak/ebola_analysis.qmd](examples/ebola_outbreak/ebola_analysis.qmd) to see:

```markdown
---
title: "Ebola Outbreak Simulation and Analysis"
format:
  html:
    toc: true
    embed-resources: true
---

## Executive Summary
[Key findings in 2-3 sentences]

## Background
[Disease context and motivation]

## Methods
```{r}
# Load packages
library(simulist)
library(cfr)
# ... analysis code
```

## Results
[Figures and tables with interpretation]

## Discussion
[Interpretation and implications]

## Conclusions
[Brief summary]
```

This is the **standard structure** for all outbreak analysis reports.

## Understanding the Skills Pipeline

Every analysis follows the same pipeline, with **reporting as the end goal**:

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Data Intake  │ -> │  Parameters  │ -> │  Simulation  │
│              │    │              │    │              │
│ Clean data   │    │ Get epi      │    │ Generate     │
│ Validate     │    │ parameters   │    │ outbreak     │
└──────────────┘    └──────────────┘    └──────────────┘
                                                ↓
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│    REPORT    │ <- │Visualization │ <- │   Analysis   │
│              │    │              │    │              │
│ Publication  │    │ Create plots │    │ Estimate CFR │
│ ready output │    │ Format tables│    │ Calculate Rt │
└──────────────┘    └──────────────┘    └──────────────┘
```

**Key insight**: Each step prepares results for the final report. Always ask: *"How will this appear in my report?"*

## Creating Your Own Analysis

### Option 1: Using Claude Code (Recommended for Beginners)

Start Claude Code in the repository:

```bash
cd epiagent_skills
claude-code
```

Then use natural language:

```
You: "I want to analyze a measles outbreak. Create a report template for me."

Claude: [Uses reporting skill]
        [Creates examples/measles_analysis/measles_analysis.qmd]
        [Customizes template for measles parameters]

You: "Fill in the analysis with simulated data"

Claude: [Uses simulation skill to get parameters]
        [Uses simulation skill to generate outbreak]
        [Uses analysis skill to estimate metrics]
        [Populates the report template]

You: "Render the report"

Claude: [Runs: quarto render examples/measles_analysis/measles_analysis.qmd]
        [Opens HTML output]
```

**Result**: Complete publication-ready report without writing code yourself.

### Option 2: Using the Template (For R Users)

Copy and customize the example:

```bash
# Create your analysis directory
mkdir -p examples/my_analysis

# Copy the template
cp examples/ebola_outbreak/ebola_analysis.qmd \
   examples/my_analysis/my_analysis.qmd

cp examples/ebola_outbreak/references.bib \
   examples/my_analysis/references.bib
```

Edit `my_analysis.qmd`:

1. **Change title and metadata** (lines 1-30)
2. **Update disease parameters** (methods section)
3. **Modify analysis** (results section)
4. **Interpret findings** (discussion section)

Render:

```bash
quarto render examples/my_analysis/my_analysis.qmd
```

### Option 3: Using Workflow Functions (For Advanced Users)

The modular functions in [R/workflow_functions.R](R/workflow_functions.R) can be used independently:

```r
source(here::here("R", "workflow_functions.R"))

# 1. Setup parameters
params <- setup_ebola_parameters()

# 2. Simulate outbreak
outbreak <- simulate_ebola_outbreak(params, outbreak_size = c(200, 400))

# 3. Clean data
cleaned <- clean_outbreak_data(outbreak$linelist)

# 4. Estimate CFR
cfr <- estimate_cfr(cleaned)

# 5. Visualize
plots <- create_visualizations(cleaned, cfr$rolling)
plots$epicurve
plots$cfr

# 6. Create your report incorporating these results
```

## Working with Real Data

If you have real outbreak data instead of simulated data:

### Step 1: Load Your Data

```r
# Read your line list
library(readr)
raw_data <- read_csv(here::here("data", "raw", "my_outbreak.csv"))
```

### Step 2: Clean with Data Intake Skill

Ask Claude:

```
"Clean this outbreak data using the data_intake skill.
 The date columns are: onset_date, report_date, outcome_date.
 Check for duplicates and missing values."
```

Claude will use the data_intake skill to generate:

```r
library(cleanepi)
library(linelist)

cleaned_data <- cleanepi::clean_data(
  data = raw_data,
  standardize_column_names = list(keep = NULL),
  replace_missing_values = list(
    target_columns = NULL,
    na_strings = c("", "NA", "unknown", "missing")
  )
) |>
  linelist::make_linelist(
    date_onset = "onset_date",
    date_reporting = "report_date",
    date_outcome = "outcome_date",
    outcome = "outcome_status"
  )
```

### Step 3: Proceed with Analysis

Once cleaned, follow the same pipeline:

```
Cleaned data → Get parameters → Analyze → Visualize → Report
```

## Common Workflows

### Workflow 1: Simulated Outbreak Study

**Use case**: Test methods, plan surveillance, training

1. Define parameters (parameters skill)
2. Simulate outbreak (simulation skill)
3. Clean data (data_intake skill)
4. Analyze (analysis skill)
5. Create report (reporting skill)

**Example**: The included [ebola_analysis.qmd](examples/ebola_outbreak/ebola_analysis.qmd)

### Workflow 2: Real Outbreak Analysis

**Use case**: Response to ongoing outbreak

1. Import real data
2. Clean and validate (data_intake skill)
3. Get disease parameters (parameters skill)
4. Estimate severity/transmissibility (analysis skill)
5. Create visualizations (visualisation skill)
6. Generate report (reporting skill)

### Workflow 3: Scenario Comparison

**Use case**: Evaluate intervention strategies

1. Setup base outbreak parameters
2. Simulate multiple scenarios (simulation skill)
3. Analyze each scenario (analysis skill)
4. Compare results (visualisation skill)
5. Synthesize findings (reporting skill)

### Workflow 4: Methods Validation

**Use case**: Test new analytical methods

1. Simulate ground truth outbreak
2. Apply multiple estimation methods (analysis skill)
3. Compare performance
4. Document results (reporting skill)

## The 7 Skills Explained

### 1. Epiverse Overview
**Purpose**: Orchestrates the other skills
**When to use**: Starting any analysis, need routing guidance
**Key feature**: Decision trees and workflow templates

### 2. Data Intake
**Purpose**: Clean and standardize epidemiological data
**When to use**: Have messy real-world data
**Key packages**: cleanepi, linelist, readepi

### 3. Parameters
**Purpose**: Get and manage epidemiological parameters
**When to use**: Need disease-specific parameters (R0, incubation, etc.)
**Key packages**: epiparameter, epiparameterDB

### 4. Simulation
**Purpose**: Generate synthetic outbreak data
**When to use**: Need test data, exploring scenarios
**Key packages**: simulist, epichains

### 5. Analysis
**Purpose**: Estimate disease severity and transmission
**When to use**: Have outbreak data, need estimates
**Key packages**: cfr, finalsize, epidemics

### 6. Visualisation
**Purpose**: Create publication-ready plots
**When to use**: Need to visualize results
**Key packages**: tracetheme, ggplot2

### 7. Reporting
**Purpose**: Generate comprehensive analysis reports
**When to use**: Ready to synthesize all results (ALWAYS the end goal)
**Key packages**: quarto, knitr, gt

## Best Practices

### 1. Start with the End in Mind

Before starting analysis, review the [reporting skill](.agent/skills/reporting/SKILL.md) to understand the final report structure. This ensures you collect the right information at each step.

### 2. Use the Introspection Protocol

The skills implement a protocol that verifies package APIs before generating code. This prevents errors from outdated training data.

**What it does:**
- Reads current package documentation
- Verifies function signatures
- Checks available vignettes
- Ensures code matches actual API

**You don't need to do anything** - Claude handles this automatically when using the skills.

### 3. Follow Code Conventions

All generated code follows these standards:

```r
# ✅ Good practices
set.seed(42)                                    # Reproducibility
file_path <- here::here("data", "raw", "data.csv")  # Portable paths
start_date <- as.Date("2024-01-01")            # ISO 8601 dates
result <- data |> filter(complete.cases())     # Native pipe
```

```r
# ❌ Avoid
# No seed = non-reproducible
file_path <- "/Users/you/data.csv"             # Absolute paths
start_date <- "1/1/2024"                       # Ambiguous dates
result <- data %>% filter(complete.cases())    # Magrittr pipe
```

### 4. Document Everything

Include in every analysis:

- Random seeds used
- Package versions (`sessionInfo()`)
- Parameter sources and justifications
- Data quality assessment
- Limitations and assumptions

The [reporting skill](.agent/skills/reporting/SKILL.md) ensures these are captured automatically.

### 5. Save Intermediate Results

```r
# Save processed data
qsave(cleaned_data, here::here("data", "processed", "cleaned.qs"))

# Save analysis results
write_csv(cfr_estimates, here::here("outputs", "tables", "cfr.csv"))

# Save plots
ggsave(here::here("outputs", "plots", "epicurve.png"),
       plot = epicurve, width = 8, height = 5, dpi = 300)
```

This allows:
- Reproducibility verification
- Sharing with collaborators
- Integration into reports

## Troubleshooting

### "Package not found"

```r
# Install missing packages
options(repos = c(
  epiverse = "https://epiverse-trace.r-universe.dev",
  CRAN = "https://cloud.r-project.org"
))
install.packages("package_name")
```

### "Quarto command not found"

```bash
# macOS
brew install quarto

# Or download from https://quarto.org/
```

### "Error in source(): cannot open the connection"

Make sure you're using `here::here()` for paths:

```r
# In Quarto documents rendered from examples/
source(here::here("..", "..", "R", "workflow_functions.R"))

# From repository root
source(here::here("R", "workflow_functions.R"))
```

### Report Rendering Fails

1. Check R version: `R.version.string` (need ≥ 4.3.0)
2. Update packages: `update.packages(ask = FALSE)`
3. Clear cache: `rm -rf _cache/`
4. Check for errors in code chunks (set `echo: true` to debug)

## Next Steps

### Learn by Example

1. **Read** [examples/ebola_outbreak/ebola_analysis.qmd](examples/ebola_outbreak/ebola_analysis.qmd)
2. **Modify** parameters and re-render
3. **Create** your own analysis using the template

### Explore the Skills

Read the skill documentation to understand capabilities:

- [Epiverse Overview](.agent/skills/epiverse_overview/SKILL.md) - Start here
- [Reporting](.agent/skills/reporting/SKILL.md) - Understand the end goal
- [Analysis](.agent/skills/analysis/SKILL.md) - Learn estimation methods
- [Visualisation](.agent/skills/visualisation/SKILL.md) - Publication plots

### Use with Claude

Start a conversation with Claude Code:

```bash
cd epiagent_skills
claude-code
```

Try these prompts:

```
"Explain the epiverse_overview skill"
"Create a new analysis for a COVID-19 outbreak"
"Help me estimate CFR from my outbreak data"
"Generate a report comparing two intervention scenarios"
```

### Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- How to add new skills
- Code standards
- Documentation requirements
- Pull request process

## Additional Resources

### Epiverse-TRACE

- **Main site**: [epiverse-trace.github.io](https://epiverse-trace.github.io/)
- **Package list**: [packages.html](https://epiverse-trace.github.io/packages.html)
- **Tutorials**: [tutorials.html](https://epiverse-trace.github.io/tutorials.html)

### Quarto

- **Guide**: [quarto.org/docs/guide/](https://quarto.org/docs/guide/)
- **R integration**: [quarto.org/docs/computations/r.html](https://quarto.org/docs/computations/r.html)
- **Publishing**: [quarto.org/docs/publishing/](https://quarto.org/docs/publishing/)

### Claude Agent SDK

- **Documentation**: [docs.anthropic.com](https://docs.anthropic.com/)
- **Skills guide**: Learn about creating custom skills

---

## Summary

**The EpiAgent Skills workflow in 3 steps:**

1. **Talk to Claude**: Describe what you want to analyze
2. **Let Skills Guide**: Claude uses skills to generate correct code
3. **Get Your Report**: Receive publication-ready analysis

**Key principle**: Start with the report in mind. Every analysis step contributes to the final deliverable.

**Get started now:**

```bash
cd epiagent_skills
quarto render examples/ebola_outbreak/ebola_analysis.qmd
```

Welcome to reproducible outbreak analytics! 🦠📊
