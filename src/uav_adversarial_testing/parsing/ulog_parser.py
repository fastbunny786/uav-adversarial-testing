"""
ULog parser for PX4 SITL mission logs.

Extracts position error (estimated vs ground truth), flight duration,
and mission completion status from a .ulg file produced by PX4.

Mission completion is inferred from two conditions:
- sufficient flight samples (drone actually flew)
- max position error below threshold (no GNSS-induced divergence)

This oracle is intentionally reused in Phase 2 for failure detection:
a spoofing scenario that pushes max error above 5m is a detected failure.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pyulog


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

COMPLETION_MIN_SAMPLES = 100
COMPLETION_MAX_ERROR_M = 5.0


# ---------------------------------------------------------------------------
# Output dataclass
# ---------------------------------------------------------------------------

@dataclass
class MissionMetrics:
    """Structured metrics extracted from a single PX4 ULog file."""

    log_file: str
    mission_completed: bool
    flight_duration_s: float
    max_position_error_m: float
    mean_position_error_m: float
    sample_count: int


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in metres between two lat/lon points."""
    R = 6_371_000.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _get_topic(log: pyulog.ULog, name: str) -> pyulog.core.ULogData | None:
    """Return the first matching topic data object, or None if absent."""
    matches = [d for d in log.data_list if d.name == name]
    return matches[0] if matches else None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def parse(log_path: str | Path) -> MissionMetrics:
    """
    Parse a PX4 ULog file and return a MissionMetrics dataclass.

    Parameters
    ----------
    log_path:
        Absolute or relative path to the .ulg file.

    Returns
    -------
    MissionMetrics
        Extracted metrics for this mission run.

    Raises
    ------
    FileNotFoundError
        If log_path does not exist.
    ValueError
        If required topics are missing from the log.
    """
    log_path = Path(log_path)
    if not log_path.exists():
        raise FileNotFoundError(f"ULog file not found: {log_path}")

    log = pyulog.ULog(str(log_path))

    # --- flight duration ------------------------------------------------------
    vehicle_status = _get_topic(log, "vehicle_status")
    land_detected = _get_topic(log, "vehicle_land_detected")

    if vehicle_status is not None and land_detected is not None:
        armed_time_us = float(vehicle_status.data["armed_time"][0])
        landed_flags = land_detected.data["landed"]
        landed_ts = land_detected.data["timestamp"]
        landed_indices = np.where(landed_flags == 1)[0]
        if len(landed_indices) > 0:
            land_time_us = float(landed_ts[landed_indices[-1]])
            flight_duration_s = (land_time_us - armed_time_us) / 1e6
        else:
            flight_duration_s = (log.last_timestamp - log.start_timestamp) / 1e6
    else:
        flight_duration_s = (log.last_timestamp - log.start_timestamp) / 1e6

    # --- position error (estimated vs ground truth) --------------------------
    est = _get_topic(log, "vehicle_global_position")
    gt = _get_topic(log, "vehicle_global_position_groundtruth")

    if est is None or gt is None:
        raise ValueError(
            "Topics 'vehicle_global_position' and/or "
            "'vehicle_global_position_groundtruth' not found in log."
        )

    est_ts = est.data["timestamp"].astype(float)
    gt_ts = gt.data["timestamp"].astype(float)

    gt_lat_interp = np.interp(est_ts, gt_ts, gt.data["lat"].astype(float))
    gt_lon_interp = np.interp(est_ts, gt_ts, gt.data["lon"].astype(float))

    errors_m = np.array([
        _haversine_m(est.data["lat"][i], est.data["lon"][i],
                     gt_lat_interp[i], gt_lon_interp[i])
        for i in range(len(est_ts))
    ])

    # --- mission completion ---------------------------------------------------
    # PX4 closes the log before writing final mission_result events so
    # seq_reached is unreliable. Completion is inferred from two conditions:
    # the drone actually flew (sufficient samples) and position error stayed
    # clean (no GNSS-induced divergence). This is also the correct oracle for
    # Phase 2 failure detection: a spoofing scenario that pushes max error
    # above COMPLETION_MAX_ERROR_M is a detected failure.
    mission_completed = (
        len(errors_m) >= COMPLETION_MIN_SAMPLES
        and float(np.max(errors_m)) < COMPLETION_MAX_ERROR_M
    )

    return MissionMetrics(
        log_file=str(log_path),
        mission_completed=mission_completed,
        flight_duration_s=round(flight_duration_s, 2),
        max_position_error_m=round(float(np.max(errors_m)), 3),
        mean_position_error_m=round(float(np.mean(errors_m)), 3),
        sample_count=len(errors_m),
    )