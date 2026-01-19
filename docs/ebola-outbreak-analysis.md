# Analysing Ebola Outbreak Data with GitHub Copilot and Epiverse

## Introduction

This vignette describes the use of GitHub Copilot in VS Code with the epiagent Model Context Protocol (MCP) server for outbreak analysis. The MCP server exposes Epiverse tools to Copilot, which can then access them through natural language queries.

**Objectives:**

- Query Copilot to discover Epiverse packages
- Retrieve epidemiological parameters through Copilot
- Execute R functions via natural language requests
- Use Copilot to orchestrate multi-step workflows

## Prerequisites

This vignette assumes you have:

- VS Code with GitHub Copilot installed
- The epiagent MCP server configured (see README.md)
- Basic familiarity with outbreak analysis concepts
- The epiagent MCP server running (check `.vscode/mcp.json`)

## Background

Ebola Virus Disease (EVD) is a severe, often fatal illness in humans with case fatality rates ranging from 25% to 90% in past outbreaks. Rapid analysis of outbreak data is critical for informing public health response. The Epiverse initiative provides a suite of R packages for real-time outbreak analytics.

The **epiagent MCP server** exposes these packages to GitHub Copilot through four core tools that Copilot can invoke automatically:

1. `list_packages` - Browse the Epiverse package ecosystem
2. `find_tools` - Semantic search for task-appropriate packages  
3. `call_function` - Execute R functions with automatic type conversion
4. `ingest_git_repo` - Analyse package source code

The MCP server exposes these tools to Copilot, which selects and invokes them based on natural language queries.

## Setup

1. Open VS Code with the epiagent workspace
2. Open Copilot Chat (`Cmd+Shift+I` or click the chat icon)
3. Select "Agent" mode from the dropdown
4. Check available MCP tools with `@workspace /tools`

The command should list 4 tools: `list_packages`, `call_function`, `find_tools`, and `ingest_git_repo`.

## 1. Package Discovery

Packages can be discovered by querying Copilot.

### Example: Finding simulation tools

**You ask Copilot:**
```
@workspace What Epiverse packages can help me simulate outbreak data?
```

**Copilot responds** (after calling `find_tools` automatically):
```
The simulist package is ideal for simulating outbreak data. It's an R 
package specifically designed for simulating line lists with realistic 
epidemiological structure including contact chains, reporting delays, 
and demographic information.

Score: 7.0
Repository: https://github.com/epiverse-trace/simulist
```

Copilot invokes the `find_tools` MCP tool to search the package registry and returns matching results.

### Example: Finding tools for different tasks

**You ask:**
```
@workspace I need to convert line list data to incidence. Which package should I use?
```

**Copilot responds:**
```
The incidence2 package is recommended. It converts individual case data 
(line lists) into aggregated incidence time series, with support for 
multiple time intervals and stratification variables.
```

**You ask:**
```
@workspace What tools estimate the reproduction number?
```

**Copilot responds:**
```
For reproduction number estimation, tutorials-middle provides comprehensive 
workflows. The package includes methods for real-time estimation that account 
for epidemiological delays and reporting lags, with connections to packages 
like EpiEstim and EpiNow2.
```

## 2. Retrieving Epidemiological Parameters Conversationally

Now that you know which tools exist, you can ask Copilot to retrieve actual data from the Epiverse databases.

### Getting Ebola incubation periods

**You ask Copilot:**
```
@workspace Get the Ebola incubation period from the epiparameter database
```

**Copilot responds:**
```
Retrieved Ebola incubation period distributions. The database contains 
5 parameterised distributions from different studies:

Status: success
Results: 5 distributions available

Each entry includes:
- Probability distribution type (gamma, lognormal, etc.)
- Distribution parameters (mean, SD, shape, scale)
- Study metadata and citations
- Inference methodology

To select a specific distribution, you can ask me to filter by study 
characteristics or geographic region.
```

Behind the scenes, Copilot:
1. Recognised you wanted epiparameter data
2. Called the `call_function` MCP tool
3. Executed `epiparameter::epiparameter_db(disease="Ebola", epi_name="incubation period")`
4. Presented the results in a user-friendly format

