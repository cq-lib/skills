# VQE cloud measurement

Use `TianyanEnergyEstimator` with a selected backend and
`VQESolver(..., execution_mode="circuit")`. Install a compatible Tianyan client
alongside the local VQE/core source.

Construct the estimator with explicit `n_qubits`, `shots`,
`calibration_mode="enabled"` or `"disabled"`, and `physical_qubits` when using
a hardware mapping. Entry i of that mapping is the physical qubit for logical
qubit i. It must have exactly `n_qubits` distinct valid entries.

The estimator groups qubit-wise commuting (QWC) Pauli terms, adds basis changes
and measurements, and batches circuits. The base circuit must not already
contain measurements. Basis decomposition happens before physical remapping;
it does not provide an arbitrary hardware routing strategy. Verify interactions
and the selected physical subgraph before submitting.

`grouping="none"` provides a useful small comparison against grouping.
`measure_only_support` affects the measured-qubit list and count width.
Preserve the strict task-ID, result-order and `result.qubits` checks in
`vqe/tianyan.py`; do not silently repair mismatched metadata.

Automatic calibration is rejected by this estimator because the client can
fall back to raw results. Do not replace its explicit mode with the client's
default. Record the measurement plan, grouping, shots, physical mapping and
task IDs with the energy result.

An optimization step can execute several grouped circuits. Budget total
objective calls, group count, shots and final evaluations. Poll existing task
handles after a timeout where supported; restarting the entire VQE can submit
duplicate experiments. Offline tests should use the package's backend/result
fixtures and never require a real API key.
