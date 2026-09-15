---
name: cqlib-pulse
description: Build and inspect pulse-level or mixed QCIS circuits with cqlib-pulse in Python, including waveforms, qubit/coupler targets, channel timing, serialization, and Tianyan cloud waveform visualization. Use for PXY, PZ, PZ0, G and pulse scheduling tasks.
---

# Cqlib Pulse

Use public imports from `cqlib_pulse`. Check the target source under
`src/cqlib_pulse/`; it is a standalone Python model, not a subclass or alias
of core `cqlib.Circuit`. Its `Qubit` and `CouplerQubit` types are its own.

- Read [pulses.md](references/pulses.md) for waveform, QCIS and timing rules.
- Read [cloud.md](references/cloud.md) for execution and waveform visualization.
- Start from [pulse_timeline.py](assets/pulse_timeline.py) for an offline
  mixed-channel construction and timing check.

Use the user's local package/environment for unreleased source. Install from
the selected checkout when needed; local waveform construction does not require
logging into Tianyan. Cloud submission and waveform creation are separate
external operations and should follow the user's requested scope.

Keep instruction parameters distinct from waveform shape. Validate target
types, finite numbers, length and channel alignment. Preserve negative
amplitudes where allowed; physical ranges depend on the cloud mapper.
Do not claim local structural checks establish hardware calibration validity.

For core gate compilation or cloud execution use the corresponding installed
skill if available; otherwise inspect that package's source. Never feed pulse
QCIS into the core parser as an assumed lossless conversion.

Verify offline QCIS round trips, PZ0 clock behavior and barriers before any
requested cloud run. Report whether a visualization is a local schedule or
an actual cloud-generated waveform artifact.

## Source fallback

Repository: [github.com/cq-lib/cqlib-pulse](https://github.com/cq-lib/cqlib-pulse).
When local guidance is insufficient, inspect the matching ref's
[public source](https://github.com/cq-lib/cqlib-pulse/tree/main/src/cqlib_pulse)
and [tests](https://github.com/cq-lib/cqlib-pulse/tree/main/tests).
Follow `core/` for targets/instructions/timing, `qcis/` for parsing/export,
and `cloud/` for waveform requests. Replace `main` with the user's revision;
do not assume a newer protocol matches an older installed package.
