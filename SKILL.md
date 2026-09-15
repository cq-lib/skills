---
name: cqlib-ecosystem
description: Navigate the Cqlib quantum-computing ecosystem when using this repository as a single entrypoint. Select the core, Tianyan, pulse, QAOA or VQE guide and the Python, Rust or C interface relevant to the user's program.
---

# Cqlib ecosystem

This is the repository-level entrypoint. Select the relevant guide below and
read its `SKILL.md`, then only the references needed for the current task.
The installation script installs those five skills individually; this root
entrypoint is for agents reading the repository directly, not an additional
skill to install alongside them.

| Task | Guide | Interfaces |
|---|---|---|
| Core circuits, parameters, simulation, compilation and formats | [cqlib](skills/cqlib/SKILL.md) | Python / Rust / C, with different feature coverage |
| Tianyan authentication, backend selection, jobs and results | [cqlib-tianyan](skills/cqlib-tianyan/SKILL.md) | Python / Rust / C on Tianyan main |
| Pulse construction, channel timing and cloud waveform rendering | [cqlib-pulse](skills/cqlib-pulse/SKILL.md) | Python |
| QUBO/Ising mapping and QAOA optimization | [cqlib-qaoa](skills/cqlib-qaoa/SKILL.md) | Python |
| VQE, chemistry preprocessing and energy estimation | [cqlib-vqe](skills/cqlib-vqe/SKILL.md) | Python |

For a cross-library workflow, read the application guide first and add the
core or Tianyan reference only as needed. Do not load every language guide or
assume Python, Rust and C have identical APIs.

Use the user's checkout and dependency lockfiles as the API baseline; these
skills target source APIs that may not match a published package. Each guide
links to its GitHub repository and relevant source/tests. If the guide is
insufficient, inspect local source or GitHub at the matching revision. Report
unavailable source instead of inventing interfaces or silently changing versions.

Code generation and offline testing do not authorize cloud submission.
Keep credentials out of examples and logs, retain submitted task IDs, and do
not automatically resubmit after an ambiguous failure or polling timeout.

For installing these skills, see [README.md](README.md) and
[scripts/install_skills.py](scripts/install_skills.py). Run installation only
when requested, with an explicit destination. It does not build SDKs, change
library branches or install dependencies.
