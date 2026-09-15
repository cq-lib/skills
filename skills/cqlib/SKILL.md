---
name: cqlib
description: Write, explain, debug, or migrate quantum programs using the Cqlib core SDK from Python, Rust, or C. Covers circuits, parameters, simulation, compilation, devices, QASM/QCIS, mitigation and visualization where exposed by the selected language. Use for SDK consumers, including the core portion of Tianyan, Pulse, QAOA and VQE workflows.
---

# Cqlib core SDK

Choose the project's language and source revision before writing code. Python
and Rust expose broad core workflows; the reviewed C ABI exposes circuit
construction and parameters only. Do not assume feature parity between bindings.

| Language | Read |
|---|---|
| Python | [Python guide](references/python.md) |
| Rust (`cqlib` / `cqlib-core`) | [Rust guide](references/rust.md) |
| C/C++ calling the C ABI | [C guide](references/c.md) |

Read only the relevant language guide and its task-specific references.
For cloud execution use `cqlib-tianyan`; for pulses use `cqlib-pulse`; for a
complete optimization or molecular workflow use `cqlib-qaoa` or `cqlib-vqe`.
If those skills are not installed, inspect the relevant package's public source.

## Resolve API questions from source

Repository: [github.com/cq-lib/cqlib](https://github.com/cq-lib/cqlib).

Prefer the user's installed version, checkout and lockfile. When these guides
do not settle an API or failure, inspect GitHub at the matching branch/tag or
commit. A local unreleased checkout takes precedence over a released package;
do not silently change version or install a different API to make an example work.

Useful upstream source roots (replace `main` with the target ref):

- [Python public package/stubs](https://github.com/cq-lib/cqlib/tree/main/crates/binding-python/cqlib)
  and [Python tests](https://github.com/cq-lib/cqlib/tree/main/crates/binding-python/tests).
- [Rust public core](https://github.com/cq-lib/cqlib/tree/main/crates/cqlib-core/src)
  and [facade crate](https://github.com/cq-lib/cqlib/tree/main/crates/cqlib).
- [C binding, generated header and examples](https://github.com/cq-lib/cqlib/tree/main/crates/binding-c).

Follow public exports to implementation and focused tests. Do not infer an
interface from another language or a stale README. If upstream is inaccessible,
report that limit and use available source without inventing API details.

## Shared correctness rules

- Preserve control/target order, symbolic binding semantics and measurement order.
  Core bitstrings and Pauli displays put q0 on the right; algorithm adapters
  may normalize differently. Test with an asymmetric state.
- Compilation to a basis, topology routing, and strict device-native validation
  are distinct contracts. Retain initial/final physical layouts.
- Matrix and density-matrix storage grows as O(4^n); use bounded validation.
- Test code changes with the smallest relevant consumer example. Report the
  tested revision and distinguish executed checks from source inspection.
