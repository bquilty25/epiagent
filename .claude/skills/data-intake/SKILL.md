---
name: data-intake
description: Skill for data intake, cleaning, and standardization using Epiverse-TRACE tools.
---

# Epiverse-TRACE Data Intake & Cleaning

> [!IMPORTANT]
> **Use the Introspection Protocol**: See [epiverse-overview](../epiverse-overview/SKILL.md) skill for the protocol. Before generating code, verify package APIs and functions using R introspection commands.

> [!NOTE]
> **Workflow Context**: This skill's code should be included in **Quarto document code chunks** (not separate R scripts). See the [reporting](../reporting/SKILL.md) skill for the complete workflow structure.

This skill handles the first stage of the outbreak analysis pipeline: importing data from Health Information Systems and preparing it for analysis.

## Packages

### `readepi`
**Purpose**: Import data from Health Information Systems (DHIS2, SORMAS, SQL databases).

**Key Functions**:
- `login()`: Authenticate with HIS
- `read_dhis2()`: Import from DHIS2
- `read_sormas()`: Import from SORMAS
- `read_rdbms()`: Import from SQL databases
- `show_tables()`: List available tables

### `cleanepi`
**Purpose**: Standardize and clean epidemiological data.

**Key Functions**:
- `clean_data()`: Master wrapper for common cleaning tasks
- `standardize_dates()`: Convert dates to ISO 8601
- `standardize_column_names()`: Convert to snake_case
- `check_subject_ids()`: Verify unique identifiers
- `remove_duplicates()`: Deduplicate records
- `replace_missing_values()`: Handle missing data

### `linelist`
**Purpose**: Tag epidemiological metadata for robust downstream analysis.

**Key Functions**:
- `make_linelist()`: Convert data.frame to linelist object
- `set_tags()`: Assign semantic tags (e.g., date_onset, outcome)
- `validate_linelist()`: Check data integrity based on tags
- `tags_df()`: Retrieve tagged data frame
- `tags_names()`: List available tag names

### `numberize`
**Purpose**: Convert written number words to numeric digits.

**Key Functions**:
- `numberize()`: Convert "twenty-one" → 21. Supports English, French, Spanish.

## Typical Workflow

1. **Import**: Use `readepi` to connect to HIS and import data
2. **Clean**: Use `cleanepi::clean_data()` to standardize and validate
3. **Tag**: Use `linelist::make_linelist()` to add epidemiological metadata
4. **Validate**: Use `linelist::validate_linelist()` to check integrity

## Best Practices

- Always use `here::here()` for file paths
- Set seeds for reproducibility
- Use ISO 8601 date format (YYYY-MM-DD)
- Document data sources and processing steps
- Check `vignette(package = "pkg_name")` for detailed workflows
