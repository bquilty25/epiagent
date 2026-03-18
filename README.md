# Epiagent Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A set of Claude Agent SDK skills for AI-powered epidemiological analysis using the Epiverse-TRACE R ecosystem.**

EpiAgent Skills gives Claude the ability to perform infectious disease epidemiology analyses — from outbreak simulation to publication-ready reports — by providing structured skill instructions grounded in the Epiverse-TRACE package ecosystem.

## What's in this repo

This repository contains only skills for the [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk). There is no standalone application code. The skills live in [`.agent/skills/`](.agent/skills/) and are loaded by Claude Code when working in this directory.

```
epiagent_skills/
└── .agent/skills/
    ├── epiverse_overview/   # Orchestrator for routing tasks
    ├── data_intake/         # Data cleaning and standardization
    ├── parameters/          # Epidemiological parameter management
    ├── simulation/          # Outbreak simulation
    ├── analysis/            # Statistical analysis (CFR, Rt, etc.)
    ├── visualisation/       # Publication-ready plots
    └── reporting/           # Publication-ready Quarto reports
```

## Skills

### [Epiverse Overview](.agent/skills/epiverse_overview/SKILL.md)
Orchestrator skill that routes tasks to the appropriate specialized skill. Start here for task planning.

### [Data Intake](.agent/skills/data_intake/SKILL.md)
Clean and standardize epidemiological data using `readepi`, `cleanepi`, `linelist`, and `numberize`.

### [Parameters](.agent/skills/parameters/SKILL.md)
Retrieve and manage epidemiological parameters (incubation periods, serial intervals) using `epiparameter` and `epiparameterDB`.

### [Simulation](.agent/skills/simulation/SKILL.md)
Generate synthetic outbreak data — line lists, contact data, transmission chains — using `simulist` and `epichains`.

### [Analysis](.agent/skills/analysis/SKILL.md)
Estimate CFR, Rt, final size, superspreading, and vaccine effectiveness using `cfr`, `finalsize`, `epidemics`, `superspreading`, and `vaccineff`.

### [Visualisation](.agent/skills/visualisation/SKILL.md)
Create publication-ready plots with the Epiverse-TRACE branded theme using `ggplot2` and `tracetheme`.

### [Reporting](.agent/skills/reporting/SKILL.md)
Generate publication-ready Quarto reports (HTML, PDF, Word) with standard academic structure.

## The Epiverse-TRACE Pipeline

Each skill maps to a stage in the epidemiology pipeline:

```
Data Intake → Parameters → Simulation → Analysis → Visualisation → Report
```

Skills can be used independently or chained together for end-to-end workflows.

## Setup

To use these skills, you need R (≥ 4.3.0) and the Epiverse-TRACE packages installed:

```r
options(repos = c(
  epiverse = "https://epiverse-trace.r-universe.dev",
  CRAN = "https://cloud.r-project.org"
))

install.packages("pacman")
pacman::p_load(
  simulist, cleanepi, linelist, cfr, epiparameter,
  finalsize, epidemics, superspreading, vaccineff, epichains,
  readepi, epiparameterDB, tracetheme, numberize,
  tidyverse, here, qs, ggplot2
)
```

Then clone this repository into your working directory so Claude Code can load the skills.

## License

MIT License — see [LICENSE](LICENSE) for details.

---

**Skills for [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk)** 
