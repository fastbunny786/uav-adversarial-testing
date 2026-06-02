# UAV Adversarial GNSS Testing Framework

An open-source adversarial testing framework for GPS-denied and GPS-spoofed UAV navigation, built on PX4 SITL, Gazebo Harmonic, ROS 2 Humble, and Edge AI inference on Jetson Nano.

## What this project does

This framework automatically discovers navigation and perception failure modes in PX4-based UAVs under GNSS attack conditions. An adversarial agent generates GNSS interference and spoofing scenarios, runs them against the autopilot, measures navigation error and perception degradation, and reports failures.

## Why it exists

GPS-denied and GPS-spoofed UAV navigation is a growing problem in defense and autonomous systems. Current UAV validation against GNSS attacks is mostly manual and ad hoc. This framework brings systematic, ML-driven adversarial testing to the problem.

## Project phases

| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Professional infrastructure | ✅ Complete |
| 1 | PX4 SITL + Gazebo baseline | 🔄 Next |
| 2 | GNSS failure scenario injection | ⏳ Planned |
| 3 | Adversarial scenario generation | ⏳ Planned |
| 4 | Edge AI integration on Jetson Nano | ⏳ Planned |
| 5 | Production-grade infrastructure | ⏳ Planned |
| 6 | Hardware-in-the-loop on Pixhawk + X500 | ⏳ Planned |

## Stack

- **Autopilot:** PX4 + Gazebo Harmonic + ROS 2 Humble
- **Adversarial ML:** Stable-Baselines3, Optuna, DEAP
- **Edge AI:** YOLOv8 on Jetson Nano via TensorRT
- **Infrastructure:** Docker, GitHub Actions, pytest, uv

## Repository

[github.com/fastbunny786/uav-adversarial-testing](https://github.com/fastbunny786/uav-adversarial-testing)
