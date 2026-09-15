"""Local one-qubit VQE without chemistry preprocessing."""

import math
from cqlib_vqe import DirectStatevectorEstimator, UCCSDFactory, VQESolver

factory = UCCSDFactory.from_compiled(
    n_qubits=1, n_electrons=0,
    generators=[[("Y", 0.5)]], initial_values=[0.1], construction_mode="jit",
)
estimator = DirectStatevectorEstimator(n_qubits=1)
solver = VQESolver(factory, estimator, optimizer_method="COBYLA",
                   max_iter=60, execution_mode="auto")
result = solver.run([("Z", 1.0)])
assert len(result["optimal_params"]) == 1
assert math.isfinite(result["optimal_value"])
assert abs(result["optimal_value"] + 1.0) < 1e-3
print("Energy:", result["optimal_value"])
print("Converged:", result["success"], result["message"])
