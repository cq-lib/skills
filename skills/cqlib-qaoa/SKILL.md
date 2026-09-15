---
name: cqlib-qaoa
description: Solve and debug combinatorial optimization problems with cqlib-qaoa in Python, including MaxCut, TSP, VRP, QUBO/Ising conversion, QAOA optimization, local sampling, Tianyan execution, and solution decoding. Use for complete optimization workflows rather than only constructing a core QAOA ansatz.
---

# Cqlib QAOA

Inspect the target source in `cqlib_qaoa/`, its requirements and focused tests.
Use `QAOASolver`, `QAOAConfig`, `OptimizerOptions` and the problem/mapping APIs
provided by the package; avoid rebuilding a solver from core circuit primitives.
Preserve explicit user choices of algorithm, optimizer and backend.

- Read [optimization.md](references/optimization.md) for the local workflow,
  parameter ordering and correctness checks.
- Read [tianyan.md](references/tianyan.md) when selecting `TianYanRunner`.
- Use [maxcut.py](assets/maxcut.py) for a small local example with an exact
  classical reference and a separate bit-order check.

Core `cqlib.circuit.ansatz` builders and this package's solver have different
contracts. A request to solve a problem needs model conversion, optimization,
sampling and decoding. A request for one ansatz may only need the core SDK.

Before reporting success, validate problem feasibility, objective sign and
constant offset, parameter length and bit ordering. Report the sampled result
and classical bound separately; a short stochastic run does not certify a
global optimum. Record shots, optimizer settings and stopping conditions.

Cloud execution follows the user's requested experiment scope and budget.
Use the Tianyan skill if installed for submission details, or inspect its public
API. Local validation should not instantiate an authenticated cloud runner.

## Source fallback

Repository: [github.com/cq-lib/cqlib-qaoa](https://github.com/cq-lib/cqlib-qaoa).
When the skill and local code do not settle the issue, inspect the matching
ref's [implementation](https://github.com/cq-lib/cqlib-qaoa/tree/main/cqlib_qaoa)
and [tests](https://github.com/cq-lib/cqlib-qaoa/tree/main/tests).
Start at `mappings/` for objective conventions, `algorithms/qaoa/` for solver
returns, `execution/` for backend normalization, and `results/` for decoding.
Replace `main` with the target revision and preserve that version's contracts.
