# Cqlib Skills

[English](README.md) | [简体中文](README.zh-CN.md)

Agent skills for the Cqlib quantum-computing ecosystem, grounded in the
repositories' source APIs rather than an assumed PyPI release.

## Skills and source repositories

| Skill | Languages | Scope | Upstream repository |
|---|---|---|---|
| [cqlib](skills/cqlib/SKILL.md) | Python / Rust / C | Core circuits and parameters; simulation, compilation, formats, devices and mitigation where exposed | [cq-lib/cqlib](https://github.com/cq-lib/cqlib) |
| [cqlib-tianyan](skills/cqlib-tianyan/SKILL.md) | Python / Rust / C | Authentication, backends, QCIS submission, polling, calibration and results | [cq-lib/cqlib-tianyan](https://github.com/cq-lib/cqlib-tianyan) |
| [cqlib-pulse](skills/cqlib-pulse/SKILL.md) | Python | Pulse QCIS, waveforms, channel timing and cloud visualization | [cq-lib/cqlib-pulse](https://github.com/cq-lib/cqlib-pulse) |
| [cqlib-qaoa](skills/cqlib-qaoa/SKILL.md) | Python | QUBO/Ising mapping, local optimization and Tianyan execution | [cq-lib/cqlib-qaoa](https://github.com/cq-lib/cqlib-qaoa) |
| [cqlib-vqe](skills/cqlib-vqe/SKILL.md) | Python | Local VQE, chemistry preprocessing and Tianyan energy estimation | [cq-lib/cqlib-vqe](https://github.com/cq-lib/cqlib-vqe) |

The former `cqlib-python` entry and the C/Rust guides are consolidated into
`cqlib`: one repository, one skill, with language-specific references. The
reviewed core C ABI supports circuit construction and parameters, not the full
Python/Rust feature set. Tianyan's **main** branch has all three interfaces;
its Git dependency on core `develop` is a separate branch choice.

Every skill links to its repository and relevant source/test directories.
When a guide is insufficient, the agent should inspect the user's checkout
first, then matching GitHub source at the relevant commit, tag or branch.
It should not assume that PyPI contains the reviewed API or silently switch
versions. If GitHub is inaccessible, it should report that limitation.

## Install the skills

Use `npx skills` for agent-aware installation, or the bundled Python installer
for offline copies to an explicit directory. Both install skills, not SDKs.
Use one installation method per destination; their update/backup mechanisms
are independent.

### Option 1: npx skills

Requires Node.js/npm; remote Git sources also require Git and network access.
The [Vercel Skills CLI](https://github.com/vercel-labs/skills#install-a-skill)
supports selecting skills, agents and project/global installation scope.
Run remote installation commands from the project where the skills are needed:

```shell
# Inspect available entries without installing
npx skills add cq-lib/skills --full-depth --list

# Install the unified core skill; choose agents in the prompts
npx skills add cq-lib/skills --full-depth --skill cqlib

# Install all five library skills
npx skills add cq-lib/skills --full-depth \
  --skill cqlib cqlib-tianyan cqlib-pulse cqlib-qaoa cqlib-vqe
```

The root `SKILL.md` is a repository navigator. The CLI normally stops discovery
at a root skill, so these commands use `--full-depth` and select library names
explicitly. The listing also includes `cqlib-ecosystem`; do not install it
alongside the five library skills. Avoid `--all` or `--skill '*'` when using
the repository root. See the [discovery implementation](https://github.com/vercel-labs/skills/blob/main/src/skills.ts).

Installation is project-scoped by default. For a global installation targeting
Codex, for example:

```shell
npx skills add cq-lib/skills --full-depth \
  --skill cqlib cqlib-tianyan --agent codex --global
```

Use `--agent claude-code` for Claude Code, or select agents interactively.
`--copy` selects independent copies instead of symlinks; review the CLI's
destination and overwrite prompts before proceeding. These flags belong to
`npx skills`, not to our Python installer.

GitHub commands install the contents published in `cq-lib/skills`, not local
uncommitted changes. If this revision is not yet pushed, or `--list` still
shows only `cqlib-python`, use the local checkout. From this repository root:

```shell
npx skills add ./skills --list
npx skills add ./skills --skill cqlib cqlib-tianyan
```

Pointing directly at `./skills` discovers only the five library skills and
needs no `--full-depth`. To install them into another project, run there and
replace `./skills` with the absolute path to this checkout's `skills/` folder.
For a fork or unpublished branch, use the corresponding GitHub repository/tree
URL instead of assuming upstream already contains the changes.

### Option 2: bundled Python installer

Requires Python 3.10+; this installer uses only the standard library and does
not download packages, build SDKs, modify agent configuration or submit jobs.
Run it from this checkout (or use an absolute path to the script).

Choose the skills directory configured for your agent and substitute it for
`/path/to/agent/skills`. The destination is required: no global installation
is selected implicitly.

```shell
python3 scripts/install_skills.py --list
python3 scripts/install_skills.py --target /path/to/agent/skills --dry-run
python3 scripts/install_skills.py --target /path/to/agent/skills
```

To install only selected skills, repeat `--skill`:

```shell
python3 scripts/install_skills.py --target /path/to/agent/skills \
  --skill cqlib --skill cqlib-tianyan
```

The installer copies complete skill directories, including references,
examples and UI metadata. Copies remain usable after this checkout is moved;
rerun the installer to pick up updates. It refuses existing destinations by
default. To update while preserving the previous installation:

```shell
python3 scripts/install_skills.py --target /path/to/agent/skills \
  --skill cqlib --replace
```

Backups are saved in a timestamped directory under the destination's sibling
`skills-backups/` (or `<destination-name>-backups/` for another directory
name), outside skill discovery. The exact location is printed. Restore by
moving the new installation aside and moving the corresponding backup back
to its original path.

Old `cqlib-python`, `cqlib-rust` and `cqlib-c` installations are reported but
not removed. After reviewing the merged `cqlib` skill, move old installations
outside the agent's discovery directory to avoid overlapping entries.
The Python installer leaves unrelated skills untouched. Use your agent's reload
procedure after installation.

SDK source-build instructions belong to each language guide; this script
installs **skills only**.

## Repository entrypoint and invocation

The root [SKILL.md](SKILL.md) is a single navigation entrypoint for an agent
reading this repository directly. It routes to the relevant library and
language; it is not a sixth skill installed alongside the five library skills.
Use the standard uppercase filename `SKILL.md`.

For explicit invocation in an agent supporting `$skill-name`:

```text
$cqlib Use Rust to bind a circuit parameter and verify its probabilities.
$cqlib Write a C consumer using the generated header, with correct cleanup.
$cqlib-tianyan Prepare a C QCIS submission program; do not submit a live job.
$cqlib-pulse Build a pulse sequence and check its channel timing locally.
$cqlib-qaoa Solve weighted MaxCut and verify the objective sign and bit order.
$cqlib-vqe Run a minimal local VQE without chemistry dependencies.
```

For agents without skill discovery, provide the root `SKILL.md` and access
to the full repository, or supply the selected skill directory. Uploading
only the entrypoint omits its references. A direct model API needs the
calling application to supply those files; an invocation string alone does
not make local files available.

## Layout and examples

```text
SKILL.md                    Repository-level navigation
scripts/
  install_skills.py          Selective install, preview and backup/update
  validate_skills.py         Links, syntax and optional offline examples
tests/                      Installer and mocked Tianyan template tests
skills/
  cqlib/                    Python / Rust / C language routing
  cqlib-tianyan/             Python / Rust / C execution guides
  cqlib-pulse/
  cqlib-qaoa/
  cqlib-vqe/
```

Each installed skill has a `SKILL.md`, `agents/openai.yaml`, focused
`references/`, and example templates under `assets/`. Load only the
references needed for the current task.

Offline examples:

- [Core Rust](skills/cqlib/assets/rust/core_workflow.rs): parameter binding,
  asymmetric ordering, basis compilation and QCIS round-trip.
- [Core C](skills/cqlib/assets/c/circuit_parameters.c): parameter ownership,
  circuit binding and error returns.
- [Pulse timing](skills/cqlib-pulse/assets/pulse_timeline.py): channel clocks,
  barriers and QCIS round-trip.
- [QAOA MaxCut](skills/cqlib-qaoa/assets/maxcut.py): exact objective enumeration,
  bit ordering and bounded local optimization.
- [Minimal VQE](skills/cqlib-vqe/assets/minimal_vqe.py): a one-qubit variational
  problem with a known ground-state energy.

Tianyan includes [Python](skills/cqlib-tianyan/assets/submit_qcis.py),
[Rust](skills/cqlib-tianyan/assets/submit_qcis.rs) and
[C](skills/cqlib-tianyan/assets/submit_qcis.c) submission templates. Running
them with valid arguments and credentials submits real jobs. They do not
embed keys or automatically resubmit after a polling timeout. Confirm the
backend, shots, calibration mode and submission authority first.

## Validation and maintenance

Dependency-free checks:

```shell
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests -v
```

With the source-built Python SDKs and their dependencies in the active
environment, run the allowlisted local examples:

```shell
python3 scripts/validate_skills.py --offline-examples
```

This runs core Python snippets plus Pulse/QAOA/VQE examples, never the cloud
submission templates. Compile C/Rust examples separately against the matching
source/header using their language guides. Validate each skill and the root
entrypoint with `skill-creator`'s `quick_validate.py` when available.

[tianyan_c_null.c](tests/tianyan_c_null.c) exercises the real Tianyan C ABI's
NULL/error/cleanup paths without loading credentials or constructing a client.
Compile it with Tianyan's generated include path and library (the same
link setup as the C submission template), then run it locally.

This review used local source revisions:

| Repository           | Reviewed commit |
|----------------------|-----------------|
| cqlib (main)         | `1d0a2c4`       |
| cqlib-tianyan (main) | `4bd2b79`       |
| cqlib-pulse          | `63bdd3e`       |
| cqlib-qaoa           | `c3c952d`       |
| cqlib-vqe            | `b173554`       |

These are review baselines, not required dependency pins. When APIs change,
check public exports, stubs/generated headers, implementation and focused
tests together. Rust consumers sharing `Circuit` with Tianyan must resolve
the same core crate identity, not just the same package version.

Keep offline and live-cloud validation separate: mocks and compilation do
not establish backend availability, authentication or actual hardware
behavior. Chemistry examples additionally require their optional chemistry
dependencies.

Keep the English and Chinese READMEs aligned when changing installation
commands, skill names, supported interfaces or review baselines. Skill
instructions remain a single maintained set; translating this README does
not create duplicate skills.
