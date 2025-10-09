import pandas as pd

from epiagent.tools.r_wrappers import call_epiverse_function


def test_clean_variable_names_fallbacks_to_python_when_r_missing():
    messy = pd.DataFrame({"Case ID": [1, 2], "Date of Onset": ["2020-01-01", "2020-01-02"]})
    result = call_epiverse_function("linelist", "clean_variable_names", args=(messy,))
    assert result.status == "success"
    cleaned = result.data
    assert isinstance(cleaned, pd.DataFrame)
    assert "case_id" in cleaned.columns
    assert "date_of_onset" in cleaned.columns


def test_incidence_fallback_produces_daily_counts():
    records = pd.DataFrame({"date_onset": ["2020-01-01", "2020-01-01", "2020-01-03"]})
    result = call_epiverse_function(
        "incidence2",
        "incidence",
        args=(records,),
        kwargs={"date_index": "date_onset"},
    )
    assert result.status == "success"
    incidence = result.data
    assert isinstance(incidence, pd.DataFrame)
    assert incidence["count"].sum() == 3
    assert incidence.iloc[0]["count"] == 2
    assert incidence.iloc[-1]["count"] == 1
