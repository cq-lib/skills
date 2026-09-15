# Rust workflows

## Compilation

Use `compile::{compile, CompileConfig, CompileMode, CompileTarget}`.
`CompileConfig` owns `mode`, `target`, and `resource_policy`.

| Target | Meaning |
|---|---|
| `CompileTarget::Logical` | Logical optimization |
| `CompileTarget::Basis(Vec<Instruction>)` | Explicit standard-gate basis |
| `CompileTarget::Device(DeviceCompileTarget)` | Strict device-native routing, lowering and validation |
| `CompileTarget::TopologyBasis { device_target, basis }` | Topology routing with a custom basis; no device-native guarantee |

`DeviceCompileTarget` owns the device, optional initial layout and optional
seed. A synthetic topology still needs native capabilities for strict
compilation. Use `Device::validate_circuit` to check a hardware target.

`CompileResult` exposes `.circuit`, `.steps`, `.changed`, `.mode`, and optional
`.device_metadata` containing initial and final layouts. For reusable
configuration use `CompilerWorkflow::try_new(config)?` and `.run(&circuit)?`.
`compile_owned`/`run_owned` consume the circuit. Preserve input and output
permutations when checking routed semantics or interpreting measurements.

## Serialization

Use `ir::{qcis, qasm2, qasm3}`. QCIS exposes `loads(&str)` and
`dumps(&Circuit)`, returning results. Inspect format-specific signatures for
file helpers and QASM options. Round-trip through the parser and compare
supported semantics, not exact whitespace.

Core QCIS delay `I Qn t` uses nonnegative integer ticks (0.5 ns in the reviewed
serializer). It is not an identity gate. Explicit identity/global-phase,
custom gates and classical control cannot simply be dumped as QCIS; lower
supported operations first and report remaining limitations. Pulse QCIS is
a separate Python package. Export success does not establish hardware validity.

## Mitigation and visualization

Inspect public re-exports and tests in `error_mitigation/` for `ZNEMitigation`,
`VirtualDistillation`, and `ErrorMitigation`. Folding levels `[0,1,2]` mean
noise factors `[1,3,5]`; copy count and estimator uncertainty matter. Use the
Rust callback bounds and result types from that revision, not Python aliases.
Model the noise or execution backend explicitly before claiming improvement.

Use public `visualization` functions for circuit/state/result rendering;
check options and output types there. Keep rendered display ordering separate
from data ordering.
