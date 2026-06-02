# UAV Adversarial GNSS Testing Framework

An open-source adversarial testing framework for GPS-denied and GPS-spoofed UAV navigation, built on PX4 SITL, Gazebo Harmonic, ROS 2 Humble, and Edge AI inference on Jetson Nano.

[![CI](https://github.com/fastbunny786/uav-adversarial-testing/actions/workflows/ci.yml/badge.svg)](https://github.com/fastbunny786/uav-adversarial-testing/actions/workflows/ci.yml)
[![Docs](https://github.com/fastbunny786/uav-adversarial-testing/actions/workflows/docs.yml/badge.svg)](https://fastbunny786.github.io/uav-adversarial-testing)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## What this project does

This framework automatically discovers navigation and perception failure modes in PX4-based UAVs under GNSS attack conditions. An adversarial agent generates GNSS interference and spoofing scenarios, runs them against the autopilot, measures navigation error and onboard perception degradation, and reports failures.

The core problem: GPS-denied and GPS-spoofed UAV navigation is a growing challenge in defense and autonomous systems. Current UAV validation against GNSS attacks is mostly manual and ad hoc. This framework brings systematic, ML-driven adversarial testing to the problem — and extends it to cover the full navigation + Edge AI perception pipeline running on Jetson Nano.

---

## Project phases

| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Professional infrastructure | ✅ Complete |
| 1 | PX4 SITL + Gazebo baseline | 🔄 Next |
| 2 | GNSS failure scenario injection | ⏳ Planned |
| 3 | Adversarial scenario generation (RL, Bayesian, evolutionary) | ⏳ Planned |
| 4 | Edge AI integration on Jetson Nano | ⏳ Planned |
| 5 | Production-grade infrastructure | ⏳ Planned |
| 6 | Hardware-in-the-loop on Pixhawk + X500 | ⏳ Planned |

Each phase ships a demoable milestone. No big-bang delivery.

---

## Stack

**Simulation and autopilot**
- PX4 Autopilot (SITL + HITL)
- Gazebo Harmonic
- ROS 2 Humble on Ubuntu 22.04 LTS
- MAVSDK-Python

**Adversarial ML**
- Stable-Baselines3 (PPO)
- Optuna (Bayesian optimization)
- DEAP (evolutionary algorithms)
- Weights & Biases (experiment tracking)

**Edge AI**
- YOLOv8 on Jetson Nano
- TensorRT / ONNX Runtime

**Infrastructure**
- Docker + Docker Compose
- GitHub Actions CI/CD
- pytest + pytest-xdist
- uv (dependency management)
- MkDocs Material (documentation)

---

## Documentation

Full documentation including architecture decisions and setup guides:
**[fastbunny786.github.io/uav-adversarial-testing](https://fastbunny786.github.io/uav-adversarial-testing)**

---

## Status

Phase 0 complete. Phase 1 (PX4 SITL + Gazebo baseline) in progress.

---

## License

MIT — see [LICENSE](LICENSE).
