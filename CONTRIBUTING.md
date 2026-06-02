# Contributing

This is a solo portfolio and research project. External contributions are not being accepted at this stage.

If you have found a bug, have a question, or want to discuss the work, feel free to open an issue.

---

## Development setup (for reference)

**Requirements:**
- Ubuntu 22.04 LTS
- Python 3.12
- [uv](https://docs.astral.sh/uv/)

**Clone and install:**
```bash
git clone git@github.com:fastbunny786/uav-adversarial-testing.git
cd uav-adversarial-testing
uv sync --all-extras --dev
```

**Run tests:**
```bash
uv run pytest -v
```

**Serve docs locally:**
```bash
uv run mkdocs serve
```

---

## Branching and commit conventions

- All work on feature branches, merged to `main` via squash PR
- Commit messages in imperative mood, ≤72 characters
- No direct commits to `main`
