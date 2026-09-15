---
name: cqlib-python
description: Write, explain, debug, test, or migrate Python programs that use the modern Cqlib quantum-computing SDK (`cqlib`), including circuits, parameters, ansatz templates, simulation, compilation, devices, QASM/QCIS, and mitigation. Do not use for developing Cqlib itself, Rust or C APIs, provider-specific Tianyan job submission, or unrelated libraries named cqlib.
---

# Cqlib Python Guide

Use the current Rust-backed Cqlib Python SDK to build, transform, simulate, and validate quantum programs. Cqlib is beta: verify names and signatures against the target environment instead of relying on memory.

## Route the Task

| Task | Read |
|---|---|
| Install Cqlib or build a first circuit | [quickstart.md](references/quickstart.md) |
| Build circuits, gates, parameters, ansatz, or control flow | [circuits.md](references/circuits.md) |
| Parse or emit QCIS, OpenQASM 2, or OpenQASM 3 | [formats.md](references/formats.md) |
| Simulate states or calculate QIS quantities | [simulation.md](references/simulation.md) |
| Compile, model devices/noise, or use mitigation | [advanced-workflows.md](references/advanced-workflows.md) |
| Migrate legacy `cqlib.circuits` or `quantum_platform` code | [legacy-api.md](references/legacy-api.md) |

Read only the references required for the request.

## Confirm the API

1. Inspect project dependency files and existing imports.
2. If installed, check `cqlib.__version__`, public signatures, and bundled `.pyi` files.
3. In a Cqlib checkout, treat `crates/binding-python/cqlib/**/*.pyi` and focused Python tests as authoritative for that revision.
4. Use current upstream source only when the local project does not settle the API.

Do not mix the legacy pure-Python `cqlib.circuits` / `cqlib.quantum_platform` API with the modern `cqlib.circuit`, `cqlib.compile`, `cqlib.device`, `cqlib.ir`, and `cqlib.qis` packages. State the assumed version when it cannot be identified.

## Implement

- Prefer public imports from `cqlib` or documented public submodules. Never use `cqlib._native` in user code.
- Preserve qubit ordering and control/target order. Verify endianness with a deterministic case when interpreting arrays or bitstrings.
- Bind symbolic parameters explicitly and keep the returned circuit; do not assume transformations mutate their input.
- Keep local device models distinct from remote service clients. Tianyan authentication and job submission belong to the separate `cqlib-tianyan` domain.
- Use the corresponding `cqlib.ir` module for QASM or QCIS; never use `repr` as an interchange format.
- Keep runnable examples complete, with all imports and no placeholder ellipses.
- Never invent an API based on Qiskit, Cirq, or another Cqlib release.

## Verify

- Run the smallest relevant example or test in the target environment.
- Assert circuit structure, symbol bindings, array shapes, probabilities, expectation values, or serialization semantics as appropriate.
- Use tolerance-based comparisons for floating-point states and matrices; account for global phase where relevant.
- For compilation, verify semantic preservation plus basis, topology, layout, and width constraints.
- For IR conversion, parse emitted output again when supported.
- Report the Cqlib version or source revision tested, commands run, and anything not exercised locally.
