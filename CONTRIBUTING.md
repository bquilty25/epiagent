# Contributing to EpiAgent Skills

Thank you for your interest in contributing to EpiAgent Skills! This document provides guidelines for contributing to this Claude Agent SDK skill pack for epidemiological analysis.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Adding New Skills](#adding-new-skills)
- [Updating Existing Skills](#updating-existing-skills)
- [Testing Requirements](#testing-requirements)
- [Documentation Standards](#documentation-standards)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project follows the [Epiverse-TRACE Code of Conduct](https://github.com/epiverse-trace/.github/blob/main/CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs

- **Use a clear and descriptive title** for the issue
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** with code snippets
- **Describe the behavior you observed** and what you expected
- **Include R session info**: `sessionInfo()` output

### Suggesting Enhancements

- **Use a clear and descriptive title**
- **Provide a step-by-step description** of the suggested enhancement
- **Explain why this enhancement would be useful** to most users
- **List any R packages or tools** you think would be helpful

### Contributing Code

We welcome contributions of:

1. **New Skills**: Additional epidemiological analysis capabilities
2. **Bug Fixes**: Corrections to existing code
3. **Documentation**: Improvements to guides and examples
4. **Examples**: New workflow demonstrations
5. **Tests**: Additional validation and testing

## Development Setup

### Prerequisites

1. **R** (≥ 4.3.0)
2. **Git**
3. **Claude Agent SDK** (if testing with Claude)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/epiagent_skills.git
cd epiagent_skills

# Install R packages
Rscript -e "source('install_packages.R')"
```

### Testing Your Setup

```r
# Run the example workflow to verify everything works
source("ebola_workflow.R")
```

If this completes successfully, your environment is ready for development.

## Coding Standards

All contributions must follow these standards:

### R Code Style

Follow the [tidyverse style guide](https://style.tidyverse.org/):

```r
# GOOD: Clear, readable, tidyverse style
cleaned_data <- raw_data |>
  filter(!is.na(date_onset)) |>
  mutate(age_group = cut(age, breaks = c(0, 18, 65, Inf)))

# BAD: Hard to read, inconsistent style
CleanedData=rawData%>%filter(!is.na(dateOnset))%>%mutate(agegroup=cut(age,breaks=c(0,18,65,Inf)))
```

**Key Conventions**:
- `snake_case` for variables and functions
- Native pipe (`|>`) not magrittr pipe (`%>%`)
- Spaces around operators (`x + y` not `x+y`)
- One command per line for readability
- Maximum line length: 80 characters

### File Paths

Always use `here::here()` for portability:

```r
# GOOD: Portable across systems
data_path <- here::here("data", "raw", "outbreak.csv")

# BAD: Hard-coded absolute paths
data_path <- "/Users/username/project/data/raw/outbreak.csv"
```

### Reproducibility

Set seeds for any stochastic operations:

```r
# Always set seed before random operations
set.seed(42)
outbreak <- sim_outbreak(...)
```

### Dates

Use ISO 8601 format (YYYY-MM-DD):

```r
# GOOD: Unambiguous date format
outbreak_date <- as.Date("2024-03-15")

# BAD: Ambiguous
outbreak_date <- as.Date("3/15/24")
```

### Comments

```r
# Good: Explain WHY, not WHAT
# Use Gamma distribution to match observed mean and variance
params <- estimate_gamma_params(mean = 10, sd = 3)

# Unnecessary: Code is self-explanatory
# Calculate the sum
total <- sum(values)
```

## Adding New Skills

### Skill Structure

1. Create a new directory: `.agent/skills/new_skill_name/`
2. Create `SKILL.md` with this structure:

```markdown
---
description: Brief one-line description of what this skill does
---

# Skill Title

> [!IMPORTANT]
> **CRITICAL: The Introspection Protocol**
> [Include the standard Introspection Protocol block]

Brief overview of the skill's purpose.

## Package: `package_name`

**Brief Package Description**

### Key Functions

- `function_name()` - Description
- `another_function()` - Description

### Usage Examples

[Include working code examples]

### Documentation

[Links to vignettes, pkgdown sites, GitHub repos]
```

### Requirements for New Skills

- [ ] YAML frontmatter with `description`
- [ ] Introspection Protocol block
- [ ] Package documentation for all relevant packages
- [ ] Working code examples
- [ ] Links to external documentation
- [ ] Update `epiverse_overview/SKILL.md` routing table
- [ ] Update `registry.json` if new packages added

### Testing New Skills

Before submitting:

1. **Verify Introspection Protocol** works as documented
2. **Test all code examples** in a clean R session
3. **Check documentation links** are valid
4. **Run with Claude** (if possible) to verify agent can use it

## Updating Existing Skills

### When Packages Update

If an Epiverse-TRACE package is updated:

1. Update the `registry.json` with new version and exports
2. Review SKILL.md for affected functions
3. Update code examples if API changed
4. Test all examples still work
5. Update vignette references if new vignettes added

### Adding Content to Existing Skills

- Maintain consistent structure with other skills
- Add examples for common use cases
- Include troubleshooting tips
- Link to relevant vignettes

## Testing Requirements

### Manual Testing

All code must be tested manually:

```r
# Start with clean session
# File -> Restart R (in RStudio)

# Test your code
source("your_script.R")

# Verify outputs
list.files(here::here("outputs"))
```

### Validation Checklist

Before submitting:

- [ ] Code runs without errors in clean R session
- [ ] All required packages are listed in dependencies
- [ ] File paths use `here::here()`
- [ ] Seeds set for reproducibility
- [ ] Outputs saved to correct directories
- [ ] No absolute paths or system-specific code
- [ ] Error messages are informative
- [ ] Comments explain epidemiological assumptions

### Example Workflow Testing

Always test with the `ebola_workflow.R`:

```bash
Rscript ebola_workflow.R
```

Verify it completes successfully and outputs are generated.

## Documentation Standards

### SKILL.md Files

**Structure**:
1. YAML frontmatter
2. Introspection Protocol
3. Package-by-package documentation
4. Code examples with comments
5. Links to external resources

**Code Examples**:
- Must be complete and runnable
- Include necessary library() calls
- Use realistic example data
- Show expected output
- Explain epidemiological context

### Comments

```r
# Epidemiological assumption: Assume constant attack rate across age groups
attack_rate <- 0.15

# Data validation: Remove cases with impossible dates (before outbreak start)
clean_data <- data |>
  filter(date_onset >= outbreak_start)
```

### Inline Documentation

For functions, use roxygen2 style:

```r
#' Simulate Ebola Outbreak
#'
#' Generates synthetic outbreak data using epidemiological parameters
#' from literature. Returns both linelist and contact data.
#'
#' @param r0 Basic reproduction number (default: 2)
#' @param outbreak_size Numeric vector of c(min, max) cases
#' @param seed Random seed for reproducibility
#'
#' @return List with `linelist` and `contacts` data frames
#'
#' @examples
#' outbreak <- simulate_ebola_outbreak(r0 = 2, outbreak_size = c(100, 500))
simulate_ebola_outbreak <- function(r0 = 2, outbreak_size = c(100, 500), seed = 42) {
  # Implementation
}
```

## Pull Request Process

### Before Submitting

1. **Create a feature branch**: `git checkout -b feature/your-feature-name`
2. **Make your changes** following the coding standards
3. **Test thoroughly** using the validation checklist
4. **Update documentation** if needed
5. **Commit with clear messages**:
   ```bash
   git commit -m "Add CFR estimation example to analysis skill

   - Added example using cfr package
   - Included delay correction
   - Updated documentation links"
   ```

### Submitting a Pull Request

1. **Push your branch**: `git push origin feature/your-feature-name`
2. **Create a pull request** on GitHub
3. **Use a clear title**: "Add [feature]" or "Fix [issue]"
4. **Describe your changes**:
   - What does this PR do?
   - Why is this change needed?
   - How was it tested?
   - Are there breaking changes?

### PR Template

```markdown
## Description
Brief description of what this PR does

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Breaking change

## Testing
- [ ] Tested in clean R session
- [ ] All examples run successfully
- [ ] Documentation builds correctly

## Checklist
- [ ] Code follows style guidelines
- [ ] Comments explain epidemiological assumptions
- [ ] Documentation updated
- [ ] Tests pass (if applicable)
```

### Review Process

1. **Automated checks** will run (if configured)
2. **Maintainer review**: A maintainer will review your code
3. **Address feedback**: Make requested changes
4. **Approval**: Once approved, your PR will be merged

## Registry Updates

When adding or updating packages in `registry.json`:

```json
{
  "package_name": {
    "title": "Package Title",
    "description": "Brief description",
    "version": "1.0.0",
    "repository": "https://github.com/org/package",
    "license": "MIT",
    "pkgdown": "https://org.github.io/package",
    "exports": ["function1", "function2"],
    "vignettes": [
      {"title": "Getting Started", "name": "intro"}
    ],
    "used_by_workflows": ["ebola_workflow.R"]
  }
}
```

## Common Contribution Scenarios

### Adding a New Epiverse Package

1. Install and test the package
2. Add entry to `registry.json`
3. Determine which skill it belongs to (or create new skill)
4. Add documentation to appropriate SKILL.md
5. Create working examples
6. Update routing in `epiverse_overview/SKILL.md`

### Fixing a Bug in a Workflow

1. Identify the issue
2. Create a test case that reproduces the bug
3. Fix the issue
4. Verify the fix works
5. Add comments explaining the fix
6. Submit PR with clear description

### Improving Documentation

1. Identify what's unclear or missing
2. Add clarifying text or examples
3. Test that examples work
4. Ensure links are valid
5. Submit PR

## Questions?

- **General questions**: Open a GitHub Discussion
- **Bugs**: Open a GitHub Issue
- **Security issues**: Email maintainers privately
- **Epiverse packages**: Visit [epiverse-trace.github.io](https://epiverse-trace.github.io/)

## Recognition

Contributors will be recognized in:
- CHANGELOG.md
- Repository contributors page
- Package citations (when applicable)

Thank you for contributing to EpiAgent Skills!
