# Cqlib Rust

## Identify the target

Inspect `Cargo.toml`, `Cargo.lock`, existing imports and the source revision.
The `cqlib` crate currently re-exports `cqlib_core::*`; the package
`cqlib-core` is imported as `cqlib_core`. Keep the crate already used by the
project. For unpublished work use the user's local path dependency.

The public modules and signatures in `crates/cqlib-core/src/` are authoritative.
Do not translate Python methods mechanically: Rust constructors, errors,
borrowing, parameters and compile configuration differ.

## Route the task

| Task | Reference |
|---|---|
| Set up, construct, bind, or simulate a circuit | [circuits-simulation.md](rust/circuits-simulation.md) |
| Compile, target a device, serialize, mitigate, or visualize | [workflows.md](rust/workflows.md) |

Start from [the runnable example](../assets/rust/core_workflow.rs) for a small
parameterized circuit, asymmetric state check, basis compilation and QCIS
round trip. Read only the relevant reference.

## Essential contracts

- Gate calls generally mutate `&mut Circuit` and return `Result<(), CircuitError>`;
  handle errors before continuing. Use `Qubit::new(index)` for circuit qargs.
- `assign_parameters(&Some(HashMap<&str, f64>))` returns a new circuit.
- `compile(&circuit, config)` preserves the caller's circuit;
  `compile_owned(circuit, config)` transfers ownership.
- State measurement mutates the state; `sample_shots(&self, ...)` does not.
  Core bitstrings and Pauli strings put q0 on the right.
- Compilation and serialization have separate target contracts. Preserve
  physical layout metadata and validate ordered gate capabilities.
- Full state storage grows as O(2^n), full matrices as O(4^n). Use small
  semantic checks and resource-appropriate production methods.

For cloud work use the public Rust `cqlib-tianyan` crate and its source;
local device models do not submit jobs. Pulse, QAOA and VQE packages reviewed
here expose Python workflows; do not invent Rust equivalents.

## Verify

Compile/run the smallest relevant consumer example against the selected
checkout. Check a non-palindromic bitstring, parameter exhaustion, semantic
equivalence up to global phase, and topology/layout where applicable.
Report the source revision, toolchain and checks actually run. Do not rebuild
all language bindings for an ordinary Rust usage task.
