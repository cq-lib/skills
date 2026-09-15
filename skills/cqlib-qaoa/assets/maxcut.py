"""Small local QAOA run with exact objective and ordering checks."""

from itertools import product
import math

from cqlib import Circuit
from cqlib_qaoa.algorithms import QAOAConfig, QAOASolver
from cqlib_qaoa.execution import LocalRunner
from cqlib_qaoa.execution.objective import energy_of_bitstring
from cqlib_qaoa.mappings import maxcut_to_qubo, qubo_to_ising
from cqlib_qaoa.optimizers import OptimizerOptions
from cqlib_qaoa.problems import MaxCut

weights = {(0, 1): 1.0, (1, 2): 2.0}
problem = MaxCut(n=3, weights=weights)
ising = qubo_to_ising(maxcut_to_qubo(problem))

def cut_weight(bits):
    return sum(weight for (i, j), weight in weights.items() if bits[i] != bits[j])

assignments = ["".join(bits) for bits in product("01", repeat=3)]
for bits in assignments:
    assert math.isclose(energy_of_bitstring(ising, bits), -cut_weight(bits), abs_tol=1e-10)
classical_optimum = max(map(cut_weight, assignments))

asymmetric = Circuit(2)
asymmetric.x(0)
_, ordered = LocalRunner().run_circuit(asymmetric, num_shots=8)
assert ordered["probability"] == {"10": 1.0}

solver = QAOASolver(
    ising, runner=LocalRunner(),
    qaoa_cfg=QAOAConfig(reps=1, shots=128, verbose=False),
    opt_cfg=OptimizerOptions(name="cobyla", options={"maxiter": 12, "tol": 1e-3}),
)
result = solver.run(initial_theta=[0.8, 0.2], verbose=False)
assert len(result.theta_opt) == 2 and math.isfinite(result.fun)
distribution = result.result_raw["probability"]
assert math.isclose(sum(distribution.values()), 1.0, abs_tol=1e-10)
best_observed = max(distribution, key=cut_weight)
print("Classical optimum:", classical_optimum)
print("Best observed:", best_observed, cut_weight(best_observed))
print("Sampled objective:", result.fun)
