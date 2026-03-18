# Changelog

All notable changes to the EpiAgent Skills project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2024-01-15

### Added - Reporting Skill and Quarto Integration

#### New Reporting Skill
- **reporting/SKILL.md**: Comprehensive 7th skill (600+ lines) providing:
  - Complete guide to creating publication-ready Quarto reports
  - Standard academic report structure (executive summary → conclusion)
  - Integration patterns for all pipeline stages
  - Figure and table formatting with gt and patchwork
  - BibTeX citation management
  - Reproducibility documentation templates
  - Multiple output formats (HTML, PDF, Word)
  - Best practices checklist

#### Quarto-Based Examples
- **examples/ebola_outbreak/**: Complete example analysis:
  - **ebola_analysis.qmd**: 500-line Quarto document with:
    - Full narrative analysis (background, methods, results, discussion)
    - Executive summary and conclusions
    - Parameter justification section
    - Interactive code chunks with labels
    - Cross-referenced figures and tables
    - Session information and package versions
  - **references.bib**: BibTeX bibliography with 4 key citations
  - **ebola_analysis.html**: Rendered 2.2 MB self-contained HTML output
- **examples/README.md**: Comprehensive guide to running and creating examples
- **examples/MIGRATION.md**: Migration guide from old workflow to Quarto

#### Modular Workflow Functions
- **R/workflow_functions.R**: Extracted reusable functions (258 lines):
  - `setup_ebola_parameters()`: Configure epidemiological parameters
  - `simulate_ebola_outbreak()`: Generate synthetic outbreak data
  - `clean_outbreak_data()`: Standardize and tag linelist
  - `estimate_cfr()`: Calculate delay-corrected case fatality risk
  - `create_visualizations()`: Generate publication-ready plots
  - All functions have roxygen2 documentation
  - Error handling and input validation included

#### Documentation
- **GETTING_STARTED.md**: Comprehensive beginner's guide (400+ lines):
  - Step-by-step walkthrough from installation to first report
  - Three usage options (Claude Code, template, functions)
  - Common workflows (simulation, real data, scenarios)
  - Explanation of all 7 skills
  - Troubleshooting section
  - Best practices and conventions

### Changed

#### Pipeline Architecture
- **6-stage pipeline** (was 5 stages):
  - Data Intake → Parameters → Simulation → Analysis → Visualization → **REPORT**
- **"Start with the end in mind" philosophy**: Report is now the explicit end goal
- All skills now document how their outputs contribute to the final report

#### Updated Skills
- **epiverse_overview/SKILL.md**:
  - Added reporting to routing table
  - Updated pipeline diagram to show 6 stages
  - Added reporting to skill dependencies
  - Updated all workflow examples to include report generation
  - Added note: "The default goal is a complete publication-ready report"
- **All SKILL.md files**: Updated to reference reporting as final deliverable

#### Repository Structure
- **Legacy workflow**: `ebola_workflow.R` preserved as `.legacy` for backwards compatibility
- **New structure**: Separation of functions (R/) and examples (examples/)
- **Output organization**: Clear distinction between data/ and outputs/

#### Main Documentation
- **README.md**:
  - Updated to mention 7 skills (was 6)
  - Added link to GETTING_STARTED.md
  - Updated pipeline diagram
  - Added reporting skill to skills overview
  - Changed "visualizations" to "reports" as end goal
- **CLAUDE.md**: Updated to reference examples/ebola_outbreak/ instead of ebola_workflow.R

### Improved

#### Reproducibility
- All examples use Quarto with `embed-resources: true` for self-contained output
- Session information automatically included in all reports
- Package versions documented
- Random seeds explicitly set
- Date of analysis auto-generated

#### User Experience
- Natural language → report workflow with Claude Code
- Template-based approach for customization
- Modular functions for advanced users
- Multiple entry points for different skill levels

#### Code Quality
- Functions properly documented with roxygen2
- Clear separation of concerns (functions vs examples)
- Consistent use of here::here() for paths
- Error messages provide actionable guidance

## [2.0.0] - 2024-01-01

### Added - Repository Modernization

#### Documentation
- **README.md**: Comprehensive project overview with quick-start guide, features, and usage examples
- **CLAUDE.md**: Detailed agent instructions including Introspection Protocol and coding standards
- **CONTRIBUTING.md**: Complete contribution guidelines with code style, testing, and PR process
- **ARCHITECTURE.md**: System design documentation with component diagrams and design decisions
- **LICENSE**: MIT license for open-source distribution
- **.gitignore**: Comprehensive ignore rules for R artifacts, data, and outputs
- **data/README.md**: Data dictionary and file format documentation
- **outputs/README.md**: Output specifications and usage guidelines

#### Skills Enhancement
- **visualisation/SKILL.md**: Expanded from 68 to 622 lines with:
  - Complete tracetheme documentation
  - Visualization cookbook with 6 plot type categories
  - Publication-ready figure guidelines
  - Integration examples with other Epiverse packages
  - Troubleshooting section
- **epiverse_overview/SKILL.md**: Added:
  - Introspection Protocol (was missing)
  - Routing examples with decision tree
  - Workflow templates for common tasks
  - Skill dependency matrix
  - Task mapping guide

#### Code Quality
- **ebola_workflow.R**: Complete refactor with:
  - Modular function architecture (6 main functions)
  - Comprehensive roxygen2 documentation
  - Error handling with try-catch blocks
  - Input validation and data quality checks
  - Progress logging and execution summary
  - Version checking and dependency verification
  - 537 lines total (from 257 lines, but more maintainable)

### Changed

#### Breaking Changes
- `ebola_workflow.R` now uses functional architecture instead of linear script
- Functions are now the primary interface (can be sourced and called individually)
- Main workflow executes via `run_ebola_workflow()` function

#### Improvements
- All file paths now use `here::here()` consistently
- Error messages are more informative with troubleshooting hints
- Plots now include subtitles and captions for context
- Data validation occurs at each pipeline stage
- Execution time tracking added to workflow

### Fixed
- Trailing whitespace in some R code files
- Inconsistent column name handling in data cleaning
- Missing error handling for package loading failures
- Hard-coded file paths replaced with portable paths

## [1.0.0] - 2024-01-01 (Initial State)

### Initial Implementation

#### Skills
- `epiverse_overview` - Basic routing skill (40 lines)
- `data_intake` - Data cleaning skill with 4 packages
- `parameters` - Parameter management skill
- `simulation` - Outbreak simulation skill (965 lines)
- `analysis` - CFR and transmission analysis skill (1,448 lines)
- `visualisation` - Basic theme skill (68 lines)

#### Core Files
- `ebola_workflow.R` - Linear workflow script (257 lines)
- `registry.json` - Package metadata for 15 packages (355 lines)

#### Directory Structure
- `.agent/skills/` - 6 skill directories with SKILL.md files
- `data/raw/` - Raw data storage
- `data/processed/` - Processed data storage
- `outputs/plots/` - Plot outputs
- `outputs/tables/` - Table outputs

### Known Limitations in v1.0.0
- Missing critical documentation (README, LICENSE, CONTRIBUTING)
- No .gitignore file
- visualisation skill incomplete (only 68 lines)
- epiverse_overview missing Introspection Protocol
- Monolithic ebola_workflow.R script
- No error handling in workflows
- No data or output documentation
- No architecture documentation

---

## Version History Summary

| Version | Date | Type | Description |
|---------|------|------|-------------|
| **2.0.0** | 2024-01-01 | Major | Complete repository modernization |
| 1.0.0 | 2024-01-01 | Initial | Initial skill pack implementation |

---

## Upgrade Guide

### Migrating from 1.0.0 to 2.0.0

#### ebola_workflow.R Changes

**Before (v1.0.0)**:
```r
# Linear script execution
source("ebola_workflow.R")
# Entire workflow runs immediately
```

**After (v2.0.0)**:
```r
# Option 1: Run complete workflow
source("ebola_workflow.R")  # Executes run_ebola_workflow() automatically

# Option 2: Use individual functions
source("ebola_workflow.R")
params <- setup_ebola_parameters()
outbreak <- simulate_ebola_outbreak(params)
# ... use functions individually
```

#### Skill Usage

**No changes required** - All skills maintain backward compatibility. The additions are enhancements only.

#### File Paths

If you have custom workflows:

**Before**:
```r
data <- read.csv("data/raw/mydata.csv")  # Relative path
```

**After**:
```r
data <- readr::read_csv(here::here("data", "raw", "mydata.csv"))  # Portable
```

---

## Future Roadmap

### Planned for v2.1.0
- Quick reference tables for analysis skill
- Integration guidance for simulation skill
- Reference tables for parameters skill
- End-to-end workflows for data_intake skill
- Enhanced registry.json with repository URLs

### Planned for v3.0.0
- CI/CD integration with GitHub Actions
- Automated testing framework
- Additional example workflows
- Interactive Shiny dashboard
- Docker containerization

### Under Consideration
- Real-time data integration from DHIS2/SORMAS
- Multi-language support (Python, Julia)
- Cloud deployment guides (AWS, Azure, GCP)
- Advanced modeling capabilities (spatial, stochastic)

---

## Contributing

To contribute:
1. Read [CONTRIBUTING.md](CONTRIBUTING.md)
2. Check planned features above
3. Open an issue to discuss your idea
4. Submit a pull request

---

## Support

- **Issues**: Report bugs via GitHub Issues
- **Documentation**: See [README.md](README.md)
- **Architecture**: See [ARCHITECTURE.md](ARCHITECTURE.md)
- **Epiverse**: https://epiverse-trace.github.io/

---

**Maintained by**: Epiverse-TRACE Team
**License**: MIT
