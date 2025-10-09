"""Dynamic wrappers around Epiverse Trace R packages for agent tooling."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import json
import re
from pathlib import Path
from typing import Any, Callable, Dict, Mapping, MutableMapping, Optional, Sequence, Tuple

import pandas as pd

FallbackCallable = Callable[[Sequence[Any], Mapping[str, Any]], Any]

from .registry import get_registry

try:  # pragma: no cover - optional dependency guard
    import rpy2.robjects as ro
    from rpy2.robjects import default_converter
    from rpy2.robjects.conversion import localconverter
    from rpy2.robjects.packages import importr
    from rpy2.robjects import pandas2ri
except ImportError:  # pragma: no cover - optional dependency
    ro = None  # type: ignore[assignment]
    default_converter = None  # type: ignore[assignment]
    localconverter = None  # type: ignore[assignment]
    importr = None  # type: ignore[assignment]
    pandas2ri = None  # type: ignore[assignment]
else:  # pragma: no cover - configuration path exercised in integration tests
    pandas2ri.activate()


def _normalise_column_name(name: str) -> str:
    slug = re.sub(r"[^0-9A-Za-z]+", "_", name.strip())
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug.lower()


def _fallback_clean_variable_names(args: Sequence[Any], kwargs: Mapping[str, Any]) -> pd.DataFrame:
    if not args:
        raise ValueError("linelist::clean_variable_names expects a dataset as the first argument")
    frame = pd.DataFrame(args[0])
    renamed = {column: _normalise_column_name(str(column)) for column in frame.columns}
    return frame.rename(columns=renamed)


def _fallback_incidence(args: Sequence[Any], kwargs: Mapping[str, Any]) -> pd.DataFrame:
    if not args:
        raise ValueError("incidence2::incidence expects a dataset as the first argument")
    frame = pd.DataFrame(args[0]).copy()
    date_index = kwargs.get("date_index")
    if not date_index:
        raise ValueError("A 'date_index' keyword argument is required for incidence2::incidence fallbacks")
    if date_index not in frame.columns:
        raise KeyError(f"Column '{date_index}' was not found in the provided dataset")

    date_series = pd.to_datetime(frame[date_index], errors="coerce").dropna()
    if date_series.empty:
        raise ValueError(f"Column '{date_index}' does not contain any parseable dates")

    date_series = date_series.dt.floor("D")
    counts = date_series.value_counts().sort_index()
    counts.index = pd.to_datetime(counts.index)
    counts = counts.sort_index()

    interval = max(int(kwargs.get("interval", 1)), 1)
    if interval > 1:
        counts = counts.resample(f"{interval}D").sum()

    if kwargs.get("fill_dates", True):
        start, end = counts.index.min(), counts.index.max()
        freq = f"{interval}D"
        counts = counts.reindex(pd.date_range(start, end, freq=freq), fill_value=0)

    result = pd.DataFrame({
        "date": counts.index.date,
        "count": counts.values,
    })
    return result


FALLBACK_IMPLEMENTATIONS: Dict[Tuple[str, str], FallbackCallable] = {
    ("linelist", "clean_variable_names"): _fallback_clean_variable_names,
    ("incidence2", "incidence"): _fallback_incidence,
}


@dataclass
class ToolResult:
    """Structured response returned to the calling agent."""

    status: str
    data: Optional[Any] = None
    message: Optional[str] = None
    artifact_path: Optional[Path] = None

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"status": self.status}
        if self.message:
            payload["message"] = self.message
        if self.data is not None:
            payload["data"] = _serialise_data(self.data)
        if self.artifact_path is not None:
            payload["artifact_path"] = str(self.artifact_path)
        return payload


def list_epiverse_packages(refresh: bool = False) -> ToolResult:
    """Return the known Epiverse Trace repositories."""

    registry = get_registry()
    if refresh:
        try:
            packages = registry.refresh_from_github()
        except Exception as err:  # pragma: no cover - network failure handling
            return ToolResult(status="error", message=str(err))
    else:
        packages = registry.sorted_packages
    return ToolResult(
        status="success",
        data={"packages": [package.to_dict() for package in packages]},
    )


def call_epiverse_function(
    package: str,
    function: str,
    args: Optional[Sequence[Any]] = None,
    kwargs: Optional[Mapping[str, Any]] = None,
    auto_convert: bool = True,
) -> ToolResult:
    """Invoke an arbitrary function from an Epiverse Trace R package."""

    registry = get_registry()
    package_known = registry.has_package(package)

    fallback = FALLBACK_IMPLEMENTATIONS.get((package, function))
    fallback_reason: Optional[str] = None
    module = None

    if importr is None:
        fallback_reason = "rpy2 is not installed, so R packages cannot be imported."
        if fallback is None:
            return ToolResult(status="error", message=fallback_reason)
    else:
        try:
            module = _import_package(package)
        except Exception as err:  # pragma: no cover - R import failure guard
            fallback_reason = f"Failed to import R package '{package}': {err}"
            if fallback is None:
                return ToolResult(status="error", message=fallback_reason)

    if module is not None and not hasattr(module, function):
        fallback_reason = f"Package '{package}' does not expose a callable named '{function}'"
        if fallback is None:
            return ToolResult(status="error", message=fallback_reason)

    positional_args = list(args or [])
    keyword_args: MutableMapping[str, Any] = dict(kwargs or {})

    execution_message: Optional[str] = None

    if module is not None and hasattr(module, function) and ro is not None and localconverter is not None:
        r_callable = getattr(module, function)
        try:
            if auto_convert:
                with localconverter(default_converter + pandas2ri.converter):
                    r_args = [ro.conversion.py2rpy(arg) for arg in positional_args]
                    r_kwargs = {key: ro.conversion.py2rpy(val) for key, val in keyword_args.items()}
                result = r_callable(*r_args, **r_kwargs)
                with localconverter(default_converter + pandas2ri.converter):
                    converted = ro.conversion.rpy2py(result)
            else:
                converted = r_callable(*positional_args, **keyword_args)
        except Exception as err:  # pragma: no cover - runtime safety
            return ToolResult(status="error", message=str(err))
    elif fallback is not None:
        try:
            converted = fallback(positional_args, keyword_args)
        except Exception as err:
            message = f"Python fallback for {package}::{function} failed: {err}"
            return ToolResult(status="error", message=message)
        execution_message = f"Python fallback executed for {package}::{function}"
        if fallback_reason:
            execution_message = f"{execution_message} ({fallback_reason})"
    else:
        if fallback_reason:
            return ToolResult(status="error", message=fallback_reason)
        return ToolResult(
            status="error",
            message="Unable to execute function because the R runtime is unavailable.",
        )

    note: Optional[str] = None
    if execution_message:
        note = execution_message
    if not package_known:
        registry_hint = (
            "Executed function successfully but the package was not present in the local registry. "
            "Consider refreshing the package list."
        )
        note = f"{note}\n{registry_hint}" if note else registry_hint
    if note is None and fallback_reason and fallback is not None:
        note = fallback_reason

    return ToolResult(status="success", data=converted, message=note)


@lru_cache(maxsize=None)
def _import_package(name: str):
    """Import an R package through :func:`rpy2.robjects.packages.importr`."""

    if importr is None:
        raise ImportError("rpy2 is not installed")
    return importr(name)


def _serialise_data(data: Any) -> Any:
    if isinstance(data, pd.DataFrame):
        return {"type": "dataframe", "records": data.to_dict(orient="records")}
    if isinstance(data, pd.Series):
        return {"type": "series", "values": data.to_dict()}
    if isinstance(data, (list, dict, str, int, float, bool)) or data is None:
        return data
    if isinstance(data, Path):
        return str(data)
    try:
        return json.loads(json.dumps(data, default=str))
    except Exception:  # pragma: no cover - fallback serialisation
        return repr(data)


__all__ = [
    "ToolResult",
    "list_epiverse_packages",
    "call_epiverse_function",
]
