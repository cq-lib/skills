# Tianyan Rust

Use the public `cqlib_tianyan` crate from `crates/cqlib-tianyan`. In a consumer
Cargo project, depend on that local path. This client uses blocking I/O;
it does not require a Tokio runtime for ordinary calls.

The Tianyan workspace depends on core Cqlib through a Git `develop` dependency.
If the consumer also uses core circuits, ensure both dependencies resolve to
the same crate source/revision. Two `cqlib_core::Circuit` types from different
Git/path sources are distinct Rust types even when their names match. Use a
consistent dependency or an explicit local Cargo patch when integrating
checkouts, and record that override.

## Workflow

- `TianyanPlatform::login_with_config(&key, TianyanConfig::default()
  .with_save_credentials(false))` logs in without persisting credentials.
- `list_backends()`/`get_backend(name)` return results; backend `name` and
  `status` are fields. `num_qubits()?` can fetch configuration and includes
  disabled qubits.
- `backend.with_device(|device| ...)` exposes the cached core device by borrow.
  Compile against that device when hardware compatibility is required.
- `backend.run(Vec<CircuitInput>, shots)` accepts QCIS strings via `.into()` or
  core circuit inputs. Converting a circuit to input is not a promise of
  automatic topology routing or device-native compilation.
- `run_with_mode(..., CalibrationMode::Enabled/Disabled/Auto)` selects calibration.
- `task.task_ids()` returns a borrowed slice; save IDs before waiting.
- `task.wait(Duration, Duration)` returns `Result<Vec<ExecutionResult>, TianyanError>`.
  `wait_raw` forces raw results; `status()` returns the completed subset.

Use [submit_qcis.rs](../assets/submit_qcis.rs) as the consumer `src/main.rs`.
It requires a backend, a prepared QCIS file and shots as command-line inputs;
it deliberately uses raw results and does not route the supplied text.
Change the calibration mode explicitly when that is part of the experiment.
Errors propagate through `Result`; timeouts do not cancel or undo submission.

For device compilation use the core Rust skill if available, or inspect core
`compile::CompileConfig` and layout metadata. For offline verification compile
the consumer and run only the package's offline tests; do not invoke its cloud
example merely to check syntax.
