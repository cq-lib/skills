# Results and readout calibration

In Python, results are core `cqlib.device.ExecutionResult` instances. Access `counts`,
`probabilities`, `qubits`, `shots`, and `task_id` as properties, not methods.
`probabilities` can be absent; `calc_probabilities()` derives frequencies from
counts. Distinguish this normalization from readout-error mitigation.

Rust returns core `ExecutionResult` values with methods such as `counts()` and
`task_id()`. C returns a `TianyanResultList` with length and per-result JSON
accessors; free owned JSON strings. The C header does not expose every Python
result field, including the full measured-qubit list in this revision. Retain
submission metadata and do not infer a missing field from bitstring width.

## Ordering

Outcome bit i corresponds to `result.qubits[i]`. Its displayed string puts
bit 0 at the right. Physical qubit Q107 need not occupy character 107.
Use task identity, the exact measured-qubit list, and the final compilation
layout to recover logical-qubit values. Check result identity/order against
submission metadata before pairing results with circuits or observables.

QAOA runners already reverse strings to q0-left order. VQE's estimator checks
task IDs and measured physical qubits strictly. Do not silently repair metadata
or reverse normalized strings a second time.

## Calibration modes

| Mode                   | Reviewed behavior                                                                                |
|------------------------|--------------------------------------------------------------------------------------------------|
| `auto`                 | Apply when calibration is available and measured width is at most 14; otherwise fall back to raw |
| `enabled`              | Require calibration; check memory before forcing a large-width inverse confusion matrix          |
| `disabled` / `run_raw` | Return raw results                                                                               |

Matrix memory grows as O(4^m) for m measured qubits. Record the requested mode
and distinguish requested automatic mitigation from verified application.
Clipping/normalization can affect the calibrated distribution; keep raw counts
for comparisons. Do not describe calibrated outputs as untouched observations.

`TianyanEnergyEstimator` in the VQE package accepts only enabled/disabled and
rejects `auto` to avoid silent fallback. Preserve that workflow's contract.
