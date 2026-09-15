"""Submit an explicitly selected QCIS file; this program creates cloud jobs."""

import argparse
import math
import os
from pathlib import Path

from cqlib_tianyan import TianyanPlatform


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("qcis_file", type=Path)
    parser.add_argument("--backend", required=True)
    parser.add_argument("--shots", required=True, type=int)
    parser.add_argument("--calibration", required=True,
                        choices=["auto", "enabled", "disabled"])
    parser.add_argument("--timeout", type=float, default=120.0)
    args = parser.parse_args()
    if args.shots <= 0 or not math.isfinite(args.timeout) or args.timeout <= 0:
        parser.error("shots and timeout must be positive; timeout must be finite")
    circuit = args.qcis_file.read_text(encoding="utf-8")
    if not circuit.strip():
        parser.error("QCIS file is empty")
    platform = TianyanPlatform.login(
        os.environ["TIANYAN_API_KEY"], save_credentials=False
    )
    backend = platform.get_backend(args.backend)
    task = backend.run_with_mode([circuit], args.shots, mode=args.calibration)
    print("Submitted task IDs:", task.task_ids, flush=True)
    results = task.wait(timeout_secs=args.timeout, poll_interval_secs=5.0)
    if [result.task_id for result in results] != list(task.task_ids):
        raise ValueError("Returned task IDs/order differ from submission")
    for result in results:
        print(result.task_id, result.qubits, result.counts)


if __name__ == "__main__":
    main()
