# Simulation and Quantum Information

## State simulation

```python
import math

from cqlib import Circuit, Statevector

circuit = Circuit(2)
circuit.h(0)
circuit.cx(0, 1)

state = Statevector(2)
state.apply_circuit(circuit)
probabilities = state.probabilities()

assert math.isclose(probabilities[0], 0.5, abs_tol=1e-10)
assert math.isclose(probabilities[3], 0.5, abs_tol=1e-10)
```

Choose the narrowest model:

- `Statevector` for pure ideal states.
- `DensityMatrix` for mixed states.
- `DensityMatrixNoise` for density-matrix evolution with noise.
- `StabilizerState` for supported Clifford workflows.

The primary state models support applying circuits, probabilities, measurements, and shot sampling. Confirm constructors and specialized methods in local stubs. Measurement collapses state; `sample_shots` is non-mutating in the current implementation. Use `Outcome.to_bitstring(width)` to make formatting explicit.

## Sampling and ordering

```python
from collections import Counter
from cqlib import Circuit, Statevector

circuit = Circuit(2)
circuit.x(0)
state = Statevector.from_circuit(circuit)
counts = Counter(outcome.to_bitstring(2) for outcome in state.sample_shots(32))
assert counts == {"01": 32}
assert state.probabilities()[1] == 1.0
```

`sample_shots` returns a list of `Outcome`, not a counts mapping. QAOA runners
already convert these strings to q0-left order; see [ordering.md](ordering.md).

For a subset or reordered measurement, retain the `Measurement` returned by
`circuit.measure_bits(...)`. `state.sample(measurement, shots)` returns an
`ExecutionResult`; `state.probs(measurement)` returns marginal probabilities.
Use the receipt belonging to the intended circuit and verify the order in
`result.qubits`. Circuit measurement construction is distinct from the
collapsing `state.measure(...)` operation. Consult the target simulator tests
before running dynamic measurement/control flow.

## QIS

Use `Pauli`, `PauliString`, and `Hamiltonian` for observables. Use `cqlib.qis.metrics` and `cqlib.qis.entropy` for fidelity, trace distance, purity, entropy, concurrence, and related quantities.

Validate input dimensions, normalization, dtype, subsystem indices, and qubit ordering. Use tolerance-based assertions and deterministic circuits before relying on sampled results.
