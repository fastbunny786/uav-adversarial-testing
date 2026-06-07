"""
Pandera schema for MissionMetrics validation.

Validates that the ULog parser output is well-formed before it is used
as input to the Phase 2 failure oracle or any downstream analysis.
"""
from __future__ import annotations

import pandera.pandas as pa
from pandera.typing import Series
import pandas as pd

from uav_adversarial_testing.parsing.ulog_parser import MissionMetrics


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

class MissionMetricsSchema(pa.DataFrameModel):
    """Pandera schema for a DataFrame of MissionMetrics rows."""

    log_file: Series[str] = pa.Field(nullable=False)
    mission_completed: Series[bool] = pa.Field(nullable=False)
    flight_duration_s: Series[float] = pa.Field(gt=0, nullable=False)
    max_position_error_m: Series[float] = pa.Field(ge=0, nullable=False)
    mean_position_error_m: Series[float] = pa.Field(ge=0, nullable=False)
    sample_count: Series[int] = pa.Field(gt=0, nullable=False)

    class Config:
        strict = True  # no extra columns allowed


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def validate(metrics: MissionMetrics) -> MissionMetrics:
    """
    Validate a single MissionMetrics instance against the schema.

    Converts to a one-row DataFrame, runs Pandera validation, and
    returns the original metrics object if validation passes.

    Raises
    ------
    pandera.errors.SchemaError
        If any field violates the schema constraints.
    """
    df = pd.DataFrame([{
        "log_file": metrics.log_file,
        "mission_completed": metrics.mission_completed,
        "flight_duration_s": metrics.flight_duration_s,
        "max_position_error_m": metrics.max_position_error_m,
        "mean_position_error_m": metrics.mean_position_error_m,
        "sample_count": metrics.sample_count,
    }])

    MissionMetricsSchema.validate(df)
    return metrics
