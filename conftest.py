"""Pytest configuration for epiagent."""

from __future__ import annotations

import subprocess

import pytest


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers", "requires_r: mark tests that need an operational R environment"
    )


def pytest_runtest_setup(item: pytest.Item) -> None:
    if "requires_r" in item.keywords:
        try:
            subprocess.run(
                ["R", "--version"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception:
            pytest.skip("R runtime is not available")
