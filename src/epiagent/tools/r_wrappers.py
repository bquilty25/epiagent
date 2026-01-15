"""Dynamic wrappers around Epiverse Trace R packages for agent tooling."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import json
from pathlib import Path
from typing import Any, Dict, Mapping, MutableMapping, Optional, Sequence

import pandas as pd

try:  # pragma: no cover - optional dependency
    import numpy as np
except ImportError:  # pragma: no cover - numpy not strictly required
    np = None

from .registry import get_registry

try:  # pragma: no cover - optional dependency guard
    import rpy2.robjects as ro
    from rpy2.robjects import default_converter
    from rpy2.robjects.conversion import get_conversion, localconverter
    from rpy2.robjects.packages import importr
    from rpy2.robjects import pandas2ri
except ImportError as exc:  # pragma: no cover - optional dependency
    raise ImportError(
        "rpy2 is required to use the Epiverse wrappers. Install it via pip "
        "and ensure that R is available in your environment."
    ) from exc

try:
    pandas2ri.activate()
except DeprecationWarning:
    # Newer rpy2 versions raise DeprecationWarning as an exception; the
    # conversion context below already handles pandas objects so we can ignore.
    pass


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

    try:
        module = _import_package(package)
    except Exception as err:  # pragma: no cover - R import failure guard
        message = f"Failed to import R package '{package}': {err}"
        return ToolResult(status="error", message=message)

    if not hasattr(module, function):
        message = f"Package '{package}' does not expose a callable named '{function}'"
        return ToolResult(status="error", message=message)

    r_callable = getattr(module, function)
    positional_args = list(args or [])
    keyword_args: MutableMapping[str, Any] = dict(kwargs or {})

    try:
        if auto_convert:
            with localconverter(default_converter + pandas2ri.converter):
                result = r_callable(*positional_args, **keyword_args)
                conversion = get_conversion()
                converted = conversion.rpy2py(result)
        else:
            converted = r_callable(*positional_args, **keyword_args)
    except Exception as err:  # pragma: no cover - runtime safety
        return ToolResult(status="error", message=str(err))

    note: Optional[str] = None
    if not package_known:
        note = (
            "Executed function successfully but the package was not present in the local registry. "
            "Consider refreshing the package list."
        )

    return ToolResult(status="success", data=converted, message=note)


@lru_cache(maxsize=None)
def _import_package(name: str):
    """Import an R package through :func:`rpy2.robjects.packages.importr`."""

    return importr(name)


def _serialise_data(data: Any) -> Any:
    if isinstance(data, pd.DataFrame):
        return {"type": "dataframe", "records": data.to_dict(orient="records")}
    if isinstance(data, pd.Series):
        return {"type": "series", "values": data.to_dict()}
    if np is not None and isinstance(data, np.ndarray):
        return {"type": "array", "values": data.tolist()}
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
