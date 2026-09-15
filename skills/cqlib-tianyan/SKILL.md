---
name: cqlib-tianyan
description: Use cqlib-tianyan from Python, Rust, or C to authenticate with the Tianyan quantum cloud, inspect backends, submit QCIS circuits, poll jobs, and interpret raw or readout-mitigated results. Covers language-specific builds, errors, and C memory ownership for cloud execution workflows.
---

# Tianyan execution

Confirm language, target checkout and source revision. The reviewed Tianyan
branch is `main`; it exposes all three language interfaces. Its Cargo manifest
points to the core repository's `develop` branch: that dependency is not the
Tianyan branch. Check `Cargo.lock` and any local overrides before combining
core types across crates. Use the project's local build for unreleased code.

## Route the task

| Language/task | Read | Example |
|---|---|---|
| Python | [execution.md](references/execution.md) | [submit_qcis.py](assets/submit_qcis.py) |
| Rust | [rust.md](references/rust.md) | [submit_qcis.rs](assets/submit_qcis.rs) |
| C | [c.md](references/c.md) | [submit_qcis.c](assets/submit_qcis.c) |
| Result meaning and calibration | [results.md](references/results.md) | Use the selected language's result accessors |

The submission examples create real cloud jobs when run. Use them only within
the user's authorized experiment scope; compile or test offline otherwise.

Core circuit construction belongs to the matching language guide in `cqlib`;
pulse construction belongs to `cqlib-pulse`. If another skill
is absent, inspect that package's public source. Language interfaces are not
identical: Python uses properties, Rust uses methods, and C uses opaque handles
and result accessors. The core C ABI currently cannot export QCIS itself.

## Execution contract

1. Establish backend, circuit set, shots and requested calibration mode.
2. Inspect device capabilities and the logical/physical mapping before hardware
   execution. Generic QCIS serialization does not validate hardware support.
3. Submit within the user's existing authorization, recording task IDs before
   polling. Code generation or an offline example is not a request to submit.
4. Poll existing tasks with bounded waits. A timeout or ambiguous network
   failure is not evidence that submission failed; do not blindly resubmit.
5. Validate returned task IDs, measured-qubit metadata and counts before using
   results. Retain raw/calibrated provenance with numerical output.

Do not print or embed API keys. Login saves credentials by default; choose
`save_credentials=False` for an ephemeral example. For validation use offline
fixtures unless live execution was requested. Report whether any tasks were
actually submitted and which checks remain offline.

## Source fallback

Repository: [github.com/cq-lib/cqlib-tianyan](https://github.com/cq-lib/cqlib-tianyan).
If the skill or local API does not resolve the task, inspect the target ref's
[Rust source](https://github.com/cq-lib/cqlib-tianyan/tree/main/crates/cqlib-tianyan/src),
[Python binding](https://github.com/cq-lib/cqlib-tianyan/tree/main/crates/binding-python),
or [C binding/header/tests](https://github.com/cq-lib/cqlib-tianyan/tree/main/crates/binding-c).
These links start at `main`; use the user's matching commit for reproducibility.
Read implementation and focused tests when tutorials conflict. Do not switch
to a different API revision or submit a live experiment merely to investigate.
