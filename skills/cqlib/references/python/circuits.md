# Circuits, Parameters, and Ansatz

## Circuit construction

```python
from cqlib import Circuit, Parameter

theta = Parameter("theta")
circuit = Circuit(2)
circuit.h(0)
circuit.rx(1, theta)
circuit.cx(0, 1)

bound = circuit.assign_parameters({"theta": 0.5})
assert bound is not circuit
assert bound.used_symbols == []
```

Use integers or `Qubit` objects as allowed by the local stub. Common methods cover fixed gates, rotations, controlled gates, interactions, barriers, reset, delay, and measurement. Check `cqlib/circuit/circuit.pyi` for exact argument order—especially controls, targets, and parameter positions.

`symbols` and `used_symbols` are properties. `symbols` can retain interned but unused names; `used_symbols` is the live dependency list. `assign_parameters` returns a circuit and has no legacy `inplace` option.

## Inspect and transform

Relevant surfaces include `operations`, `depth()`, `dag()`, `inverse()`, `decompose()`, `to_gate(name)`, `compose(...)`, `to_matrix()`, `to_symbolic_matrix()`, and `validate()`. Confirm mutation semantics from the installed stub and tests; copy before a mutating composition when the source must be preserved.

Measurements and dynamic control flow introduce non-unitary behavior, so matrix-based validation may no longer apply.

`Circuit.measure()` and `measure_bits()` return a `Measurement` receipt,
not counts or the circuit. Keep that receipt for simulator `sample()`/`probs()`
and preserve the requested measurement order. See [simulation.md](simulation.md).

## Custom gates

Use `CircuitGate`, `MCGate`, `StandardGate`, and `UnitaryGate` through their documented append methods. Validate custom matrix shape and unitarity. Supply multi-control qubits in the exact order required by the current signature.

## Dynamic circuits

Use `Circuit.var()` and classical expressions for runtime state. Build `if_`, `if_else`, `while_`, `for_uint`, and `switch` bodies through callbacks; callback bodies are transactional. Use `measure_into` or `measure_bits_into` for existing classical targets. Inspect the local classical type/expression stubs before constructing literals or stores.

Construction, binding, simulation, compilation, and export have different
control-flow support. The reviewed core `assign_parameters` rejects circuits
containing classical control; do not promise that a constructible dynamic
circuit can also be bound or exported to QCIS.

## Ansatz

Use `cqlib.circuit.ansatz` builders for two-local circuits, feature maps, QAOA, and Hamiltonian evolution. Builder APIs evolve, so inspect the corresponding `.pyi` and a focused test before selecting method names.

After building an ansatz, verify its width, `used_symbols`, optimizer-vector length, parameter sharing, and entangling edges. Bind a small instance and compare it with a known state or expectation value.
