"""
Mission launcher — starts PX4 SITL, runs the mission orchestrator,
parses the resulting ULog, and prints metrics.

Usage:
    uv run python src/uav_adversarial_testing/scripts/run_mission.py

Exit codes:
    0 — mission completed successfully
    1 — mission failed or SITL did not start
"""

import asyncio
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path

from uav_adversarial_testing.scripts.fly_mission import run as fly
from uav_adversarial_testing.parsing.ulog_parser import parse

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PX4_ROOT = Path.home() / "PX4-Autopilot"
LOG_ROOT = PX4_ROOT / "build/px4_sitl_default/rootfs/log"
SITL_CMD = ["make", "px4_sitl", "gz_x500"]
SITL_UDP_PORT = 14540
SITL_READY_TIMEOUT_S = 60
SITL_READY_POLL_INTERVAL_S = 2


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sitl_is_ready(port: int) -> bool:
    """Return True if something is listening on UDP port (SITL is up)."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(1)
        try:
            s.connect(("127.0.0.1", port))
            s.send(b"\x00")
            return True
        except (OSError, socket.timeout):
            return False


def _wait_for_sitl(timeout_s: int, poll_s: float) -> bool:
    """Poll until SITL UDP port is reachable or timeout expires."""
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        if _sitl_is_ready(SITL_UDP_PORT):
            return True
        print(f"[launcher] Waiting for SITL on UDP {SITL_UDP_PORT}...")
        time.sleep(poll_s)
    return False


def _latest_ulog() -> Path | None:
    """Return the most recently modified .ulg file under LOG_ROOT."""
    ulogs = sorted(LOG_ROOT.rglob("*.ulg"), key=lambda p: p.stat().st_mtime)
    return ulogs[-1] if ulogs else None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    print(f"[launcher] Starting PX4 SITL: {' '.join(SITL_CMD)}")
    sitl = subprocess.Popen(
        SITL_CMD,
        cwd=PX4_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=lambda: signal.signal(signal.SIGINT, signal.SIG_IGN),
    )

    try:
        print(f"[launcher] Waiting up to {SITL_READY_TIMEOUT_S}s for SITL to be ready...")
        if not _wait_for_sitl(SITL_READY_TIMEOUT_S, SITL_READY_POLL_INTERVAL_S):
            print("[launcher] ERROR: SITL did not become ready in time.")
            sitl.terminate()
            return 1

        print("[launcher] SITL ready. Running mission...")
        asyncio.run(fly())

        # give PX4 a moment to flush the log after landing
        time.sleep(3)

        log_path = _latest_ulog()
        if log_path is None:
            print("[launcher] ERROR: No ULog file found after mission.")
            return 1

        print(f"[launcher] Parsing log: {log_path}")
        metrics = parse(log_path)
        print(f"[launcher] {metrics}")

        return 0 if metrics.mission_completed else 1

    finally:
        print("[launcher] Shutting down SITL...")
        sitl.terminate()
        sitl.wait(timeout=10)
        print("[launcher] SITL stopped.")


if __name__ == "__main__":
    sys.exit(main())
