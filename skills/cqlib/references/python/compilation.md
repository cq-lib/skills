# Compilation

Import `compile` and `CompileTarget` from `cqlib.compile`.

| Inputs | Contract |
|---|---|
| No target | Logical optimization |
| `target_basis=[...]` | Explicit output basis |
| `device=device` | Strict device-native compilation, routing and validation |
| `device=device, target_basis=[...]` | Route on the topology and lower to the chosen basis; no device-native guarantee |

`CompileTarget.logical()`, `.basis(...)`, `.device(...)`, and
`.topology_basis(...)` express these contracts explicitly. Do not combine
`target` with loose `device`/`target_basis` arguments. `seed` controls layout
and routing heuristics, not all randomness in an experiment.

## Small basis-compilation example

```python
import numpy as np
from cqlib import Circuit
from cqlib.compile import compile

source = Circuit(2)
source.h(0)
source.cx(0, 1)
result = compile(source, target_basis=["H", "CZ"])
assert len(source.operations) == 2
assert result.steps
left = source.to_matrix()
right = result.circuit.to_matrix()
overlap = np.vdot(left.ravel(), right.ravel())
assert abs(overlap) > 0
phase = overlap / abs(overlap)
np.testing.assert_allclose(right, phase * left, atol=1e-10)
```

For a real backend, obtain `device = backend.device_config()` and compile
with `device=device`. Keep `result.circuit` and
`result.device_metadata.initial_layout` / `.final_layout` together. The metadata
is absent for logical/basis-only compilation. A topology-only model without
native capabilities is insufficient for strict native compilation.

Check output instructions, ordered physical couplings, capacity and layout.
For routed circuits, account for both input and output permutations before
comparing states/matrices. Width can grow with physical indices or ancillas;
do not compare unequal-size matrices or allocate a full device-width matrix.
Use bounded logical test cases and mapped measurements instead.
