# Local optimization

Build a problem from `cqlib_qaoa.problems`, convert it with
`cqlib_qaoa.mappings`, and supply the Ising Hamiltonian to `QAOASolver`.
Select `LocalRunner` for local statevector sampling. Use the project's source
installation and dependency set; do not replace its core SDK with another API.

## Contracts

- `QAOAConfig.reps = p` uses a flat vector of length `2*p` ordered as
  `[gamma_0, ..., gamma_(p-1), beta_0, ..., beta_(p-1)]`, not interleaved pairs.
- `shots` belongs to `QAOAConfig`; repeated objectives and final `post_eval`
  consume additional samples. A seed for one optimizer is not a global
  sampling seed; inspect the selected optimizer's supported options.
- `QAOASolver.run()` returns `QAOAResult` in the reviewed implementation,
  despite an outdated dictionary return annotation. Access `.theta_opt`,
  `.fun`, `.history`, `.result_raw`, and `.ising` as attributes.
- `result_raw["probability"]` is the distribution key. Final sampling errors
  may instead appear as `post_eval_error`; do not treat that as a distribution.
- Runner result strings put q0 on the left. Local and cloud runners already
  perform this conversion; the core `Outcome` display puts q0 on the right.
- The Ising human-readable Pauli display uses its own q0-right convention;
  it is not an interchange format for algorithm bitstrings.

Keep QUBO sense and constant offset through conversion. `maxcut_to_qubo`
represents maximization; `qubo_to_ising` converts to a minimization objective.
For a small case compare `energy_of_bitstring` against the original cut weight
for every assignment. Use ordinary problem definitions rather than assuming
that a lower Ising energy numerically equals a larger cut weight.

For TSP/VRP, record variable indexing, fixed depot/start choices, penalties and
constraints. Decode with the package's problem-specific result utilities and
verify route feasibility separately from energy. Selecting the largest
probability bitstring alone does not establish a valid route.

Use `.plot_history`, `.plot_probability`, and problem-specific plotting methods
only after valid result data exists. Use numerical checks for automated tests;
plots need not open a GUI during a local verification run.
