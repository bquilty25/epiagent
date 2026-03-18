# EpiAgent Skills Architecture

This document describes the system design and architecture of the EpiAgent Skills repository.

## Table of Contents

- [Overview](#overview)
- [System Design](#system-design)
- [Component Architecture](#component-architecture)
- [Data Flow](#data-flow)
- [Skill System](#skill-system)
- [Integration Points](#integration-points)
- [Design Decisions](#design-decisions)

## Overview

EpiAgent Skills is a Claude Agent SDK skill pack that bridges AI agents with the Epiverse-TRACE R package ecosystem for infectious disease epidemiology. The architecture follows a modular pipeline design that enables flexible composition of analysis workflows.

### Core Principles

1. **Modularity**: Each skill is independent and self-contained
2. **Composability**: Skills can be chained together in pipelines
3. **Introspection-First**: Always verify APIs before code generation
4. **Reproducibility**: Seed management and portable paths throughout
5. **Standards Compliance**: Follows Epiverse-TRACE conventions

## System Design

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Claude Agent                          │
│                    (AI Orchestrator)                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   EpiAgent Skills Layer                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Overview   │  │ Data Intake  │  │  Parameters  │     │
│  │ (Orchestrator│  │   (Clean)    │  │   (Library)  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Simulation  │  │   Analysis   │  │Visualization │     │
│  │  (Generate)  │  │ (Estimate)   │  │   (Plot)     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Epiverse-TRACE R Packages                       │
│  simulist │ cleanepi │ linelist │ epiparameter │ cfr │      │
│  epidemics │ finalsize │ superspreading │ vaccineff │ ...   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    R Ecosystem                               │
│              tidyverse │ ggplot2 │ here │ qs                │
└─────────────────────────────────────────────────────────────┘
```

### Five-Stage Pipeline

The core architecture follows a standardized 5-stage pipeline:

```
1. DATA INTAKE → 2. PARAMETERS → 3. SIMULATION → 4. ANALYSIS → 5. VISUALIZATION
```

Each stage is optional and can be entered at any point based on user needs.

## Component Architecture

### 1. Skill Layer (`.agent/skills/`)

The primary interface between Claude and the R packages.

#### Skill Structure

Each skill is a directory containing a `SKILL.md` file:

```
.agent/skills/
├── skill_name/
│   └── SKILL.md          # Skill documentation and examples
```

#### SKILL.md Format

```markdown
---
description: Brief one-line description
---

# Skill Title

> [!IMPORTANT]
> **CRITICAL: The Introspection Protocol**
> [Standard introspection instructions]

## Package: package_name

### Key Functions
### Usage Examples
### Documentation Links
```

### 2. Workflow Layer (`ebola_workflow.R`)

Demonstrates end-to-end pipeline implementation.

**Architecture**:
```
┌─────────────────────────────────────────┐
│         run_ebola_workflow()            │
│         (Main Orchestrator)             │
└─────────────────┬───────────────────────┘
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
┌──────────────────┐ ┌──────────────────┐
│ setup_ebola_     │ │ simulate_ebola_  │
│ parameters()     │ │ outbreak()       │
└────────┬─────────┘ └────────┬─────────┘
         │                    │
         └─────────┬──────────┘
                   ▼
        ┌──────────────────────┐
        │  clean_outbreak_data()│
        └──────────┬─────────────┘
                   ▼
        ┌──────────────────────┐
        │    estimate_cfr()     │
        └──────────┬─────────────┘
                   ▼
        ┌──────────────────────┐
        │ create_visualizations│
        └──────────┬─────────────┘
                   ▼
        ┌──────────────────────┐
        │    save_outputs()     │
        └───────────────────────┘
```

### 3. Registry Layer (`registry.json`)

Machine-readable metadata catalog.

**Structure**:
```json
{
  "package_name": {
    "title": "Package Title",
    "description": "Description",
    "version": "x.y.z",
    "repository": "https://github.com/...",
    "exports": ["function1", "function2"],
    "vignettes": [{"title": "...", "name": "..."}],
    "pkgdown": "https://...",
    "used_by_workflows": ["workflow1.R"]
  }
}
```

**Purpose**:
- Package discovery
- Function lookup
- Version tracking
- Documentation linkage

## Data Flow

### Complete Pipeline Data Flow

```
[User Request]
      │
      ▼
[Skill Routing] ──────────► registry.json (lookup)
      │
      ▼
[Introspection Protocol]
      │  ls("package:name")
      │  vignette(package)
      │  args(function)
      │
      ▼
[Code Generation]
      │
      ▼
┌─────────────────────────────────────────────────────┐
│                   R EXECUTION                        │
│                                                      │
│  [Raw Data] ──► clean_data() ──► [Cleaned Data]    │
│      │                                   │           │
│      │                                   ▼           │
│      │                          make_linelist()      │
│      │                                   │           │
│      │                                   ▼           │
│      ├──────────► sim_outbreak() ──► [Tagged Data] │
│      │                                   │           │
│      │                                   ▼           │
│      │                             cfr_static()      │
│      │                             cfr_rolling()     │
│      │                                   │           │
│      │                                   ▼           │
│      │                          [CFR Estimates]      │
│      │                                   │           │
│      ▼                                   ▼           │
│  [Parameters] ──────────────────► ggplot() + theme_ │
│  (from library)                          trace()     │
│                                          │           │
│                                          ▼           │
│                                    [Visualizations]  │
└──────────────────────────────────────────┬──────────┘
                                           │
                                           ▼
                                ┌──────────────────────┐
                                │  File System Output  │
                                │                      │
                                │  data/processed/*.qs │
                                │  outputs/plots/*.png │
                                │  outputs/tables/*.csv│
                                └──────────────────────┘
```

### Data Types and Transitions

| Stage | Input Type | Output Type | Format |
|-------|------------|-------------|--------|
| **Raw** | CSV/Excel/Database | Data frame | Varies |
| **Cleaned** | Data frame | Validated data frame | .qs |
| **Tagged** | Data frame | linelist object | .qs |
| **Analysis** | linelist | CFR estimates | tibble |
| **Visualization** | tibble | ggplot object | PNG/PDF |

## Skill System

### Skill Dependencies

```
epiverse_overview (hub)
    │
    ├──► data_intake ──┐
    │                  │
    ├──► parameters ───┼──► simulation ──┐
    │                  │                 │
    │                  └──► analysis ◄───┘
    │                         │
    └──► visualisation ◄──────┘
```

**Dependency Rules**:
- **epiverse_overview**: No dependencies (hub)
- **data_intake**: No dependencies
- **parameters**: No dependencies
- **simulation**: Requires parameters (optional)
- **analysis**: Requires data_intake and/or parameters
- **visualisation**: Requires data from any other skill

### Skill Communication

Skills communicate through:

1. **Data Objects**: Shared R objects (data frames, models)
2. **File System**: Intermediate files in `data/processed/`
3. **Registry**: Metadata lookup
4. **Documentation**: Cross-references in SKILL.md files

Example flow:
```r
# simulation skill output
outbreak <- sim_outbreak(...)

# data_intake skill input
cleaned <- clean_data(outbreak$linelist)

# analysis skill input
cfr <- cfr_static(cleaned)

# visualisation skill input
plot <- ggplot(cfr) + ...
```

## Integration Points

### 1. Claude Agent SDK Integration

**Location**: `.agent/skills/`
**Protocol**: SKILL.md files in prescribed format
**Discovery**: Automatic via directory scanning

### 2. R Package Integration

**Connection**: Direct R function calls
**Safety**: Introspection Protocol verifies APIs
**Isolation**: Each package is independent

### 3. File System Integration

**Paths**: `here::here()` for portability
**Formats**: `.qs` for R objects, CSV for exports
**Structure**: Standardized directory layout

### 4. External Tool Integration

**Python**: Read CSV outputs with pandas
**Excel**: Import CSV tables directly
**Jupyter**: Use R kernel or read files
**Databases**: Export via DBI/odbc packages

## Design Decisions

### 1. Modular Skill Architecture

**Decision**: Separate skills for each pipeline stage

**Rationale**:
- Enables independent development
- Allows flexible composition
- Simplifies testing and maintenance
- Matches natural analysis workflow

**Alternatives Considered**:
- Monolithic single skill ❌ (too complex)
- Package-per-skill ❌ (too granular)

### 2. Introspection Protocol

**Decision**: Mandatory API verification before code generation

**Rationale**:
- Package APIs evolve over time
- Training data may be outdated
- Prevents hallucination
- Ensures working code

**Implementation**: Standardized block in all SKILL.md files

### 3. Registry System

**Decision**: JSON metadata catalog for packages

**Rationale**:
- Machine-readable format
- Easy to update
- Enables intelligent routing
- Documents ecosystem

**Alternatives Considered**:
- No registry ❌ (harder discovery)
- SQL database ❌ (overkill)
- YAML format ❌ (less standard)

### 4. Five-Stage Pipeline

**Decision**: Standardize on 5 stages (intake → parameters → simulation → analysis → visualization)

**Rationale**:
- Matches epidemiological workflow
- Clear separation of concerns
- Easy to teach and communicate
- Flexible entry/exit points

**Flexibility**: Any stage can be skipped or repeated

### 5. File Formats

**Decision**: Use `.qs` for R objects, CSV for exports

**Rationale**:
- `.qs`: Fast, compressed, preserves R structures
- CSV: Universal compatibility for external tools
- Both: Human-readable metadata

**Performance**: 10x faster than RDS, smaller files

### 6. Functional Decomposition

**Decision**: Refactor workflows into documented functions

**Rationale**:
- Reusability across workflows
- Easier testing
- Better documentation
- Clear interfaces

**Example**: `ebola_workflow.R` uses 6 main functions

## Scalability Considerations

### Handling Large Outbreaks

For outbreaks >10,000 cases:

1. **Data Storage**: Use DuckDB or SQLite instead of .qs
2. **Processing**: Chunked data processing
3. **Visualization**: Aggregate before plotting
4. **Memory**: Stream processing where possible

### Multiple Workflows

When building multiple workflows:

1. **Shared Functions**: Extract to `R/functions.R`
2. **Configuration**: Use config files (YAML/JSON)
3. **Templating**: Parameterize workflows
4. **Testing**: Unit tests for reusable functions

### Team Collaboration

For team environments:

1. **Version Control**: Git for code, DVC for data
2. **Environments**: renv for reproducibility
3. **Documentation**: Keep ARCHITECTURE.md updated
4. **Reviews**: Pull request workflow

## Future Enhancements

Potential architecture improvements:

1. **Caching Layer**: Cache expensive computations
2. **Parallel Processing**: future/furrr integration
3. **API Server**: REST API for programmatic access
4. **Dashboard**: Shiny app for interactive exploration
5. **CI/CD**: Automated testing and deployment
6. **Containerization**: Docker for environment consistency

## Technical Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **AI** | Claude Agent SDK | Agent orchestration |
| **Skill System** | Markdown | Documentation format |
| **Analysis** | R (≥4.3.0) | Statistical computing |
| **Packages** | Epiverse-TRACE | Domain-specific tools |
| **Data** | tidyverse | Data manipulation |
| **Viz** | ggplot2 + tracetheme | Visualization |
| **Paths** | here | Portable paths |
| **Serialization** | qs | Fast data storage |
| **Version Control** | Git | Code management |

## Maintenance

### Regular Tasks

1. **Update registry.json** when packages update
2. **Verify Introspection Protocol** still works
3. **Test workflows** with new package versions
4. **Update documentation** for API changes
5. **Archive old outputs** periodically

### Monitoring

Key metrics to track:

- Workflow execution time
- Package versions in use
- Skill usage patterns
- Error rates by skill
- Output file sizes

## Support and Resources

- **Architecture Questions**: See this document
- **Skill Development**: See [CONTRIBUTING.md](CONTRIBUTING.md)
- **Claude Instructions**: See [CLAUDE.md](CLAUDE.md)
- **Package Docs**: See [registry.json](registry.json) for links
- **Epiverse**: https://epiverse-trace.github.io/

---

**Document Version**: 2.0.0
**Last Updated**: 2024-01-01
**Maintained By**: Epiverse-TRACE Team
