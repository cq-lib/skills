# Legacy Python API Migration

Legacy code commonly imports `cqlib.circuits`, `cqlib.quantum_platform`, `cqlib.mapping`, `cqlib.simulator`, `cqlib.utils`, or `cqlib.benchmark`. It may use direct gate classes, `Circuit.qcis`, `Circuit.load`, `Circuit.to_qasm2`, `inplace=`, `cache_params=`, `StatevectorSimulator`, or platform clients.

Do not perform blind name replacement. Classify each symbol as retained, renamed, moved, behaviorally changed, or absent; then verify the modern stub and a focused test.

Common directions:

| Legacy surface | Modern direction |
|---|---|
| `cqlib.circuits` | `cqlib.circuit` |
| `Circuit.qcis` / `Circuit.load` | `cqlib.ir.qcis.dumps` / `loads` |
| `Circuit.to_qasm2()` | `cqlib.ir.qasm2.dumps` |
| sequence or in-place parameter binding | `assign_parameters(dict[str, float])`, keeping its return |
| `StatevectorSimulator` | `cqlib.qis.Statevector` workflow |
| mapping/transpilation helpers | current compiler, device, layout, and routing workflow |
| `TianYanPlatform` / `GuoDunPlatform` | separate provider/adapter integration; no `cqlib.device` substitute |

Gate and directive names, argument order, operation storage, sampling results, bit ordering, visualization, and platform execution all require behavioral migration—not just import changes.

Migration sequence:

1. Inventory imports, symbols, and intended behavior.
2. Rewrite imports, then calls and result handling.
3. Replace serialization, simulation, and compilation with explicit modern modules.
4. Add assertions for return types, mutation, ordering, exceptions, and numerical tolerance.
5. Build the current extension and run focused tests.
6. State unsupported legacy behavior explicitly rather than claiming compatibility.
