# Rust circuits and simulation

## Local setup

Use the toolchain required by the checkout's Cargo metadata. In a separate
consumer project, add one local dependency (replace the path):

```toml
[dependencies]
cqlib-core = { path = "/path/to/cqlib/crates/cqlib-core" }
```

Alternatively depend on `crates/cqlib` and import `cqlib::...`; it re-exports
the same public modules. Do not add both merely to access the same API.

Copy [core_workflow.rs](../../assets/rust/core_workflow.rs) into the consumer's
`src/main.rs` and run `cargo run`. The example uses only the core dependency.

## Circuit and parameter semantics

Public imports include `circuit::{Circuit, Qubit, Parameter, Instruction,
StandardGate}`. `Circuit::new(n)` creates the circuit; gate operations return
results. Numeric rotations accept numbers, symbolic rotations accept
`Parameter::symbol("theta")`. Clone a reusable parameter when passing ownership.

Binding takes `&Option<HashMap<&str, f64>>`, not a Python dict or an in-place
flag. Check `bound.used_symbols().is_empty()` for unresolved dependencies;
the interned parameter table is not the live symbol set.

Dynamic classical construction is under `circuit` and `circuit_classical.rs`.
The reviewed `assign_parameters` rejects classical-control instructions. Verify
construction, binding and execution independently before promising dynamic
control support for an entire workflow.

## Simulation and observables

`qis::{Statevector, DensityMatrix, DensityMatrixNoise, StabilizerState}` expose
different models. `Statevector::from_circuit(&circuit)` returns a result;
`apply_circuit(&mut self, &Circuit)` changes an existing state.
`Statevector::new(n)` creates the zero state. `probabilities()` returns a vector.

`sample_shots(shots)` returns `Vec<Outcome>`. `Outcome::to_bitstring(width)`
prints q0 on the right. `measure`/`measure_all` collapse the state. Circuit
`measure_bits` returns a `Measurement` receipt; simulator `sample`/`probs`
use that receipt for selected-qubit order and marginals.

Use `qis::{Hamiltonian, PauliString, Observable}` for expectation values.
Inspect their constructors and coefficient types in `qis/hamiltonian.rs` and
`qis/pauli/` before converting an external model. External VQE Pauli lists
and QAOA result strings use q0-left order; convert once at the boundary.
