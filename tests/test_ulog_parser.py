"""
Tests for the ULog parser and MissionMetrics schema validation.

These tests run against a real .ulg file generated from a clean PX4 SITL
baseline mission (no GNSS interference). They establish the expected
behaviour of the parser and the schema for a healthy flight.

The ULog file path is read from the environment variable ULOG_PATH.
If the variable is not set, the tests are skipped — this allows CI to
run the smoke tests without needing a live SITL environment.
"""
from __future__ import annotations

import os
from pathlib import Path

import pytest

from uav_adversarial_testing.parsing.ulog_parser import parse, MissionMetrics
from uav_adversarial_testing.parsing.metrics_schema import validate


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _ulog_path() -> Path | None:
    """Return the ULog path from the environment, or None if not set."""
    val = os.environ.get("ULOG_PATH")
    return Path(val) if val else None


@pytest.fixture
def metrics() -> MissionMetrics:
    """Parse the test ULog file and return MissionMetrics."""
    path = _ulog_path()
    if path is None:
        pytest.skip("ULOG_PATH not set — skipping parser tests")
    return parse(path)


# ---------------------------------------------------------------------------
# Parser tests
# ---------------------------------------------------------------------------

def test_mission_completed(metrics: MissionMetrics) -> None:
    """Baseline mission must complete successfully."""
    assert metrics.mission_completed is True


def test_position_error_baseline(metrics: MissionMetrics) -> None:
    """Clean SITL baseline: max position error must be under 2m."""
    assert metrics.max_position_error_m < 2.0, (
        f"Max position error {metrics.max_position_error_m}m exceeds 2m "
        "for a clean baseline flight — check SITL setup."
    )


def test_flight_duration_positive(metrics: MissionMetrics) -> None:
    """Flight duration must be positive."""
    assert metrics.flight_duration_s > 0


def test_sample_count_sufficient(metrics: MissionMetrics) -> None:
    """Must have enough samples to be a real flight, not a ground test."""
    assert metrics.sample_count >= 100


def test_mean_lte_max(metrics: MissionMetrics) -> None:
    """Mean position error cannot exceed max position error."""
    assert metrics.mean_position_error_m <= metrics.max_position_error_m


# ---------------------------------------------------------------------------
# Schema validation tests
# ---------------------------------------------------------------------------

def test_schema_passes(metrics: MissionMetrics) -> None:
    """MissionMetrics from a clean flight must pass Pandera schema."""
    validated = validate(metrics)
    assert validated is metrics
