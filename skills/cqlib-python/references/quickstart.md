# Quickstart

## Environment

Cqlib currently requires CPython 3.10+ and NumPy 2.1+. Follow an existing project pin. For a new isolated environment, upstream documents the beta package as:

```shell
python -m pip install --pre cqlib
```

Binary wheels depend on platform and architecture; building an sdist requires Rust.

## First circuit

```python
from cqlib import Circuit

circuit = Circuit(2)
circuit.h(0)
circuit.cx(0, 1)

matrix = circuit.to_matrix()
assert circuit.num_qubits == 2
assert len(circuit.operations) == 2
assert matrix.shape == (4, 4)
```

## Public modules

| Module | Purpose |
|---|---|
| `cqlib` | Common circuit, compiler, device, and QIS exports |
| `cqlib.circuit` | Circuits, gates, parameters, and classical control |
| `cqlib.circuit.ansatz` | Variational forms and feature maps |
| `cqlib.ir` | QCIS, OpenQASM 2, and OpenQASM 3 |
| `cqlib.qis` | States, Hamiltonians, Pauli objects, entropy, and metrics |
| `cqlib.compile` | Compiler workflows and transforms |
| `cqlib.device` | Devices, topology, layout, noise, and result models |
| `cqlib.error_mitigation` | ZNE and virtual distillation |

Prefer the shortest public import supported by the target version. Do not import `cqlib._native` from application code.
