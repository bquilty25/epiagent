"""Integration tests for the epiagent wrappers."""

from __future__ import annotations

import math

import pytest

from epiagent import ToolResult, call_epiverse_function, list_epiverse_packages


def test_list_epiverse_packages_loads_catalogue():
    """Ensure the registry JSON is parsed successfully without refreshing."""

    result = list_epiverse_packages()
    assert isinstance(result, ToolResult)
    assert result.status == "success"
    assert isinstance(result.data, dict)
    packages = result.data.get("packages", [])
    assert isinstance(packages, list)
    # The curated registry currently contains at least one entry.
    assert packages, "expected at least one package entry in the registry"


@pytest.mark.requires_r
def test_call_epiverse_function_accepts_numpy_results():
    """Calling an R function should return a numpy array when appropriate."""

    result = call_epiverse_function("stats", "rnorm", kwargs={"n": 4})
    assert result.status == "success"
    assert result.data is not None
    assert hasattr(result.data, "tolist")
    payload = result.to_payload()
    assert payload["status"] == "success"
    array_info = payload["data"]
    assert array_info["type"] == "array"
    assert len(array_info["values"]) == 4
    assert all(math.isfinite(x) for x in array_info["values"])
