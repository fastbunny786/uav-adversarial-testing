# ADR #001 — ROS 2 Humble on Ubuntu 22.04 LTS

**Date:** 2026-04-26  
**Status:** Accepted

---

## Context

This project requires a ROS 2 distribution to interface PX4 with the adversarial test orchestration layer. Two candidates were evaluated:

- **ROS 2 Humble** on Ubuntu 22.04 LTS
- **ROS 2 Jazzy** on Ubuntu 24.04 LTS

ROS 2 Jazzy is the current LTS release as of 2024. A naive stack selection would default to the newest LTS. However, this is a PX4-centric project, and PX4's own documentation is the authoritative source for stack compatibility.

---

## Decision

**Ubuntu 22.04 LTS + ROS 2 Humble.**

PX4's ROS 2 User Guide explicitly states:

> "The supported and recommended ROS 2 platform for working with PX4 is ROS 2 Humble LTS on Ubuntu 22.04."

This recommendation reflects the reality that PX4's build system, Docker images, forum answers, and community tutorials are overwhelmingly written against Humble + 22.04. Deviating from this combination introduces friction at every integration point.

---

## Consequences

**Positive:**
- Full alignment with PX4's official recommended platform
- Maximum compatibility with PX4 tutorials, Docker images, and community support
- Reduced integration risk across the entire Phase 1–6 arc

**Negative:**
- ROS 2 Humble reaches end-of-life in May 2027
- A planned migration to ROS 2 Jazzy + Ubuntu 24.04 will be required in late 2026 or early 2027
- This migration is a known future cost, accepted deliberately

**Rejected alternative:**
ROS 2 Jazzy on Ubuntu 24.04 was rejected because it is off the PX4-recommended path. While it works for generic ROS 2 development, the additional integration effort for a PX4-centric project outweighs the benefit of running the newer distribution.

---

## Notes

This decision was reached after an initial incorrect recommendation (Jazzy) was caught and corrected via pushback during project planning. It is documented here so future contributors understand the constraint is PX4-driven, not arbitrary.
