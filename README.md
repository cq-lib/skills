# Cqlib Skills

Agent skills for using Cqlib. The current skill helps an AI agent write,
explain, debug, test, and migrate Python programs with the Cqlib SDK.

## What the Skill Does

### `cqlib-python`

[`cqlib-python`](skills/cqlib-python/SKILL.md) covers:

- circuits, gates, parameters, and ansatz templates;
- state simulation and quantum-information utilities;
- QCIS, OpenQASM 2, and OpenQASM 3;
- compilation, devices, layouts, and noise models;
- error mitigation; and
- migration from the legacy Cqlib Python API.

It is for Python code that uses Cqlib. It does not cover developing Cqlib
itself, Rust or C APIs, or Tianyan job submission.

When the skill is active, the agent is instructed to confirm the API from the
installed Cqlib version or the current source stubs instead of relying on
remembered interfaces. It should use public Cqlib modules, keep parameter and
qubit ordering explicit, and run a relevant check after writing code.

## How to Use

1. Install or load the complete `skills/cqlib-python/` directory in the agent.
2. Start a new session if the agent discovers skills only at startup.
3. Invoke `cqlib-python` explicitly, or ask the agent to use Cqlib Python.

The exact location and invocation syntax depend on the agent:

| Agent | Install or load | Invoke |
|---|---|---|
| Codex | `~/.codex/skills/cqlib-python/` or `<project>/.agents/skills/cqlib-python/` | `$cqlib-python ...` |
| Claude Code | `~/.claude/skills/cqlib-python/` or `<project>/.claude/skills/cqlib-python/` | `/cqlib-python ...` |
| Other agents | Import the complete `cqlib-python` directory if Agent Skills are supported | Agent-specific |

### Codex

Install the skill for the current user:

```shell
mkdir -p ~/.codex/skills
ln -s /absolute/path/to/cqlib-skill/skills/cqlib-python \
  ~/.codex/skills/cqlib-python
```

Alternatively, put the directory under
`<project>/.agents/skills/cqlib-python/` to use it only in one project. Start a
new session, then invoke it explicitly:

```text
$cqlib-python Create a parameterized circuit and verify the bound result.
```

Codex can also select it automatically when the request clearly mentions using
Cqlib Python.

### Claude Code

Install the skill for the current user:

```shell
mkdir -p ~/.claude/skills
ln -s /absolute/path/to/cqlib-skill/skills/cqlib-python \
  ~/.claude/skills/cqlib-python
```

Alternatively, put the directory under
`<project>/.claude/skills/cqlib-python/`. Start a new session, then invoke it
with Claude Code's slash syntax:

```text
/cqlib-python Create a Bell-state circuit and verify its probabilities.
```

Claude Code can also select it automatically from a request that clearly
mentions Cqlib Python.

### TeleAgent and Other Agents

If an agent such as TeleAgent does not support Agent Skills directly, give it
the complete skill directory or ask it to read `SKILL.md` and the referenced
file required for the task. A remote agent must receive uploaded files because
it cannot read a path on the local computer.

For an agent that can read local files, use:

```text
Read /absolute/path/to/cqlib-python/SKILL.md and follow its instructions for
this request. Load only the reference required for the task.
```

For a remote agent, upload the complete directory. Uploading only `SKILL.md`
omits the task-specific material under `references/`.

If the platform has an Agent Skills import page, import the complete
`cqlib-python` directory and use the invocation syntax shown by that platform.

### Custom GPT and Model APIs

For a custom GPT, put the main instructions from `SKILL.md` in its Instructions
and upload the files under `references/` as Knowledge.

For a direct model API, the calling program must provide `SKILL.md` and the
relevant reference in the model context. A model API does not discover local
skill directories or implement `$cqlib-python` by itself.

Example request:

```text
Use Cqlib Python to create a Bell-state circuit and verify its probabilities.
```

## What the Skill Includes

```text
skills/cqlib-python/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    ├── advanced-workflows.md
    ├── circuits.md
    ├── formats.md
    ├── legacy-api.md
    ├── quickstart.md
    └── simulation.md
```

- `SKILL.md` is the entry point. Its YAML frontmatter identifies when the
  skill applies, and its Markdown body defines routing and working rules.
- `agents/openai.yaml` contains optional Codex interface metadata.
- `references/` contains focused instructions loaded only when needed.

### `SKILL.md`

The YAML frontmatter contains:

- `name`: the skill identifier, `cqlib-python`;
- `description`: the supported Cqlib tasks and the boundaries that prevent the
  skill from being selected for unrelated requests.

The Markdown body contains four parts:

- **Route the Task** maps a request to the appropriate reference;
- **Confirm the API** explains how to identify the Cqlib version and check
  public signatures;
- **Implement** records important Cqlib usage rules;
- **Verify** describes the checks to perform after producing code.

### `agents/openai.yaml`

This optional file provides the display name, short description, and suggested
prompt used by compatible Codex interfaces. Other agents can use the skill
without this file.

### `references/`

| Reference | Read it for |
|---|---|
| `quickstart.md` | Installing Cqlib, creating a first circuit, or choosing public imports |
| `circuits.md` | Building circuits, gates, parameters, control flow, transformations, or ansatz templates |
| `formats.md` | Reading, writing, or converting QCIS and OpenQASM programs |
| `simulation.md` | Simulating states or calculating observables, metrics, and entropy |
| `advanced-workflows.md` | Compiling circuits or working with devices, layouts, noise, results, and mitigation |
| `legacy-api.md` | Updating programs written with the legacy Cqlib Python API |

References are not intended to be loaded together for every request. For
example, a circuit-construction request normally uses `circuits.md`, while a
QCIS conversion request normally uses `formats.md`.

The loading flow is:

```text
User request
    → select cqlib-python from its name and description
    → read SKILL.md
    → read the relevant reference
    → check the installed Cqlib API or source stubs
    → write and verify the Cqlib program
```