### Getting serial intervals

**You ask:**
```
@workspace Now get the Ebola serial interval
```

**Copilot responds:**
```
Retrieved Ebola serial interval distributions:

Status: success
Results: 4 parameterised distributions

The serial interval (time between symptom onset in consecutive cases) 
is essential for estimating the reproduction number. These distributions 
come from studies of West and Central African outbreaks.
```

### Exploring other diseases

**You ask:**
```
@workspace What about COVID-19 serial intervals?
```

**Copilot responds:**
```
Retrieved COVID-19 serial interval data. Multiple distributions are 
available from studies conducted in different settings (China, Europe, 
USA). The estimates range from 4-7 days depending on the study and 
variant era.
```

The query automatically adjusts to the specified disease.

## 3. Multi-Tool Workflows

Copilot can invoke multiple MCP tools sequentially to complete complex requests.

### Example: Complete outbreak analysis request

**You ask Copilot:**
```
@workspace I need to analyse an Ebola outbreak. Can you:
1. Find the best tools for estimating CFR
2. Get the Ebola case fatality parameters
3. Recommend packages for visualising epidemic curves
```

**Copilot responds:**

```
Here's your complete Ebola analysis toolkit:

1. CFR ESTIMATION
   Package: cfr
   Purpose: Estimates disease severity and under-reporting in real-time, 
            accounting for reporting delays
   Score: 11.5
   Topics: case-fatality-rate, outbreak-analysis, epidemic-modelling

2. EBOLA PARAMETERS
   Retrieved from epiparameter database:
   - Incubation period: 5 distributions available
   - Serial interval: 4 distributions available
   - CFR estimates: Available from literature

3. VISUALISATION
   Package: incidence2
   Purpose: Creates epidemic curves from line list or incidence data
   Features: 
   - Daily, weekly, or custom intervals
   - Stratification by demographics
   - Built-in plotting methods
   
   Also recommended: tutorials-early
   Purpose: Tutorials for data visualisation and exploratory analysis

Your analysis pipeline is ready. Would you like me to execute any of 
these tools with specific parameters?
```

Tool invocation sequence:
1. `find_tools` to locate the CFR package
2. `call_function` to retrieve Ebola parameters
3. `find_tools` to locate visualisation packages
4. Results synthesised in response

### Multi-step workflow example

**You ask:**
```
@workspace Walk me through setting up an Ebola severity analysis pipeline
```

**Copilot responds:**

```
I'll help you set up a complete Ebola severity analysis pipeline:

STEP 1: DATA PREPARATION
Tool: cleanepi
- Standardises date formats
- Validates case data
- Handles missing values

STEP 2: PARAMETER RETRIEVAL
Tool: epiparameter
✓ Retrieved Ebola incubation period (5 distributions)
✓ Retrieved Ebola serial interval (4 distributions)
- Select appropriate distribution based on your outbreak setting

STEP 3: INCIDENCE CALCULATION
Tool: incidence2
- Converts line list to time series
- Aggregates by appropriate time interval
- Stratifies by relevant variables

STEP 4: CFR ESTIMATION
Tool: cfr
Methods available:
- Naive CFR (deaths/cases)
- Delay-adjusted CFR
- Under-reporting correction
- Bayesian estimation

STEP 5: VISUALISATION & REPORTING
Tool: tutorials-early
- Generates epidemic curves
- Creates summary statistics
- Produces publication-ready figures

Would you like me to help implement any specific step?
```

## 4. Conversational Data Exploration

You can have back-and-forth conversations with Copilot to refine your analysis.

### Interactive parameter selection

**You:**
```
@workspace Which Ebola incubation period study should I use?
```

**Copilot:**
```
The choice depends on your outbreak context. The database has 5 studies:
- West African outbreak (2014-2016): larger sample, more recent
- Central African outbreaks: different transmission settings
- Healthcare vs community transmission: affects delay distributions

I can help you filter by study characteristics. What's your outbreak setting?
```

**You:**
```
@workspace West African, community transmission
```

