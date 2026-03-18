---
name: visualisation
description: Skill for creating standardised Epiverse-TRACE plots using ggplot2 and tracetheme.
---

# Epiverse-TRACE Visualisation

> [!IMPORTANT]
> **Use the Introspection Protocol**: See [epiverse-overview](../epiverse-overview/SKILL.md) skill for the protocol. Before generating code, verify package APIs and functions using R introspection commands.

> [!NOTE]
> **Workflow Context**: This skill's code should be included in **Quarto document code chunks** (not separate R scripts). Plots are created and displayed inline in the Quarto document. See the [reporting](../reporting/SKILL.md) skill for the complete workflow structure.

This skill provides guidance for creating publication-ready epidemiological visualizations using the Epiverse-TRACE visual style.

## Package: `tracetheme`

**Purpose**: Standardized ggplot2 theme and color scales following Epiverse-TRACE branding.

**Installation**:
```r
# From r-universe (recommended)
install.packages("tracetheme", repos = c("https://epiverse-trace.r-universe.dev", "https://cloud.r-project.org"))

# From GitHub
pak::pak("epiverse-trace/tracetheme")
```

**Key Functions**:
- `theme_trace()`: Main theme function for consistent visual style
- `scale_color_trace()`: Color scale for color aesthetic
- `scale_fill_trace()`: Fill scale for fill aesthetic
- `trace_palette()`: View available color palettes
- `show_palette()`: Display palette examples

**Key Features**:
- Consistent Epiverse-TRACE branding
- Colorblind-friendly palettes
- Publication-ready defaults
- Seamless ggplot2 integration

## Essential Plot Types

### Epidemic Curves
Show temporal distribution of cases:
- Daily/weekly case counts: `geom_histogram()` or `geom_col()`
- Stratified by outcome: Use `fill` aesthetic with `geom_histogram(position = "stack")`
- Smooth curves: `geom_smooth()` for trend lines

### Time Series with Uncertainty
Show estimates with confidence intervals:
- `geom_ribbon()` for uncertainty bands
- `geom_line()` for point estimates
- Essential for CFR, Rt, and other time-varying estimates

### Distributions
Show parameter or delay distributions:
- `geom_histogram()` for observed data
- `geom_density()` or `stat_function()` for theoretical distributions
- Overlay observed vs theoretical for comparison

### Multi-Panel Figures
Combine multiple plots:
- Use `patchwork` package: `(plot1 + plot2) / (plot3 + plot4)`
- Or `gridExtra::grid.arrange()`
- Tag panels with `labs(tag = "A")`

## Publication Standards

### Figure Sizing
```r
ggsave(
  filename = here::here("outputs", "plots", "figure.png"),
  width = 8,    # inches (single column: 3.5-4, double: 7-8)
  height = 5,   # inches
  dpi = 300,    # high resolution for print
  bg = "white"  # white background
)
```

### Recommended Dimensions
- Single column: 3.5-4" width
- 1.5 column: 5-6" width
- Double column: 7-8" width
- Poster/presentation: 10-12" width

### Accessibility
- Use colorblind-safe palettes (tracetheme colors are designed for this)
- Add text labels where possible
- Use line types and shapes in addition to colors
- Ensure sufficient contrast

### Font Guidelines
```r
theme_trace(
  base_size = 12,         # Base font size
  base_family = "sans"    # Use sans-serif fonts
)

# Customize specific elements
+ theme(
  plot.title = element_text(size = 14, face = "bold"),
  axis.title = element_text(size = 11),
  axis.text = element_text(size = 9)
)
```

## Common Patterns

### Pattern: Rolling Estimate with CI
```r
ggplot(data, aes(x = date)) +
  geom_ribbon(aes(ymin = lower, ymax = upper), fill = "blue", alpha = 0.2) +
  geom_line(aes(y = estimate), color = "darkblue", linewidth = 1) +
  labs(title = "Title", x = "Date", y = "Estimate") +
  theme_trace()
```

