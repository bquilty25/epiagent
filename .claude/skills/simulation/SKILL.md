---
name: simulation
description: Skill for simulating outbreaks, contact data, and transmission chains using simulist and epichains.
---

# Epiverse-TRACE Simulation

> [!IMPORTANT]
> **Use the Introspection Protocol**: See [epiverse-overview](../epiverse-overview/SKILL.md) skill for the protocol. Before generating code, verify package APIs and functions using R introspection commands.

> [!NOTE]
> **Workflow Context**: This skill's code should be included in **Quarto document code chunks** (not separate R scripts). See the [reporting](../reporting/SKILL.md) skill for the complete workflow structure.

This skill provides tools for simulating synthetic outbreak data and transmission chains for testing, validation, and scenario analysis.

## Packages

### `simulist`
**Purpose**: Simulate individual-level outbreak data including line lists and contact tracing data.

**Key Functions**:
- `sim_linelist()`: Simulate line list with cases, dates, outcomes
- `sim_contacts()`: Simulate contact tracing data
- `sim_outbreak()`: Simulate both line list and contacts together

**Post-processing Functions**:
- `truncate_linelist()`: Create real-time snapshot with right-truncation
- `messy_linelist()`: Add realistic data quality issues
- `censor_linelist()`: Censor dates to weekly/monthly

**Key Features**:
- Parameterized with epiparameter distributions
- Age-structured populations
- Age-stratified risks (hospitalization, death)
- Time-varying CFR
- Realistic data quality issues

### `epichains`
**Purpose**: Simulate and analyze transmission chains using branching processes.

**Key Functions**:
- `simulate_chains()`: Simulate full transmission trees with details
- `simulate_chain_stats()`: Simulate chain statistics only (faster)
- `likelihood()`: Calculate likelihood of observed chain sizes/lengths
- `summary()`: Summarize chain statistics
- `aggregate()`: Aggregate cases by time or generation
- `plot()`: Visualize chains

**Key Features**:
- Track infection trees
- Calculate chain sizes and lengths
- Population effects (finite population, immunity)
- Generation times

## Typical Workflow

### Simulating Line List Data

1. Get epidemiological parameters from `epiparameter`:
   - Contact distribution
   - Infectious period
   - Onset to hospitalization
   - Onset to death

2. Call `sim_linelist()` or `sim_outbreak()` with:
   - Reproduction number (via contact distribution and infection probability)
   - Delay distributions
   - Hospitalization and death risks
   - Population structure

3. Post-process if needed:
   - `truncate_linelist()` for real-time analysis
   - `messy_linelist()` for realistic data quality issues

### Simulating Transmission Chains

1. Define offspring distribution (Poisson, negative binomial)
2. Set generation time distribution
3. Call `simulate_chains()` for full details or `simulate_chain_stats()` for speed
4. Analyze with `summary()`, `aggregate()`, `plot()`

### Chain Size Analysis

1. Simulate chains with `simulate_chain_stats(statistic = "size")`
2. Calculate outbreak probability with results
3. Compare to empirical data using `likelihood()`

## Important Simulation Considerations

### Reproduction Number
- R = contact_rate × probability_of_infection
- If R > 1, outbreaks can grow very large
- Use `outbreak_size` parameter to cap maximum size
- No susceptible depletion in basic model

### Right-Truncation
Real-time outbreak analysis requires accounting for incomplete data:
```r
# Simulate full outbreak
full_outbreak <- sim_linelist(...)

# Create real-time snapshot
realtime_data <- truncate_linelist(
  linelist = full_outbreak,
  max_date = as.Date("2023-03-01")
)
```

### Realistic Data Quality
Add common data issues for testing cleaning pipelines:
```r
messy_data <- messy_linelist(
  linelist = clean_linelist,
  proportion_missing = 0.1,
  proportion_dates_inconsistent = 0.05
)
```

## Best Practices

- Always set `set.seed()` for reproducibility
- Use parameters from literature via `epiparameter`
- Document parameter sources and justifications
- Test cleaning pipelines on simulated data before real data
- Use time-varying CFR for longer outbreaks
- Consider age-structure when relevant
- Cap outbreak size to prevent excessive simulation time

## Common Use Cases

1. **Testing Analysis Methods**: Generate data with known properties to validate methods
2. **Scenario Analysis**: Compare intervention effects on outbreak dynamics
3. **Method Validation**: Test whether analysis methods can recover true parameters
4. **Training Data**: Create realistic examples for teaching
5. **Pipeline Testing**: Validate data cleaning and analysis workflows
6. **Sensitivity Analysis**: Assess impact of parameter uncertainty

## Integration with Other Skills

- **parameters**: Provides realistic distributions for simulation
- **data-intake**: Simulated data tests cleaning pipelines
- **analysis**: Simulated data validates analysis methods
- **visualisation**: Creates epidemic curves and transmission networks
- **reporting**: Documents simulation methods and parameters
