# Local VQE

Install the selected local checkout with its core, NumPy and SciPy dependencies.
The chemistry extra adds PySCF/OpenFermion preprocessing; a precompiled generator
ansatz does not need it. Do not build a molecule merely to evaluate an existing
Hamiltonian and ansatz.

Use `UCCSDFactory.from_compiled` with `n_qubits`, `n_electrons`, generators and
initial values when preprocessing is already done. Each generator is a list
of `(pauli_string, coefficient)` terms in the package's q0-left convention.
Use [minimal_vqe.py](../assets/minimal_vqe.py) for a one-qubit energy check.

| Choice | Purpose |
|---|---|
| `DirectStatevectorEstimator` | Fused local parameter evaluation |
| `NativeStatevectorEstimator` | Circuit/statevector expectation evaluation |
| `execution_mode="auto"` | Select direct execution when factory and estimator support it |
| `execution_mode="circuit"` | Circuit-oriented estimators, including cloud |
| `execution_mode="direct_statevector"` | Requires compatible factory and estimator methods |
| `construction_mode="jit"` | Build numerical circuits per evaluation |
| `construction_mode="bind"` | Use symbolic templates and binding |

`VQESolver.run(hamiltonian_data)` returns a dictionary with `optimal_value`,
`optimal_params`, `n_evals`, `n_iters`, `success`, `message`, `execution_mode`
and `history`. Preserve the optimizer message and budget in reports. A short
COBYLA run can reach a good energy while reporting `success=False` because
its evaluation budget is exhausted.

For cross-checks compare direct and circuit estimators on the same bound
parameters and Hamiltonian. Check asymmetric Pauli operators, normalization,
parameter dimensions and a small exact reference. Avoid asserting global
optimality from a stochastic or budget-limited run.
