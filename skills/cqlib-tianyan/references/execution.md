# Python authentication and execution

Inspect `crates/binding-python/cqlib_tianyan/__init__.pyi` and binding source.
Python result conversion and `device_config()` require compatible core `cqlib`
even though the packaging metadata lists it as optional. Confirm module paths.

For a local source build, activate the intended environment and run
`maturin develop --release -m crates/binding-python/Cargo.toml` from the Tianyan
repository. Build/install the matching core Python package for device and
result conversion. Do not infer the Python API from an older root README.

## Discover a backend without submitting

```python
import os
from cqlib_tianyan import TianyanPlatform

platform = TianyanPlatform.login(
    os.environ["TIANYAN_API_KEY"], save_credentials=False
)
for backend in platform.list_backends():
    print(backend.name, backend.status)
```

Login and listing still perform network requests. `from_credentials()` reuses
saved credentials; refresh can write updated credentials according to config.
Use actual backend names returned by the service rather than hardcoded examples.
`backend.num_qubits()` includes disabled qubits and is not a usable-qubit list.

## Core-to-device preparation

The following function prepares QCIS from a core circuit with the requested
measurement instructions already attached:

```python
from cqlib.compile import compile
from cqlib.ir import qcis

def prepare_for_backend(circuit, backend):
    device = backend.device_config()
    compiled = compile(circuit, device=device)
    return qcis.dumps(compiled.circuit), compiled.device_metadata
```

Retain metadata for result decoding. A supplied custom basis plus topology
does not guarantee native compatibility. An already mapped pulse QCIS file
uses its own protocol; do not send it through the core compiler/parser.

## Submission and polling

`backend.run(list[str], shots)` returns a `TaskHandle` after submission.
Use `run_raw` for disabled calibration or
`run_with_mode(circuits, shots, mode="enabled")` for explicit calibration.
The client splits batches into at most 50 circuits per request; avoid redundant
batching unless the application needs additional budget control.

`task.wait(timeout_secs=120, poll_interval_secs=5)` returns results.
`wait_raw` uses the same parameter names and forces raw results.
`task.status()` queries once and may return only completed circuits. Its
returned list is not a list of all job statuses; absence does not mean failure.

Save task IDs and circuit ordering as soon as submission returns. A wait timeout
does not cancel jobs. Reuse the task handle while available; inspect current
public recovery/query APIs for process restarts rather than inventing a
`TaskHandle(task_ids)` constructor or automatic resubmission.

Some tutorials disagree on exception behavior. Inspect the installed exception
class and binding; do not promise that all errors are catchable as
`TianyanError`. If a boundary catches `Exception` for reporting, preserve the
original error and do not turn it into a success or unconditional retry.
