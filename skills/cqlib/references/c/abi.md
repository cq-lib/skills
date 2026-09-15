# Core C ABI contracts

| Surface | Current exports |
|---|---|
| Lifetime | `circuit_new(size_t)`, `circuit_free(CircuitWrapper*)` |
| Inspection | `circuit_num_qubits`, `circuit_num_operations`, `circuit_num_parameters`, `circuit_validate` |
| Fixed gates | `circuit_h/x/y/z(circuit, uint32_t qubit)` |
| Rotations | `circuit_rx/ry/rz(circuit, qubit, double theta)` |
| Two-qubit | `circuit_cx/cz(circuit, first, second)` |
| Directives | `circuit_measure`, `circuit_reset` |
| Parameters | `param_parse`, `param_free`, `param_evaluate` |
| Symbolic rotations | `circuit_rx_param/ry_param/rz_param(circuit, qubit, const parameter)` |
| Bind circuit | `circuit_assign_params(const circuit, const char* bindings)` |

Gate/directive operations return `int32_t`: 0 success, -1 invalid/null argument,
-2 out-of-bounds qubit, -3 core/parameter error. Numeric rotations reject
non-finite angles before checking the circuit pointer. Both qubits of a
two-qubit operation must be valid; an in-range but invalid pair can return -3.

Free functions accept NULL. Size getters return 0 on NULL, so 0 does not prove
a valid empty circuit. Pointer-producing operations can return NULL on failure;
allocation failure/panics are not promised to become ordinary status codes.

`circuit_num_parameters` counts interned symbolic parameters, not necessarily
unbound symbols. The C ABI does not expose the Rust live-symbol query.
Do not require this count to become zero after binding.

`param_evaluate(parameter, bindings)` returns a double with no separate status
channel; errors collapse to 0.0. `circuit_assign_params` passes an optional
parsed map to the core; invalid input can become `None` rather than an explicit
parse error. A non-NULL returned circuit does not prove complete binding.
Validate binding syntax and intended symbol coverage in caller code.

`circuit_measure` appends a measurement operation; it does not execute a circuit
or return a bit. There is no public simulator or serialization export in this
revision. Do not fabricate `circuit_run`, `circuit_to_qcis`, or `last_error`.

The library clones parameters on append, so `param_free` is safe after a
successful symbolic append. Avoid concurrent access to one mutable handle.
Never use C `free` for Rust allocations or share handles with the Tianyan ABI.
