# Compilation, Devices, and Mitigation

These APIs evolve quickly. Inspect `cqlib/compile/**/*.pyi`, `cqlib/device/**/*.pyi`, or `cqlib/error_mitigation/**/*.pyi` from the target version before writing constructor arguments.

## Compilation

The standard compiler is `cqlib.compile.compile`; the top-level package exports it as `compile_circuit`. It returns a `CompileResult`, not only a circuit. Read its compiled circuit, layout/metadata, `changed` state, and step reports according to the current stub.

Use `CompileConfig` and `CompilerWorkflow` when explicit mode, target basis, device, layout, resource policy, or seed control is required. Use individual `cqlib.compile.transform` functions only when stage-level control is necessary.

Validate both semantics and target compliance:

- required native/target basis;
- permitted topology edges for two-qubit operations;
- device width and physical layout;
- representative parameter bindings;
- nonmutation of the source where promised.

## Devices and results

Use `Device`, `Topology`, and `Layout` for local hardware models. Standard device constructors include line, ring, star, grid, and edge-based forms in the current API. Model characterization with the public noise/property types supported by the installed version.

`Status`, `Outcome`, and `ExecutionResult` are local data models; they do not submit jobs. Keep provider submission and polling in an adapter and translate responses at that boundary. Preserve qubit/bit ordering and validate that counts agree with shots.

## Error mitigation

Use `cqlib.error_mitigation` for ZNE, virtual distillation, and unified mitigation workflows. Confirm fold levels, extrapolation method, copy count, callback signature, and result type locally before implementation.

Estimator callbacks must follow the exact current contract and preserve underlying exceptions. Test invalid configuration and repeated state transitions. Mitigation does not replace a physically meaningful noise/execution model.
