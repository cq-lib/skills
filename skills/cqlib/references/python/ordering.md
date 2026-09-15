# Qubit and result ordering

The following conventions are source-specific and must be checked again when
adapting another revision.

| Boundary | Convention |
|---|---|
| Core `Outcome.to_bitstring(n)` | Bit 0 is the rightmost character |
| Core `PauliString.from_str()` | Rightmost character acts on q0 |
| QAOA runner `result["probability"]` | q0 is leftmost; runners already reverse core outcomes |
| VQE list of `(pauli_string, coefficient)` | q0 is leftmost; VQE's Hamiltonian conversion already reverses it |
| `ExecutionResult` | Outcome bit i corresponds to `result.qubits[i]`, not necessarily physical qubit i |

Do not reverse values a second time after an adapter has normalized them.
Track logical indices, physical indices, measurement order, and display order
separately. After routing, retain both initial and final layouts.

Use a two-qubit state with only q0 flipped: core output is `"01"`, whereas the
QAOA runner returns `"10"`. Bell outcomes `00`/`11` cannot detect reversal.
For Pauli conversion, use `ZI` versus `IZ` on an asymmetric state.

Source lookup: core `device/result.pyi`, QAOA
`execution/local_runner.py` and `execution/platform_runner.py`, VQE
`vqe/hamiltonian.py` and `vqe/tianyan.py`.
