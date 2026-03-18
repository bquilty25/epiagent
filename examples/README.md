# EpiAgent Skills Examples

This directory contains example analyses demonstrating the Epiverse-TRACE workflow using Quarto for reproducible research.

## Available Examples

### 1. [Ebola Outbreak Analysis](ebola_outbreak/)

**File**: [`ebola_outbreak/ebola_analysis.qmd`](ebola_outbreak/ebola_analysis.qmd)

A complete end-to-end demonstration of outbreak analysis:
- Simulate realistic Ebola outbreak using branching processes
- Clean and validate epidemiological data
- Estimate case fatality risk with delay correction
- Create publication-ready visualizations

**Rendered Output**: HTML report with embedded plots and tables

**Run Time**: ~10-20 seconds

**Requirements**:
- R ≥ 4.3.0
- Quarto ≥ 1.3.0
- Epiverse-TRACE packages (see setup chunk)

## Running Examples

### Option 1: Render with Quarto

```bash
# Render to HTML
quarto render examples/ebola_outbreak/ebola_analysis.qmd

# Render to PDF (requires LaTeX)
quarto render examples/ebola_outbreak/ebola_analysis.qmd --to pdf

# Render both formats
quarto render examples/ebola_outbreak/ebola_analysis.qmd --to all
```

### Option 2: Open in RStudio

1. Open `ebola_analysis.qmd` in RStudio
2. Click "Render" button in the toolbar
3. View output in RStudio viewer or browser

### Option 3: Use R Directly

```r
# Install quarto package if needed
install.packages("quarto")

# Render document
quarto::quarto_render("examples/ebola_outbreak/ebola_analysis.qmd")
```

## Output Locations

Rendered documents are saved alongside the source `.qmd` files:

```
examples/
└── ebola_outbreak/
    ├── ebola_analysis.qmd          # Source document
    ├── ebola_analysis.html         # Rendered HTML
    ├── ebola_analysis.pdf          # Rendered PDF (if generated)
    └── references.bib              # Bibliography
```

Data and plots are saved to the repository root directories:

```
data/
├── raw/
│   ├── simulated_linelist.qs
│   └── simulated_contacts.qs
└── processed/
    └── cleaned_tagged_linelist.qs

outputs/
├── plots/
│   ├── epicurve.png
│   └── cfr_rolling.png
└── tables/
    └── cfr_rolling_estimates.csv
```

## Quarto Features Used

### Document Features
- **Table of Contents**: Automatic navigation
- **Code Folding**: Show/hide code chunks
- **Embedded Resources**: Self-contained HTML output
- **Cross-references**: Automatic figure and table numbering
- **Citations**: BibTeX integration

### Code Execution
- **Caching**: Intelligent re-execution
- **Echo Control**: Show or hide code
- **Figure Options**: Size, captions, layout
- **Table Formatting**: Publication-quality tables with `gt`

## Creating New Examples

To add a new example:

1. **Create directory**:
   ```bash
   mkdir examples/my_analysis
   ```

2. **Create Quarto document**:
   ```bash
   touch examples/my_analysis/my_analysis.qmd
   ```

3. **Use template structure**:
   ```yaml
   ---
   title: "My Analysis Title"
   format:
     html:
       toc: true
       code-fold: false
       embed-resources: true
   ---
   ```

4. **Add to this README**

## Best Practices

### Reproducibility
- ✅ Set random seeds: `set.seed(42)`
- ✅ Document package versions in session info
- ✅ Use `here::here()` for portable paths
- ✅ Include date of analysis: `date: today`
- ✅ Enable code visibility: `echo: true`

### Code Quality
- ✅ Name code chunks: `#| label: chunk-name`
- ✅ Add figure captions: `#| fig-cap: "Description"`
- ✅ Control warnings/messages: `#| warning: false`
- ✅ Use descriptive variable names
- ✅ Comment complex operations

### Documentation
- ✅ Executive summary at top
- ✅ Background and objectives section
- ✅ Methodology description
- ✅ Results with interpretation
- ✅ Discussion of limitations
- ✅ Session information at end

## Example Workflow Functions

Reusable functions are stored in [`R/workflow_functions.R`](../R/workflow_functions.R):

- `setup_ebola_parameters()` - Define disease parameters
- `simulate_ebola_outbreak()` - Generate synthetic data
- `clean_outbreak_data()` - Standardize and validate
- `estimate_cfr()` - Calculate case fatality risk
- `create_visualizations()` - Generate plots

These can be sourced in any analysis:

```r
source(here::here("R", "workflow_functions.R"))
```

## Troubleshooting

### Quarto Not Found

```bash
# Install Quarto
# macOS with Homebrew
brew install quarto

# Or download from https://quarto.org/docs/get-started/
```

### Missing Packages

```r
# Install Epiverse packages
options(repos = c(
  epiverse = "https://epiverse-trace.r-universe.dev",
  CRAN = "https://cloud.r-project.org"
))

install.packages(c(
  "simulist", "cleanepi", "linelist", "cfr",
  "epiparameter", "tidyverse", "tracetheme",
  "here", "qs", "gt"
))
```

### Rendering Errors

1. **Check R version**: `R.version.string` (need ≥ 4.3.0)
2. **Update packages**: `update.packages(ask = FALSE)`
3. **Clear cache**: Delete `_cache/` directory
4. **Check paths**: Ensure working directory is repository root

### PDF Rendering Issues

PDF output requires LaTeX:

```bash
# Install TinyTeX (recommended)
quarto install tinytex

# Or use system LaTeX
# macOS: brew install --cask mactex
# Ubuntu: sudo apt-get install texlive-full
```

## Resources

### Quarto Documentation
- [Quarto Guide](https://quarto.org/docs/guide/)
- [Quarto with R](https://quarto.org/docs/computations/r.html)
- [Publishing Docs](https://quarto.org/docs/publishing/)

### Epiverse-TRACE
- [Main Site](https://epiverse-trace.github.io/)
- [Package List](https://epiverse-trace.github.io/packages.html)
- [Tutorials](https://epiverse-trace.github.io/tutorials.html)

### Reproducible Research
- [renv for Dependency Management](https://rstudio.github.io/renv/)
- [here package](https://here.r-lib.org/)
- [Reproducibility Guide](https://the-turing-way.netlify.app/reproducible-research/)

## Contributing Examples

We welcome new examples! Please:

1. Follow the structure of existing examples
2. Include comprehensive documentation
3. Test rendering before submitting
4. Add entry to this README
5. Submit pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines.

---

**Need help?** Open an issue or see the main [README](../README.md)
