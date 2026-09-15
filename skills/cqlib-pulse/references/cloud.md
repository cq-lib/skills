# Pulse cloud integration

## Execute a prepared pulse circuit

Submit `[circuit.to_qcis()]` with a selected `cqlib_tianyan` backend. Use
`task.wait(timeout_secs=..., poll_interval_secs=...)`. PulseCircuit itself
does not select devices, submit jobs, or poll hardware results. Keep channel
IDs and hardware calibration assumptions with the experiment.

## Cloud waveform visualization

The package provides `TianyanWaveformClient.from_api_key(...)` and
`CloudPulseVisualizer(client)` independently of the execution client.

```python
from cqlib_pulse import CloudPulseVisualizer, TianyanWaveformClient

def create_visualization(circuit, api_key):
    api = TianyanWaveformClient.from_api_key(api_key)
    visualizer = CloudPulseVisualizer(api)
    job = visualizer.create(circuit, circuit_name="pulse-example", is_verify=True)
    return job, visualizer
```

This function creates a remote waveform job when called. Save `job.query_id`
before waiting. `visualizer.query(job)` returns a URL or `None`;
`visualizer.wait(job, timeout_secs=300, poll_interval_secs=3)` waits for a URL.
`visualizer.visualize(...)` combines creation and waiting. It returns a cloud
artifact URL, not a local plot or hardware measurement result.

Authentication uses the package's token provider; the reviewed client refreshes
and retries once after HTTP 401. Do not add unlimited login/create retries or
create another job solely because an existing job timed out.
Use a fake `WaveformAPI` for offline validation of create/query behavior.
