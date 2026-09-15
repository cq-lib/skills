# Visualization

Use the public `cqlib.visualization` module. Its circuit and plot functions
return SVG/text, not Matplotlib figures.

```python
from cqlib import Circuit
from cqlib.visualization import draw_figure, draw_text

circuit = Circuit(2)
circuit.h(0)
circuit.cx(0, 1)
text = draw_text(circuit)
svg = draw_figure(circuit)
assert isinstance(text, str) and text
assert "<svg" in svg
```

`draw_figure(..., output_path="circuit.svg")` saves an artifact when requested.
`plot_histogram` and `plot_distribution` take an `ExecutionResult`, not an
arbitrary counts dictionary. `plot_bloch_multivector`, `plot_state_city`, and
`plot_state_paulivec` accept supported state objects. Inspect the visualization
stub for options; `reverse_bits` changes the display, not the stored circuit.

Use pulse scheduling and cloud visualization APIs for pulse timelines.
