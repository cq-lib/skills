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

## QIS

Use `Pauli`, `PauliString`, and `Hamiltonian` for observables. Use `cqlib.qis.metrics` and `cqlib.qis.entropy` for fidelity, trace distance, purity, entropy, concurrence, and related quantities.

Validate input dimensions, normalization, dtype, subsystem indices, and qubit ordering. Use tolerance-based assertions and deterministic circuits before relying on sampled results.
