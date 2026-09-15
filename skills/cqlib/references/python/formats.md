# QASM and QCIS

Use `cqlib.ir.qasm2`, `cqlib.ir.qasm3`, or `cqlib.ir.qcis`. Current modules expose `loads`/`load` for strings/files and `dumps`/`dump` for strings/files.

```python
from cqlib.ir import qasm2, qcis

source = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
h q[0];
cx q[0],q[1];
"""

circuit = qasm2.loads(source)
qcis_text = qcis.dumps(circuit)
```

Convert formats through `Circuit`: parse, inspect or transform, then serialize with the target module. Use `str` and `repr` only for diagnostics.

Not every operation is representable in every format. Round-trip representative gates, symbolic parameters, measurement, reset, barriers, and control flow. Compare supported semantics rather than byte-identical formatting. Confirm exception types from the installed stub and behavior rather than assuming all parser failures share one type.

## QCIS boundaries

- Core QCIS `I Qn t` is a delay, not an identity gate. The reviewed Rust
  serializer defines `t` in 0.5 ns ticks; preserve units when crossing into
  pulse code, whose scheduling API uses nanoseconds. Do not assume numeric
  delay arguments have the same meaning across packages.
- Standard identity, explicit global-phase gates, custom gates, and classical
  control/storage are not directly represented by the core serializer.
  Lower supported high-level gates first; do not silently delete unsupported
  operations just to make export succeed.
- Serialization supports more gates than a particular device may execute.
  Compile to the selected device before hardware submission; basis-only
  compilation does not establish topology compatibility.
- `PulseCircuit.from_qcis()`/`to_qcis()` handle pulse instructions. Do not route
  PXY/PZ/PZ0/G text through the core circuit parser as a universal converter.
