---
name: cqlib-vqe
description: Build, run, and validate Python VQE workflows with cqlib-vqe, including molecular Hamiltonians, active spaces, JW/BK/parity mapping, canonical UCCSD, adaptive operator selection, local estimators, and Tianyan grouped measurements. Use for molecular or precompiled-generator VQE tasks in the Cqlib ecosystem.
---

# Cqlib VQE

Use the public `cqlib_vqe` API and verify the target `cqlib_vqe/` source and
core SDK revision. Documentation may call the modern core "cqlib 2.x" while
the Python distribution version uses 1.4 beta; determine capability from the
selected source rather than equating those labels.

- Read [local.md](references/local.md) for estimator/mode selection and a
  precompiled ansatz. [minimal_vqe.py](assets/minimal_vqe.py) needs no molecular
  preprocessing dependencies.
- Read [chemistry.md](references/chemistry.md) for molecules, active spaces,
  mappings, canonical parameters and adaptive pools.
- Read [tianyan.md](references/tianyan.md) for grouped cloud measurement.

Preserve the Hamiltonian, reference state and generator encoding together.
VQE input Pauli lists use q0-left order; the package reverses them when
constructing native core Pauli objects. Do not reverse them again.

Report geometry/basis/charge/multiplicity and active-space policy when relevant,
energy units, reference energies, optimizer settings, evaluation budget and
convergence status. A finite or low energy does not itself establish optimizer
success or chemical accuracy. Start validation with a bounded local case.

Use chemistry dependencies only for molecular preprocessing. Cloud estimators
create repeated measurement tasks; execute only within the user's experiment
scope, with explicit shots and iteration limits. Use the Tianyan skill if
available for client details, otherwise inspect its public binding directly.

## Source fallback

Repository: [github.com/cq-lib/cqlib-vqe](https://github.com/cq-lib/cqlib-vqe).
If local guidance is insufficient, inspect the matching ref's
[implementation](https://github.com/cq-lib/cqlib-vqe/tree/main/cqlib_vqe),
[examples](https://github.com/cq-lib/cqlib-vqe/tree/main/examples), and
[tests](https://github.com/cq-lib/cqlib-vqe/tree/main/tests).
Use `chemistry/` for encoding and active spaces, `vqe/factory.py` for parameters,
and `vqe/tianyan.py` for grouped measurement metadata. Replace `main` with the
user's revision; do not substitute another commit's scientific conventions.
