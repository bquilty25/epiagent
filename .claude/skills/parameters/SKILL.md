---
name: parameters
description: Skill for retrieving and managing epidemiological parameters (incubation periods, serial intervals) using epiparameter.
---

# Epiverse-TRACE Parameters

> [!IMPORTANT]
> **Use the Introspection Protocol**: See [epiverse-overview](../epiverse-overview/SKILL.md) skill for the protocol. Before generating code, verify package APIs and functions using R introspection commands.

> [!NOTE]
> **Workflow Context**: This skill's code should be included in **Quarto document code chunks** (not separate R scripts). See the [reporting](../reporting/SKILL.md) skill for the complete workflow structure.

This skill provides access to a library of epidemiological parameters from the literature and tools for parameter manipulation.

## Packages

### `epiparameter`
**Purpose**: Classes and helper functions for working with epidemiological parameters.

**Key Functions**:
- `epiparameter_db()`: Load parameters from library (disease, epi_name, author filters)
- `epiparameter()`: Create custom parameter object
- `parameter_tbl()`: View parameters as table
- `plot()`: Visualize parameter distribution
- `convert_params_to_summary_stats()`: Convert distribution parameters to mean/SD
- `convert_summary_stats_to_params()`: Convert mean/SD to distribution parameters
- `extract_param()`: Extract parameters from summary statistics

**Supported Distributions**: gamma, lognormal, Weibull, normal, negative binomial, geometric

### `epiparameterDB`
**Purpose**: Database of epidemiological parameters extracted from literature.

**Access**: Via `epiparameter::epiparameter_db()` (recommended) or direct JSON access

**Coverage**: 23 diseases, 125+ parameter sets including incubation periods, serial intervals, generation times, onset-to-hospitalization, onset-to-death

**Online Database**: View at https://epiverse-trace.github.io/epiparameter/articles/database.html

## Typical Workflow

### Finding Parameters
```r
# Search by disease and parameter type
param <- epiparameter_db(
  disease = "Ebola Virus Disease",
  epi_name = "incubation period",
  single_epiparameter = TRUE
)

# View all available parameters
all_params <- epiparameter_db()
parameter_tbl(all_params)
```

### Using Parameters
```r
# Extract distribution function
dist_func <- function(x) dgamma(x, shape = param$shape, scale = param$scale)

# Use in analysis
cfr_static(data, delay_density = dist_func)
```

### Creating Custom Parameters
```r
# When parameter not in library
custom_param <- epiparameter(
  disease = "COVID-19",
  epi_name = "onset to hospitalization",
  prob_distribution = create_prob_distribution(
    prob_distribution = "lnorm",
    prob_distribution_params = c(meanlog = 1.5, sdlog = 0.5)
  )
)
```

### Parameter Conversion
```r
# Convert summary statistics to distribution parameters
params <- convert_summary_stats_to_params(
  mean = 10,
  sd = 5,
  distribution = "gamma"
)
```

## Common Parameter Types

- **Incubation period**: Time from infection to symptom onset
- **Serial interval**: Time between symptom onset in infector and infectee
- **Generation time**: Time between infection in infector and infectee
- **Onset to hospitalization**: Time from symptoms to hospital admission
- **Onset to death**: Time from symptoms to death
- **Hospitalisation to death**: Time from admission to death
- **Offspring distribution**: Number of secondary infections per case

## Best Practices

- Always cite the source of parameters (use `get_citation()`)
- Check parameter applicability (population, setting, time period)
- Use `single_epiparameter = TRUE` when expecting one result
- Visualize distributions with `plot()` to verify plausibility
- Document parameter choices in analysis reports
- Consider uncertainty in parameter estimates

## Contributing Parameters

To add parameters to the library:
1. Use the public [Google Sheet](https://docs.google.com/spreadsheets/d/1eCL3n_woseg5Npu7XD7TcuNoLUIhMBu8ZoLCkVdATUE/edit)
2. Or submit PR to [epiparameterDB](https://github.com/epiverse-trace/epiparameterDB)

## Integration with Other Skills

- **simulation**: Use parameters to simulate realistic outbreaks
- **analysis**: Use delay distributions for CFR correction
- **reporting**: Document parameter sources and justifications
