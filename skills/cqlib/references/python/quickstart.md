# Quickstart

## Environment

Cqlib requires CPython 3.10+ and NumPy 2.1+ in the reviewed source. Follow the
project's environment and source revision. For an unreleased checkout, build
inside an activated virtual environment, from the core repository root:

```shell
maturin develop --release -m crates/binding-python/Cargo.toml
```

This requires Maturin and the Rust toolchain specified by the checkout. An
existing wheel can instead be installed by its explicit local path. Do not
upgrade from a package index to resolve a source/API mismatch. Confirm both
`cqlib.__version__` and `cqlib.__file__`; building Python bindings uses
`crates/binding-python/Cargo.toml`, whose version can differ from the workspace.

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
| `cqlib.visualization` | Text/SVG circuits, state plots, and result plots |

Prefer the shortest public import supported by the target version. Do not import `cqlib._native` from user code.
