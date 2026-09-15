# Pulse model and QCIS

| Waveform | Protocol ID |
|---|---|
| `NumericWaveform` | -1 |
| `CosineWaveform` | 0 |
| `FlattopWaveform` | 1 |
| `SlepianWaveform` | 2 |

Waveforms contain length, amplitude and shape-specific values. `PXY` owns
frequency, phase and `drag_alpha`; `PZ`/`PZ0` own `call_mapper`. Use
`core/waveforms.py` and `core/instructions.py` for exact constructors and
numeric constraints. Do not fabricate device frequency or amplitude limits.

Targets are `Qubit(n)` (Qn) and `CouplerQubit(n)` (Gn). Coupler IDs are opaque
hardware identifiers, not arithmetic encodings of two logical qubits. Use
explicit target objects when the channel type matters.

`PulseCircuit.to_qcis()` serializes; `.from_qcis(text)` restores supported
operations. `.load(text)` is a compatibility alias. `qcis_dumps`/`qcis_loads`
are also public. This package supports a subset of ordinary QCIS gates along
with pulse instructions; inspect `qcis/parser.py` for the actual opcode set.

## Channel timing

- Lengths and `ScheduledOperation.start_ns/end_ns` are in nanoseconds.
- PXY/PZ/G/I advance the corresponding channel clock.
- PZ0 has a waveform duration but does not advance the channel clock.
- B aligns the listed channels to their maximum current time.
- Ordinary operations other than I/B do not advance clocks in the reviewed
  scheduler; the timeline is not a complete hardware gate-duration simulation.

Inspect `schedule()` and `channel_times`. Independent channels can overlap;
an ordered operation list does not imply global serialization.
Core QCIS delays use integer ticks in its serializer (0.5 ns in the reviewed
source). Do not assume equal numeric values across core and pulse delay APIs
mean equal physical durations; verify the target protocol at that boundary.
