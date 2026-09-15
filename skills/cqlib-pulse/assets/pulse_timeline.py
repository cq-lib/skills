"""Offline construction, round-trip and channel-clock checks."""

from cqlib_pulse import CosineWaveform, CouplerQubit, PulseCircuit, Qubit

q = Qubit(1)
g = CouplerQubit(107)
circuit = PulseCircuit()
circuit.pxy(q, CosineWaveform(length=40, amplitude=0.2),
            frequency=5e9, phase=0.0, drag_alpha=1.0)
circuit.pz(g, CosineWaveform(length=20, amplitude=-0.1), call_mapper=True)
circuit.pz0(g, CosineWaveform(length=10, amplitude=0.0), call_mapper=False)
assert circuit.channel_times == {q: 40, g: 20}
circuit.b(q, g)
assert circuit.channel_times == {q: 40, g: 40}
circuit.delay(q, length=20)
circuit.measure(q)
text = circuit.to_qcis()
restored = PulseCircuit.from_qcis(text)
assert restored.to_qcis() == text
assert restored.channel_times == {q: 60, g: 40}
print(text)
print(restored.schedule())
