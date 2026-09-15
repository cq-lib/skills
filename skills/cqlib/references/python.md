# Cqlib Python Guide

Use the current Rust-backed Cqlib Python SDK to build, transform, simulate, and validate quantum programs. Cqlib is beta: verify names and signatures against the target environment instead of relying on memory.

## Route the Task

| Task | Read |
|---|---|
| Install Cqlib or build a first circuit | [quickstart.md](python/quickstart.md) |
| Build circuits, gates, parameters, ansatz, or control flow | [circuits.md](python/circuits.md) |
| Parse or emit QCIS, OpenQASM 2, or OpenQASM 3 | [formats.md](python/formats.md) |
| Simulate states or calculate QIS quantities | [simulation.md](python/simulation.md) |
| Compile, model devices/noise, or use mitigation | [advanced-workflows.md](python/advanced-workflows.md) |
| Draw circuits, states, or measurement results | [visualization.md](python/visualization.md) |
| Interpret bitstrings, Pauli strings, or cross-package results | [ordering.md](python/ordering.md) |
| Migrate legacy `cqlib.circuits` or `quantum_platform` code | [legacy-api.md](python/legacy-api.md) |

Read only the references required for the request.

For a complete optimization problem use `cqlib-qaoa`; for molecular VQE use
`cqlib-vqe`. Core ansatz builders only construct circuits. `cqlib-pulse` owns
pulse circuits and `cqlib-tianyan` owns cloud execution. Use those skills if
installed for the corresponding part of a combined task; otherwise inspect
that package's public source and tests. Do not assume sibling skills are installed.

## Confirm the API

1. Inspect project dependency files and existing imports.
2. If installed, check `cqlib.__version__`, public signatures, and bundled `.pyi` files.
3. In a Cqlib checkout, treat `crates/binding-python/cqlib/**/*.pyi` and focused Python tests as authoritative for that revision.
4. Record the source revision and module location for development builds;
   version strings alone do not identify unreleased interfaces. If stubs and
   behavior disagree, inspect the binding implementation and focused tests.
   Do not substitute a released package for the user's local checkout.

Do not mix the legacy pure-Python `cqlib.circuits` / `cqlib.quantum_platform` API with the modern `cqlib.circuit`, `cqlib.compile`, `cqlib.device`, `cqlib.ir`, and `cqlib.qis` packages. State the assumed version when it cannot be identified.

## Implement

- Prefer public imports from `cqlib` or documented public submodules. Never use `cqlib._native` in user code.
- Preserve qubit ordering and control/target order. Verify endianness with a deterministic case when interpreting arrays or bitstrings.
- Bind symbolic parameters explicitly and keep the returned circuit; do not assume transformations mutate their input.
- Keep local device models distinct from remote service clients. Tianyan authentication and job submission belong to the separate `cqlib-tianyan` domain.
- Use the corresponding `cqlib.ir` module for core QASM or QCIS; pulse QCIS belongs to `cqlib_pulse`. Never use `repr` as an interchange format.
- Keep runnable examples complete, with all imports and no placeholder ellipses.
- Never invent an API based on Qiskit, Cirq, or another Cqlib release.

## Verify

- When producing or changing runnable code, run the smallest relevant example or test in the target environment. Explanation-only tasks need only relevant inspection.
- Assert circuit structure, symbol bindings, array shapes, probabilities, expectation values, or serialization semantics as appropriate.
- Use tolerance-based comparisons for floating-point states and matrices; account for global phase where relevant.
- For compilation, verify semantic preservation plus basis, topology, layout, and width constraints.
- For IR conversion, parse emitted output again when supported.
- Report the Cqlib version or source revision tested, commands run, and anything not exercised locally.
- Use full matrices only for small cases: statevectors require O(2^n) storage,
  while density matrices and circuit matrices require O(4^n). Verify larger
  tasks with bounded examples, structural constraints, or suitable observables.
