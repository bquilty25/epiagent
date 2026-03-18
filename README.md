# EpiAgent Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![R Version](https://img.shields.io/badge/R-%E2%89%A54.3.0-blue.svg)](https://www.r-project.org/)
[![Epiverse-TRACE](https://img.shields.io/badge/Epiverse-TRACE-9b59b6.svg)](https://epiverse-trace.github.io/)

**AI-powered epidemiological analysis skills for Claude using the Epiverse-TRACE R package ecosystem.**

EpiAgent Skills is a comprehensive skill pack that enables Claude AI agents to perform sophisticated infectious disease epidemiology analyses, from outbreak simulation to publication-ready reports.

📚 **New user?** Start with [GETTING_STARTED.md](GETTING_STARTED.md) for a comprehensive walkthrough.

## Features

- **Modular Skills Architecture**: 7 specialized skills covering the complete epidemiology pipeline
- **Introspection Protocol**: Built-in API verification to prevent hallucination
- **Production-Ready**: Reproducible workflows with comprehensive error handling
- **Epiverse-TRACE Integration**: Full support for 15+ epidemiological R packages
- **Publication Quality**: Standardized themes and visualization guidelines

## Quick Start

### Installation

1. **Install R** (≥ 4.3.0): [Download R](https://cran.r-project.org/)

2. **Install Epiverse-TRACE packages**:

```r
# Set up repositories
options(repos = c(
  epiverse = "https://epiverse-trace.r-universe.dev",
  CRAN = "https://cloud.r-project.org"
))

# Install core packages
install.packages("pacman")
pacman::p_load(
  simulist, cleanepi, linelist, cfr, epiparameter,
  tidyverse, here, qs, ggplot2, tracetheme
)
```

3. **Clone this repository**:

```bash
git clone https://github.com/your-username/epiagent_skills.git
cd epiagent_skills
```

### Run the Example Analysis

We provide a complete Ebola outbreak analysis as a reproducible Quarto document:

```bash
# Render the analysis
quarto render examples/ebola_outbreak/ebola_analysis.qmd

# Or open in RStudio and click "Render"
```

**What it does:**
1. Simulates an Ebola outbreak with realistic epidemiological parameters
2. Cleans and standardizes the data using Epiverse-TRACE tools
3. Estimates case fatality risk (CFR) with delay correction
4. Generates publication-ready epidemic curves and CFR plots
5. Produces a comprehensive HTML report with embedded results

**Outputs:**
- HTML Report: `examples/ebola_outbreak/ebola_analysis.html`
- Processed data: [data/processed/](data/processed/)
- Plots: [outputs/plots/](outputs/plots/) (epicurve.png, cfr_rolling.png)
- Tables: [outputs/tables/](outputs/tables/) (cfr_rolling_estimates.csv)

See [examples/README.md](examples/README.md) for more details.

## Repository Structure

```
epiagent_skills/
├── .agent/skills/              # Claude Agent SDK skills
│   ├── epiverse_overview/      # Orchestrator for routing tasks
│   ├── data_intake/            # Data cleaning and standardization
│   ├── parameters/             # Epidemiological parameter management
│   ├── simulation/             # Outbreak simulation
│   ├── analysis/               # Statistical analysis (CFR, R0, etc.)
│   ├── visualisation/          # Publication-ready plots
│   └── reporting/              # Publication-ready Quarto reports
├── examples/                   # Example analyses (Quarto documents)
│   └── ebola_outbreak/         # Ebola outbreak analysis demo
├── R/                          # Reusable workflow functions
│   └── workflow_functions.R    # Modular pipeline functions
├── registry.json               # Package metadata registry
├── data/                       # Data files
│   ├── raw/                    # Simulated raw data
│   └── processed/              # Cleaned, processed data
└── outputs/                    # Generated outputs
    ├── plots/                  # Visualizations (PNG)
    └── tables/                 # Analysis results (CSV)
```

## Skills Overview

### 1. [Epiverse Overview](.agent/skills/epiverse_overview/SKILL.md)
**Orchestrator skill** for routing tasks to the appropriate specialized skill. Start here for task planning.

### 2. [Data Intake](.agent/skills/data_intake/SKILL.md)
Clean and standardize epidemiological data using `readepi`, `cleanepi`, `linelist`, and `numberize`.

**Key capabilities:**
- Import from HIS databases (DHIS2, SORMAS, SQL)
- Clean messy data (duplicates, date formats, missing values)
- Tag and validate linelist data
- Convert numeric words to digits

### 3. [Parameters](.agent/skills/parameters/SKILL.md)
Retrieve and manage epidemiological parameters using `epiparameter` and `epiparameterDB`.

**Key capabilities:**
- Access library of epidemiological parameters from literature
- Convert between parameter representations (mean/SD → distribution parameters)
- Extract parameters from summary statistics
- Plot parameter distributions

### 4. [Simulation](.agent/skills/simulation/SKILL.md)
Generate synthetic outbreak data using `simulist` and `epichains`.

**Key capabilities:**
- Simulate realistic line lists and contact data
- Branching process simulations for transmission chains
- Age-structured populations
- Time-varying case fatality risk

### 5. [Analysis](.agent/skills/analysis/SKILL.md)
Estimate disease severity, transmissibility, and outbreak dynamics using `cfr`, `finalsize`, `epidemics`, `superspreading`, and `vaccineff`.

**Key capabilities:**
- Case fatality risk (CFR) estimation with delay correction
- Final outbreak size prediction
- Compartmental epidemic modeling (SIR/SEIR)
- Superspreading analysis
- Vaccine effectiveness estimation

### 6. [Visualisation](.agent/skills/visualisation/SKILL.md)
Create publication-ready plots using `tracetheme` and `ggplot2`.

**Key capabilities:**
- Epiverse-TRACE branded theme
- Epidemic curves
- Time series with confidence intervals
- Colorblind-safe palettes

### 7. [Reporting](.agent/skills/reporting/SKILL.md)
Generate publication-ready Quarto reports with standard academic structure.

**Key capabilities:**
- Standard academic format (intro, methods, results, discussion, conclusion)
- Integration of all analysis results, figures, and tables
- Reproducibility documentation (session info, package versions)
- Multiple output formats (HTML, PDF, Word)
- BibTeX citation management

## The Epiverse-TRACE Pipeline

EpiAgent Skills follows the **6-stage epidemiology pipeline**, with reporting as the **end goal**:

```
Data Intake → Parameters → Simulation → Analysis → Visualization → REPORT
```

> **Start with the end in mind**: Every step should be executed with the final publication-ready report in mind.

Each skill can be used independently or chained together for complete workflows.

## Key Concepts

### Introspection Protocol

All skills implement a **critical introspection protocol** that requires agents to verify APIs before generating code:

1. List available functions: `ls("package:pkg_name")`
2. Read README: `system.file("README.md", package = "pkg_name")`
3. Check vignettes: `vignette(package = "pkg_name")`
4. Verify signatures: `args(function_name)`
5. Read documentation: `tools::Rd2txt(...)`

This prevents hallucination and ensures generated code matches actual package APIs.

### Code Conventions

All code follows these standards:
- **Style**: tidyverse (snake_case, `|>` pipe operator)
- **Paths**: `here::here()` for portability
- **Reproducibility**: `set.seed()` for stochastic operations
- **Dates**: ISO 8601 format (YYYY-MM-DD)
- **Visualization**: `ggplot2` with `tracetheme::theme_trace()`

## Example Use Cases

### Case 1: Simulate and Analyze an Outbreak

```r
# 1. Simulate outbreak (simulation skill)
outbreak <- simulist::sim_outbreak(
  contact_distribution = contact_dist,
  infectious_period = infectious_dist,
  outbreak_size = c(100, 500)
)

# 2. Clean data (data_intake skill)
cleaned <- cleanepi::clean_data(outbreak$linelist)

# 3. Analyze CFR (analysis skill)
cfr_est <- cfr::cfr_static(data = cleaned, delay_density = delay_func)

# 4. Visualize (visualisation skill)
ggplot(cleaned, aes(x = date_onset)) +
  geom_histogram() +
  tracetheme::theme_trace()
```

### Case 2: Retrieve Parameters from Literature

```r
# Get Ebola incubation period (parameters skill)
ebola_incub <- epiparameter::epiparameter_db(
  disease = "Ebola Virus Disease",
  epi_name = "incubation period"
)

# Extract distribution for use in simulation
incub_dist <- epiparameter::get_distribution(ebola_incub)
```

### Case 3: Estimate Vaccine Effectiveness

```r
# Analyze vaccine effectiveness (analysis skill)
ve <- vaccineff::estimate_ve(
  data = cohort_data,
  outcome = "infection",
  vaccine = "dose1_date"
)
```

## Package Registry

The [registry.json](registry.json) file contains metadata for 15 Epiverse-TRACE packages:

**Core Analysis**: simulist, cleanepi, linelist, cfr, epiparameter, finalsize
**Advanced Modeling**: epidemics, superspreading, vaccineff, epichains
**Data & Utilities**: readepi, epiparameterDB, tracetheme, numberize

Each entry includes exported functions, vignettes, and documentation links.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:
- How to add new skills
- Code style guidelines
- Testing requirements
- Documentation standards

## Documentation

- **Skills Documentation**: See [`.agent/skills/`](.agent/skills/) for detailed skill documentation
- **Architecture**: See [ARCHITECTURE.md](ARCHITECTURE.md) for system design
- **Changelog**: See [CHANGELOG.md](CHANGELOG.md) for version history
- **Epiverse-TRACE**: Visit [epiverse-trace.github.io](https://epiverse-trace.github.io/) for package documentation

## Citation

If you use EpiAgent Skills in your work, please cite the Epiverse-TRACE packages:

```bibtex
@misc{epiverse2024,
  title = {Epiverse-TRACE: Tools for outbreak analytics},
  author = {{Epiverse-TRACE Development Team}},
  year = {2024},
  url = {https://epiverse-trace.github.io/}
}
```

## License

MIT License - see [LICENSE](LICENSE) for details.

This project builds upon the Epiverse-TRACE ecosystem, which is supported by data.org and developed by the Centre for the Mathematical Modelling of Infectious Diseases at the London School of Hygiene & Tropical Medicine.

## Support

- **Issues**: Report bugs or request features via GitHub Issues
- **Discussions**: Join the Epiverse-TRACE community discussions
- **Documentation**: Check package-specific documentation at pkgdown sites

---

**Built with [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk)** | **Powered by [Epiverse-TRACE](https://epiverse-trace.github.io/)**
