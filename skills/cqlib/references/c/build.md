# Build and link

From the selected core repository root:

```shell
cargo build --release -p binding-c
```

The build script generates `crates/binding-c/include/cqlib_c.h` and produces
the platform library under `target/release` (or `CARGO_TARGET_DIR`). It writes
the header into the source tree even when the target directory is elsewhere;
use a writable isolated checkout if the original must remain unchanged.

Copy [circuit_parameters.c](../../assets/c/circuit_parameters.c) into the consumer
project. Set the include/library paths to the matching build. On Unix, the
link library name is `binding_c`, not `cqlib`:

```shell
cc -std=c11 -Wall -Wextra -Werror circuit_parameters.c \
  -I /path/to/cqlib/crates/binding-c/include \
  -L /path/to/cqlib/target/release \
  -Wl,-rpath,/path/to/cqlib/target/release \
  -lbinding_c -lm -o circuit_parameters
./circuit_parameters
```

Replace `/path/to/cqlib` with the selected checkout. For static linking inspect
the Rust toolchain's native library requirements rather than copying a dynamic
link command. Windows needs the matching import library and runtime DLL search
path. Match architecture and toolchain; do not substitute a handwritten header
for the generated ABI. For C++ consumers inspect whether the generated header
has C linkage guards and supply `extern "C"` around inclusion if necessary.
