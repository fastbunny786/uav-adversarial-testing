# ADR-002: Repository Strategy — Single Public Spine Repo

**Date:** 2026-06-07
**Status:** Accepted

---

## Context

At project start, two repos existed:

- `uav-adversarial-testing` (public) — the spine project, started fresh
  with professional structure from commit #1.
- `px4-sitl-ci` (private) — a scratch repo used to prove the SITL concept
  worked: Holybro X500 in Gazebo Harmonic, headless mission flying a 20m
  square, GitHub Actions on a self-hosted runner. It contained hard-won
  gotchas (PX4 v1.17 topic versioning asymmetry, QoS durability, preflight
  circuit breaker parameters) but was written as exploratory code, not
  portfolio-quality engineering.

The question was how to handle `px4-sitl-ci` once the spine repo was
established: consolidate it, keep it separate, or delete it.

---

## Decision

**Delete `px4-sitl-ci` entirely. Do not consolidate it into the spine repo.**

The spine repo (`uav-adversarial-testing`) is the single public repo for
all project work. All new code is written directly here to portfolio
standard from the start.

---

## Rationale

**Against consolidation:**
Importing scratch-quality exploratory code into a portfolio repo would
pollute the commit history and contradict the project's core standard:
professionally structured from commit #1, reproducible by a stranger.
A hiring engineer reading the repo history should see deliberate,
well-reasoned commits — not a bulk import of learning debris.

**Against keeping `px4-sitl-ci` as a separate public repo:**
A second public repo with lower-quality code would undermine the portfolio
signal of the spine repo. It would also create maintenance overhead and
confusion about which repo is authoritative.

**For deletion:**
The knowledge gained in `px4-sitl-ci` (SITL gotchas, QoS settings,
circuit breaker parameters) transfers to the engineer, not to the code.
That knowledge is re-expressed in clean, documented form in the spine repo
as it becomes relevant — starting with the MAVSDK mission orchestrator
and the PX4 SITL stack decision in ADR-001.

---

## Consequences

- All SITL knowledge from `px4-sitl-ci` must be re-implemented in the
  spine repo to portfolio standard. No copy-paste from the deleted repo.
- The self-hosted runner (`fastbunny53-ubuntu`) was de-registered from
  `px4-sitl-ci` and will be re-registered against the spine repo when
  CI headless SITL missions are implemented in Phase 1.
- Future exploratory work follows the same pattern: scratch privately,
  ship cleanly to the spine repo once the approach is validated.
