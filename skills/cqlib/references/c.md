# Cqlib C ABI

## Establish the actual ABI

Inspect the target checkout's `crates/binding-c/src/circuit.rs`, generated
`include/cqlib_c.h`, Cargo build configuration and C examples/tests.
Use a header and library built from the same revision.

The reviewed core C binding exposes circuit construction and parameters only.
It does not export core simulation, compilation, matrices, QCIS/QASM, devices,
or mitigation. Explain unsupported requests and available language boundaries
without inventing C entry points or changing the user's language choice.

The actual names are `circuit_new`, `circuit_h`, `circuit_free`, etc., and the
header is `cqlib_c.h`. The root README's `cqlib_circuit_*` example does not match
this binding. Read [abi.md](c/abi.md) for signatures and failure modes.

## Implement

- Treat `CircuitWrapper` and `ParameterWrapper` as opaque library-owned objects.
  Release them exactly once with their matching library free function.
- Check pointers before access and integer status after each operation.
  Null checks cannot validate dangling or foreign pointers.
- Parameterized append clones its parameter. Binding returns a new circuit;
  the caller owns both original and bound circuits.
- Pass valid NUL-terminated UTF-8 strings. Binding syntax is `theta:0.5,phi:1.0`.
  Validate names and finite numeric values; malformed bindings can be treated
  like absent bindings in this revision.
- `param_evaluate` returns `0.0` for errors as well as valid zero results.
  Do not claim that the ABI provides reliable evaluation-error detection.

Use [the complete C example](../assets/c/circuit_parameters.c) and
[build instructions](c/build.md) for construction and cleanup.
Tianyan's separate C ABI uses a different header, handles and deallocators;
inspect that package rather than treating it as the core binding.

## Verify

Compile and link against the actual generated header/library, then run the
example. Check valid operations, out-of-range status, parameter lifetime and
cleanup. Do not present a mock-header syntax check as runtime ABI validation.
Report missing exports or toolchain limitations explicitly.
