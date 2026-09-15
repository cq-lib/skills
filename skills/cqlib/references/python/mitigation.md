# Error mitigation

The estimator contract in the reviewed Python binding is:

```text
(Circuit, Hamiltonian | None, int | None) -> tuple[float, float]
```

The two outputs represent estimate and variance. Do not return only a float
or a counts dictionary. The observable and shot count may be absent depending
on the workflow. Preserve estimator exceptions.

ZNE accepts nonnegative integer folding levels, not noise multipliers:
levels `[0, 1, 2]` correspond to noise factors `[1, 3, 5]`.

```python
from cqlib import Circuit, Hamiltonian, PauliString, Statevector
from cqlib.error_mitigation import ZNEMitigation

circuit = Circuit(1)
circuit.x(0)
observable = Hamiltonian.from_list([(PauliString.from_str("Z"), 1.0)])
zne = ZNEMitigation(circuit, [0, 1, 2])

def exact_estimator(run_circuit, observable, shots):
    if observable is None:
        raise ValueError("This estimator requires an observable")
    return Statevector.from_circuit(run_circuit).expectation(observable), 0.0

values = zne.run_em_sequence_with_shots(None, observable, 128, exact_estimator)
assert zne.noise_factors == [1, 3, 5]
assert all(abs(value + 1.0) < 1e-10 for value in values)
```

This ideal-state check validates the callback and folding semantics; it does
not demonstrate noise reduction. For a mitigation study, specify the noise
model or execution backend, raw baseline, shots and uncertainty. Density-matrix
noise has separate ideal and readout-adjusted probability APIs; use
`probabilities_with_readout(qubits)` with an explicit qubit list when testing
readout noise, and check the local
stub before configuring `NoiseModel`.

Virtual distillation uses additional copies and numerator/denominator runs.
Account for width, shot allocation and the denominator before reporting a
ratio. Inspect `virtual_distillation.pyi` for `run_vd` and copy-count contracts.
For combined workflows use `ErrorMitigation`, `MitigationMethod`, `RunArgs`,
and `ProcessArgs` from `cqlib.error_mitigation`.
