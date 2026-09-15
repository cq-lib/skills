# Devices and results

`Device`, `Topology`, and `Layout` are local models. They do not authenticate,
submit, query, or cancel a remote job. Even `ExecutionResult.cancel()` only
changes the local result model.

Use the selected backend's `device_config()` for real hardware. A generated
line/grid topology is a synthetic model, not a substitute for calibration and
native-gate capabilities. Read the `device` public stubs for constructors.

For `ExecutionResult`:

- `counts`, `shots`, `qubits`, `status`, and `task_id` are properties.
- `probabilities` can be `None`; `calc_probabilities()` populates normalized
  frequencies from counts.
- Bit i of an outcome corresponds to `qubits[i]`. Use the measured width,
  not the largest physical index, when interpreting bitstrings.
- Check counts, shots, task identity and measured-qubit metadata before
  estimating an observable. Preserve raw versus mitigated provenance.

See [ordering.md](ordering.md) for cross-package conventions. Cloud submission
uses `cqlib_tianyan`; core data-model methods do not perform that work.
