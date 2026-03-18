---
name: analysis
description: Skill for analysing outbreaks: estimating severity (CFR), transmissibility (Rt), final size, superspreading, and vaccine effectiveness.
---

# Epiverse-TRACE Analysis

> [!IMPORTANT]
> **Use the Introspection Protocol**: See [epiverse-overview](../epiverse-overview/SKILL.md) skill for the protocol. Before generating code, verify package APIs and functions using R introspection commands.

> [!NOTE]
> **Workflow Context**: This skill's code should be included in **Quarto document code chunks** (not separate R scripts). See the [reporting](../reporting/SKILL.md) skill for the complete workflow structure.

This skill provides tools for analyzing outbreak data to estimate key epidemiological metrics.

## Packages

### `cfr`
**Purpose**: Estimate disease severity and case ascertainment with delay correction.

**Key Functions**:
- `cfr_static()`: Estimate overall CFR for an outbreak
- `cfr_rolling()`: Estimate time-varying CFR
- `cfr_time_varying()`: Estimate CFR with temporal changes

**Key Features**: Accounts for delay from onset to death, provides corrected and naive estimates

### `finalsize`
**Purpose**: Calculate the final size of an epidemic in heterogeneous populations.

**Key Functions**:
- `final_size()`: Calculate epidemic final size given R0
- `r_eff()`: Calculate effective reproduction number

**Key Features**: Handles age-structured populations, contact matrices, heterogeneous susceptibility

### `superspreading`
**Purpose**: Estimate individual-level variation in transmission.

**Key Functions**:
- `probability_epidemic()`: Calculate probability outbreak becomes epidemic
- `probability_extinct()`: Calculate probability of extinction
- `proportion_cluster_size()`: Proportion of transmission in clusters
- `proportion_transmission()`: Proportion causing X% of transmission

**Key Features**: Fits offspring distributions (negative binomial, Poisson-lognormal), estimates R and k

### `epidemics`
**Purpose**: Composable epidemic scenario modelling.

**Key Functions**:
- `model_default()`: SEIR-V model with interventions
- `population()`: Create population structure
- `intervention()`: Define contact reduction or vaccination
- `model_ebola()`: Stochastic Ebola model
- `model_vacamole()`: COVID-19 vaccination model

**Key Features**: Contact matrices, age-stratified risks, time-varying parameters, interventions

### `vaccineff`
**Purpose**: Estimate vaccine effectiveness from cohort and case-control studies.

**Key Functions**:
- `make_vaccineff_data()`: Prepare data for VE estimation
- `estimate_vaccineff()`: Estimate VE using Cox regression
- `plot()`: Visualize VE results (log-log plots, survival curves)
- `summary()`: Get VE estimates with confidence intervals

**Key Features**: Handles cohort design, matching, immunization delays, time-varying effects

## Typical Workflow

### Severity Analysis
1. Prepare line list with `linelist` package
2. Get onset-to-death delay from `epiparameter`
3. Estimate CFR with `cfr::cfr_static()` or `cfr::cfr_rolling()`

### Transmission Analysis
1. Get generation time from `epiparameter`
2. Estimate R and k using `superspreading` or fit offspring distribution
3. Calculate epidemic probability with `probability_epidemic()`

### Scenario Modeling
1. Define population with `epidemics::population()`
2. Set up interventions with `epidemics::intervention()`
3. Run model with `epidemics::model_default()` or disease-specific model

### Final Size
1. Get contact matrix (e.g., from `socialmixr`)
2. Define susceptibility structure
3. Calculate with `finalsize::final_size()`

## Best Practices

- Always account for delays when estimating severity
- Use delay distributions from literature (`epiparameter`)
- Report estimates with uncertainty (confidence intervals)
- Visualize time-varying estimates to show temporal changes
- Check model assumptions (proportional hazards for CFR)
- Document parameter sources and justifications

## Common Pitfalls

- **CFR without delay correction**: Underestimates severity during active outbreak
- **Ignoring heterogeneity**: Leads to incorrect final size estimates
- **Wrong offspring distribution**: Affects superspreading inference
- **Misspecified contact matrices**: Impacts intervention effectiveness

## Integration with Other Skills

- **data-intake**: Provides cleaned line list data
- **parameters**: Provides delay distributions for correction
- **visualisation**: Creates plots of rolling estimates, epidemic curves
- **reporting**: Synthesizes results into publication-ready document
