# Chemistry and adaptive UCCSD

## Molecular workflow

```python
from cqlib_vqe import (
    DirectStatevectorEstimator, MolecularDataEngine, UCCSDFactory, VQESolver,
)

molecule = MolecularDataEngine(
    geometry=[("H", (0.0, 0.0, 0.0)), ("H", (0.0, 0.0, 0.735))],
    basis="sto-3g", multiplicity=1, charge=0, mapper_type="jw",
).run()
factory = UCCSDFactory(molecule, construction_mode="jit", trotter_steps=1, trotter_order=2)
estimator = DirectStatevectorEstimator(n_qubits=molecule.n_qubits)
solver = VQESolver(factory, estimator, max_iter=100, execution_mode="auto")
result = solver.run(molecule.hamiltonian_data)
print(result["optimal_value"], result["success"], result["message"])
print(molecule.reference_energies)
```

This example requires the chemistry extra and performs molecular preprocessing.
Confirm geometry units and record geometry, basis, charge and multiplicity.
Use `molecule.n_qubits`/`n_electrons` rather than estimating width from atoms.

## Active space and encoding

For larger molecules choose `ActiveSpaceConfig.automatic(...)` or an explicit
policy before preprocessing; the maximum active qubit budget is positive and
even. Record `active_space_report` with each numerical result. Full space is
an explicit resource choice, not a default fallback after failure.

The selected `jw`, `bk` or `parity` mapping must be shared by the Hamiltonian,
excitation generators and Hartree–Fock reference. BK/parity reference bitstrings
cannot generally be constructed by simply filling the first occupied qubits.
Use the factory's reference construction and canonical packed-parameter order.

## Adaptive selection

Use the public `AdaptiveSelectedUCCSDSolver` and `AdaptiveSelectionConfig` with
the signatures in the target source and maintained adaptive examples. A zero
CCSD initial amplitude does not remove an excitation from the complete
candidate pool. Select using the intended gradient criterion and preserve
canonical parameter mapping when the ansatz grows. Bound pool scans, optimizer
evaluations and active space; report the selected pool and convergence history.
