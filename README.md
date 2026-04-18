# UAV Adversarial GNSS Testing Framework

An open-source hardware-in-the-loop test framework that uses adversarial
machine learning to automatically discover navigation failure modes in
PX4-based UAVs under GPS-denied and GPS-spoofed conditions.

## Status

🚧 **Phase 0 — Project setup.** No runnable code yet. This repository is
under active initial construction.

## Why this project

GPS-denied and GPS-spoofed UAV navigation is a growing real-world problem,
but validation against GNSS attacks is still largely manual and ad hoc.
This project builds automated, reproducible, adversarial test infrastructure
for PX4-based quadcopters, starting in simulation (PX4 SITL + Gazebo
Harmonic) and extending to real hardware (Holybro X500 + Pixhawk, HITL).

## Roadmap

- **Phase 0** — Project infrastructure (this phase)
- **Phase 1** — PX4 SITL + Gazebo end-to-end baseline
- **Phase 2** — GNSS failure scenario injection
- **Phase 3** — Adversarial scenario generation (RL, Bayesian opt, evolutionary)
- **Phase 4** — Scaled, reproducible experiment infrastructure
- **Phase 5** — Hardware-in-the-Loop on Pixhawk + Holybro X500

## License

MIT — see [LICENSE](LICENSE).

## Author

WaqasA