**Copilot:**
```
For West African community transmission, I recommend the WHO Ebola 
Response Team (2014) parameterisation. It has:
- Large sample size (n > 4500 cases)
- Mean incubation: 11.4 days
- Distribution: Gamma(mean=11.4, sd=7.3)
- Context: 2014-2016 West Africa outbreak

Would you like me to extract the specific parameters?
```

Parameters can be refined through follow-up queries without writing code.

## 5. Asking for Complete Code

When you're ready to implement, you can ask Copilot to generate the actual code.

**You ask:**
```
@workspace Write Python code that uses the epiagent tools to:
1. Find CFR estimation packages
2. Get Ebola parameters
3. Print a summary
```

**Copilot generates:**

```python
from epiagent import find_relevant_packages, call_epiverse_function

# 1. Find CFR packages
cfr_packages = find_relevant_packages("estimate case fatality rate")
print(f"CFR estimation: {cfr_packages[0].package.name}")
print(f"  Score: {cfr_packages[0].score}")

# 2. Get Ebola parameters
incubation = call_epiverse_function(
    package="epiparameter",
    function="epiparameter_db",
    kwargs={"disease": "Ebola", "epi_name": "incubation period"}
)

serial = call_epiverse_function(
    package="epiparameter",
    function="epiparameter_db",
    kwargs={"disease": "Ebola", "epi_name": "serial interval"}
)

# 3. Summary
print(f"\nEbola Parameters:")
print(f"  Incubation: {incubation.status}")
print(f"  Serial interval: {serial.status}")
```

The generated code can be executed, modified, or integrated into existing workflows.

## Summary

This vignette described the use of GitHub Copilot with the epiagent MCP server for outbreak analysis workflows:

**Conversational Discovery:**
- Ask Copilot to find packages → it searches the Epiverse ecosystem
- Request specific tools → it recommends based on your task
- Query across 67+ packages → no need to know they exist

**Autonomous Execution:**
- Ask for data → Copilot calls R functions automatically
- Request parameters → it retrieves from databases
- Need multiple steps → it orchestrates tools seamlessly

**Interactive Refinement:**
- Have back-and-forth conversations to refine analysis
- Copilot remembers context across the conversation
- Adjust parameters and approaches conversationally

**Code Generation:**
- When ready, ask Copilot to generate executable code
- It creates proper Python using the epiagent library
- Code can be run, modified, and integrated into workflows

MCP tools are invoked through natural language queries rather than direct function calls. Copilot selects and executes tools based on query context.

## Practical Tips

### Query formulation

1. Specific queries (e.g., "Find tools for delay-adjusted CFR estimation") yield more relevant results than general terms
2. Multi-part questions can be processed in a single request
3. Follow-up queries can refine results
4. Code generation requires explicit requests

### Checking MCP status

To verify your MCP tools are working:
```
@workspace /tools
```

You should see: `list_packages`, `call_function`, `find_tools`, `ingest_git_repo`

### Understanding Copilot's tools use

Watch the chat window for indicators that Copilot is calling MCP tools. You'll see:
- "Using tool: find_tools" 
- "Using tool: call_function"

This transparency helps you understand what's happening behind the scenes.

## Next Steps

**Try these queries in Copilot Chat:**

```
@workspace What packages help with vaccine effectiveness studies?
```

```
@workspace Get me the measles incubation period and R0 estimates
```

```
@workspace Create a complete dengue outbreak analysis pipeline
```

```
@workspace Which packages work with contact tracing data?
```

## Resources

- **Epiverse tutorials:** https://epiverse-trace.github.io/
- **GitHub Copilot docs:** https://docs.github.com/copilot
- **MCP specification:** https://modelcontextprotocol.io/
- **epiagent repository:** https://github.com/epiverse-trace/epiagent

## Session Information

To share your setup:
```
@workspace Show my MCP configuration
```

Copilot will display your `.vscode/mcp.json` settings and confirm the tools are loaded.

---

*This vignette describes the use of MCP-enabled tools in GitHub Copilot for epidemiological analysis workflows.*
