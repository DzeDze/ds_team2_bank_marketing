"""
Input validation for uploaded CSVs.

We validate that the uploaded file includes the exact feature columns needed by the pipeline.
"""

from dataclasses import dataclass
from typing import Iterable, List, Sequence

import pandas as pd


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    missing: List[str]
    extra: List[str]

def validate_columns(df: pd.DataFrame, required_cols: Iterable[str]) -> ValidationResult:
    """
    Validate DataFrame includes required columns.

    Args:
        df: input data
        required_cols: required columns

    Returns:
        ValidationResult
    """
    required = list(required_cols)
    missing = [c for c in required if c not in df.columns]
    extra = [c for c in df.columns if c not in required] if required else []
    return ValidationResult(ok=len(missing) == 0, missing=missing, extra=extra)