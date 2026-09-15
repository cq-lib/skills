# Tianyan C ABI

Build from the Tianyan repository root with `cargo build -p binding-c`.
The generated header is `crates/binding-c/include/cqlib_tianyan.h`; use the
matching `libbinding_c` artifact. Core Cqlib also builds a library called
`libbinding_c`: select explicit paths and keep artifacts separate. A shared
basename does not make these interchangeable libraries or handles.

Use the package's `crates/binding-c/Makefile` for platform-specific static
link flags. For a dynamic Unix consumer, set the include directory, selected
Tianyan library directory and runtime search path. C++ callers use C linkage
as required by the generated header.

## Ownership

| Value | Cleanup |
|---|---|
| `TianyanPlatformC*` | `tianyan_platform_free` |
| `TianyanBackendC*` | `tianyan_backend_free` |
| Backend array | `tianyan_backend_list_free(array, len)` frees elements and array |
| `TianyanTaskC*` | `tianyan_task_free` |
| `TianyanResultList*` | `tianyan_result_list_free` |
| Owned JSON / `tianyan_last_error()` string | `tianyan_string_free` |
| Task-ID array | `tianyan_task_ids_free(array, len)` |
| Borrowed `const char*` getter | Do not free; cannot outlive parent |

Do not free array elements again after the array-specific cleanup. Read the
thread-local error immediately after a failing call; another call may clear
it. Unlike the core C ABI, Tianyan does provide `tianyan_last_error()`.

## Execution

`tianyan_platform_login_with_config` accepts a `TianyanConfigC` with explicit
booleans. A zero-initialized config sets those booleans false; it is not the
same as passing NULL for all defaults. `tianyan_backend_run_with_mode` takes
an array of NUL-terminated QCIS strings, array length, shots, and integer mode:
0 Auto, 1 Enabled, 2 Disabled.

`tianyan_task_wait(task, timeout_secs, poll_interval_secs)` returns a result
list or NULL. Validate finite positive durations in C before calling: the
reviewed binding converts directly with `Duration::from_secs_f64`, and invalid
values may panic rather than return a recoverable error. A successful empty
status snapshot differs from a NULL error result.

Use result length, task ID, shots, and JSON counts/probabilities accessors.
The result task-ID getter is backed by cached `CString` storage. In the
reviewed source, some name getters (including `tianyan_task_device_name`)
return `String::as_ptr()` without establishing NUL termination. Do not use
those getters with `%s`/`strlen`; retain the caller's known name and flag the
binding limitation until corrected. Do not generalize the safe result-ID
implementation to every borrowed string getter.

[submit_qcis.c](../assets/submit_qcis.c) accepts backend, prepared QCIS text,
and shots as arguments, uses raw results, records IDs before waiting, and
cleans up every owned allocation. It creates cloud jobs when executed.
For offline ABI checks, exercise NULL/error paths without constructing a
client. The package's `tests/test_api.c` also calls
`tianyan_platform_from_credentials()` and login with an invalid key; do not
assume that whole test is network-free or isolated from saved credentials.
