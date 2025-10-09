"""Run a reference workflow against Epi R Handbook linelist data."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from textwrap import indent
from typing import Iterable, List

import pandas as pd

# Ensure the package under development is importable when running from the repo root.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:  # pragma: no cover - import guard
    sys.path.insert(0, str(SRC_PATH))

from epiagent.agent import EpiAgent, PlannedToolCall  # noqa: E402
from epiagent.tools.r_wrappers import ToolResult, call_epiverse_function  # noqa: E402

HANDBOOK_LINELIST_URL = (
    "https://raw.githubusercontent.com/appliedepi/epiRhandbook_eng/master/"
    "data/case_linelists/fluH7N9_China_2013.csv"
)
GOAL = "Clean the flu H7N9 linelist and compute daily incidence"


def load_handbook_linelist() -> pd.DataFrame:
    """Download the flu H7N9 linelist used throughout the Epi R Handbook."""

    frame = pd.read_csv(HANDBOOK_LINELIST_URL)
    for column in ["date_of_onset", "date_of_hospitalisation", "date_of_outcome"]:
        if column in frame.columns:
            frame[column] = pd.to_datetime(frame[column], errors="coerce")
    return frame


def summarise_dataframe(frame: pd.DataFrame) -> str:
    """Return a human-readable summary of a dataframe."""

    preview = frame.head().to_dict(orient="records")
    summary = {
        "rows": int(frame.shape[0]),
        "columns": list(frame.columns),
        "preview": preview,
    }
    return json.dumps(summary, indent=2, default=str)


def execute_plan(plan: Iterable[PlannedToolCall], linelist: pd.DataFrame) -> List[ToolResult]:
    """Execute the subset of the plan that can run with Python fallbacks."""

    results: List[ToolResult] = []
    working_data = linelist

    for step in plan:
        if step.package == "linelist" and step.function == "clean_variable_names":
            result = call_epiverse_function(step.package, step.function, args=(working_data,))
            if result.status == "success" and isinstance(result.data, pd.DataFrame):
                working_data = result.data
            results.append(result)
        elif step.package == "incidence2" and step.function == "incidence":
            kwargs = {"date_index": "date_of_onset", "fill_dates": True}
            result = call_epiverse_function(step.package, step.function, args=(working_data,), kwargs=kwargs)
            results.append(result)
        else:
            # Steps requiring R execution are reported as skipped.
            results.append(
                ToolResult(
                    status="skipped",
                    message=(
                        f"No Python fallback exists for {step.package}::{step.function}. "
                        "Install rpy2 and the Epiverse packages to execute this step."
                    ),
                )
            )
    return results


def print_plan(plan: Iterable[PlannedToolCall]) -> None:
    """Pretty-print the proposed plan."""

    for index, step in enumerate(plan, start=1):
        print(f"  {index}. {step.package}::{step.function} - {step.description}")


def print_results(results: Iterable[ToolResult]) -> None:
    """Pretty-print the results from :func:`execute_plan`."""

    for index, result in enumerate(results, start=1):
        message = result.message or ""
        print(f"Step {index}: {result.status}")
        if message:
            print(indent(message, "    "))
        if isinstance(result.data, pd.DataFrame):
            print(indent("Preview:", "    "))
            print(indent(result.data.head().to_string(index=False), "      "))
        elif result.data is not None:
            print(indent(f"Data: {result.data}", "    "))


def main() -> None:
    linelist = load_handbook_linelist()
    agent = EpiAgent()

    print(f"Goal: {GOAL}\n")
    print("Linelist snapshot:")
    print(indent(summarise_dataframe(linelist), "  "))

    shortlist = agent.shortlist_packages(GOAL)
    plan = agent.plan(GOAL)

    print("\nShortlisted packages:")
    for item in shortlist:
        print(f"  - {item.name} (score={item.score:.2f}): {item.reason}")

    print("\nPlanned tool calls:")
    print_plan(plan)

    print("\nExecuting available steps...")
    results = execute_plan(plan, linelist)
    print_results(results)


if __name__ == "__main__":  # pragma: no cover - manual execution entry point
    main()