### Pattern: Stratified Epidemic Curve
```r
ggplot(data, aes(x = date, fill = category)) +
  geom_histogram(binwidth = 7, color = "white") +
  scale_fill_trace() +
  labs(title = "Title", x = "Date", y = "Cases") +
  theme_trace()
```

### Pattern: Distribution Comparison
```r
ggplot(data, aes(x = value)) +
  geom_histogram(aes(y = after_stat(density)), binwidth = 1, fill = "blue", alpha = 0.5) +
  stat_function(fun = dgamma, args = list(shape = 2, scale = 5), color = "red") +
  labs(title = "Observed vs Theoretical", x = "Value", y = "Density") +
  theme_trace()
```

## Integration with Epiverse Packages

### With cfr Package
```r
cfr_results |>
  ggplot(aes(x = date)) +
  geom_ribbon(aes(ymin = severity_low, ymax = severity_high),
              fill = "darkred", alpha = 0.2) +
  geom_line(aes(y = severity_estimate), color = "darkred") +
  scale_y_continuous(labels = scales::percent) +
  labs(title = "Rolling CFR", x = "Date", y = "CFR") +
  theme_trace()
```

### With epidemics Package
```r
model_output |>
  pivot_longer(cols = c(S, E, I, R), names_to = "compartment") |>
  ggplot(aes(x = time, y = value, color = compartment)) +
  geom_line(linewidth = 1) +
  scale_color_trace() +
  labs(title = "SEIR Dynamics", x = "Time", y = "Count") +
  theme_trace()
```

### With epiparameter Package
```r
# Plot parameter distribution
tibble(x = seq(0, 30, 0.1)) |>
  mutate(density = dgamma(x, shape = 2, scale = 5)) |>
  ggplot(aes(x, density)) +
  geom_area(fill = "steelblue", alpha = 0.5) +
  labs(title = "Incubation Period", x = "Days", y = "Density") +
  theme_trace()
```

## Best Practices

1. **Load tracetheme**: Always `library(tracetheme)`
2. **Apply theme last**: Add `theme_trace()` after all geom layers
3. **Match scales**: Use `scale_fill_trace()` with `fill` aesthetic, `scale_color_trace()` with `color`
4. **Set dimensions**: Use `ggsave()` with explicit width/height/dpi
5. **Test accessibility**: Check colorblind-friendliness
6. **Save plots**: Always save to `outputs/plots/` with descriptive names
7. **Use here::here()**: For portable file paths

## Troubleshooting

### Theme Not Applied
```r
# Apply theme at END of ggplot chain
ggplot(data, aes(x, y)) +
  geom_point() +
  theme_trace()  # Must be after all geom layers
```

### Colors Not Showing
```r
# Match scale function to aesthetic mapping
aes(fill = outcome)   → scale_fill_trace()
aes(color = outcome)  → scale_color_trace()
```

### Font Warnings
```r
# Use default fonts if warnings appear
theme_trace(base_family = "")
```

## Complete Example

```r
library(ggplot2)
library(tracetheme)
library(dplyr)

# Create epidemic curve
epicurve <- linelist |>
  ggplot(aes(x = date_onset)) +
  geom_histogram(binwidth = 7, fill = "steelblue", color = "white") +
  labs(
    title = "Epidemic Curve",
    subtitle = "Weekly case counts",
    x = "Date of Onset",
    y = "Cases"
  ) +
  theme_trace()

# Save plot
ggsave(
  here::here("outputs", "plots", "epicurve.png"),
  epicurve,
  width = 8, height = 5, dpi = 300, bg = "white"
)
```

## Resources

- **ggplot2 Documentation**: https://ggplot2.tidyverse.org/
- **tracetheme GitHub**: https://github.com/epiverse-trace/tracetheme
- **patchwork**: https://patchwork.data-imaginist.com/
- **Color Brewer**: https://colorbrewer2.org/

## Integration with Other Skills

- **analysis**: Visualizes CFR, Rt, and other estimates
- **data-intake**: Creates plots of cleaned data
- **simulation**: Shows simulated outbreak dynamics
- **reporting**: All plots included in final report with `theme_trace()`
