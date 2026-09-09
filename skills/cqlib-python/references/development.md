# Python Binding Development

The Python binding lives under `crates/binding-python/`:

```text
crates/binding-python/
├── pyproject.toml
├── cqlib/        # Public Python modules and .pyi stubs
├── src/          # PyO3 implementation
└── tests/        # Python binding tests
```

## Build and test

From the Cqlib repository root in an activated environment:

```shell
python -m pip install "maturin>=1.10,<2"
maturin develop -m crates/binding-python/Cargo.toml
pytest crates/binding-python/tests/
```

Run a focused test first while iterating. Run relevant Cargo tests when shared Rust behavior changes. Follow repository lint, format, and pre-commit configuration.

## Binding invariants

- Update PyO3 signatures, exports, docstrings, Python wrappers, `.pyi` declarations, and tests together.
- Use the established exception hierarchy; do not leak Rust panics into Python.
- Keep mutation/return behavior explicit and consistent.
- Keep NumPy dtype, shape, dimensionality, and contiguity requirements consistent.
- Verify defining-submodule and intended top-level imports.
- Release the GIL for substantial Rust computation only where the established safety pattern permits it.

The distribution is typed and includes `py.typed`; stale stubs are a public API defect. Packaging checks must ensure Python sources, stubs, and `py.typed` are included while local native artifacts and caches are excluded.

For diagnostics, locating `cqlib._native` is acceptable, but application code must not import it directly.
