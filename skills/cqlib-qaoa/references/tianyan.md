# QAOA on Tianyan

`cqlib_qaoa.execution.TianYanRunner(login_key=..., machine=...)` logs in during
construction. Creating a runner is not an offline configuration-only operation.
Select an actual backend discovered through the Tianyan client, keep the key
outside code, and set `save_credentials=False` when persistence is unnecessary.

The runner uses core compilation for hardware and converts results into the
algorithm's q0-left distribution. Its simulator-name heuristic and fixed wait
settings are revision-specific; inspect `execution/platform_runner.py` before
configuring a new backend. `need_transpile=False` assumes the circuit is already
valid for the chosen device; it is not a workaround for a routing failure.

Core compilation returns layout metadata under `.device_metadata` in the
reviewed core. Do not assume the runner's legacy `initial_layout` or
`mapping_virtual_to_final` fields contain a complete mapping. For a nontrivial
hardware layout, verify logical-to-physical and result-qubit correspondence
against an asymmetric circuit before trusting objective values. If that
mapping is not established, report the integration limitation.

Budget objective evaluations, shots per evaluation, optimizer-specific extra
evaluations and final sampling. `post_eval` is enabled by default and can
submit another circuit. Keep task IDs before polling, distinguish raw versus
calibrated results, and do not restart a cloud optimization merely because
one wait timed out.
