from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from epiagent.agent import EpiAgent, plan_epiverse_goal
from epiagent.tools.registry import EpiversePackage, EpiverseRegistry


def make_registry() -> EpiverseRegistry:
    packages = {
        "incidence2": EpiversePackage(
            name="incidence2",
            summary="Calculate incidence curves from linelist data.",
            category="r_package",
            topics=["incidence", "surveillance"],
        ),
        "linelist": EpiversePackage(
            name="linelist",
            summary="Clean and standardise linelist data structures.",
            category="r_package",
            topics=["data-cleaning"],
        ),
    }
    return EpiverseRegistry(packages=packages)


def test_shortlist_packages_ranks_relevant_packages():
    agent = EpiAgent(registry=make_registry())
    shortlist = agent.shortlist_packages("clean this linelist")
    assert shortlist
    assert shortlist[0].name == "linelist"


def test_plan_generates_expected_calls():
    agent = EpiAgent(registry=make_registry())
    plan = agent.plan("estimate rt and compute incidence")
    packages = {step.package for step in plan}
    assert {"EpiEstim", "incidence2"}.issubset(packages)


def test_run_skips_execution_when_no_plan():
    agent = EpiAgent(registry=make_registry(), planning_rules=())
    report = agent.run("explore")
    assert report["plan"] == []
    assert report["execution"] == []


def test_plan_epiverse_goal_returns_shortlist_and_plan():
    report = plan_epiverse_goal("clean the linelist")
    assert "shortlist" in report
