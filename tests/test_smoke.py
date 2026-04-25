"""Smoke test: confirms the test suite runs and pytest is wired up correctly.

This file deliberately contains a trivial test. Real tests will arrive
with Phase 1 (the PX4 SITL + Gazebo baseline). Until then, this exists
so that CI has at least one passing test to collect, which prevents the
"no tests collected" failure mode (pytest exit code 5).
"""


def test_smoke() -> None:
    """Trivial assertion that always passes. Proves pytest collection works."""
    assert True


def test_package_importable() -> None:
    """Confirms the project's own package can be imported.

    This exercises the editable install setup that uv configured: if this
    test passes in CI, it means `uv sync` correctly installed our package
    into the venv and Python can find it via standard import resolution.
    """
    import uav_adversarial_testing  # noqa: F401
