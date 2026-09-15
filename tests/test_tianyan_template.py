"""Exercise Python submission control flow with a fake SDK, never a cloud client."""

from contextlib import redirect_stderr, redirect_stdout
import io
from pathlib import Path
import runpy
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch


SCRIPT = Path(__file__).resolve().parents[1] / "skills/cqlib-tianyan/assets/submit_qcis.py"


class SubmissionTemplateTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.qcis = Path(self.temporary.name) / "circuit.qcis"
        self.qcis.write_text("X Q0\nM Q0\n", encoding="utf-8")
        self.task = Mock(task_ids=["task-1"])
        self.task.wait.return_value = [SimpleNamespace(task_id="task-1", qubits=[0], counts={"1": 8})]
        self.platform_class = Mock()
        self.backend = self.platform_class.login.return_value.get_backend.return_value
        self.backend.run_with_mode.return_value = self.task
        self.output = io.StringIO()

    def run_template(self, *extra):
        argv = [str(SCRIPT), str(self.qcis), "--backend", "fake-backend",
                "--shots", "8", "--calibration", "disabled", *extra]
        fake_module = SimpleNamespace(TianyanPlatform=self.platform_class)
        with patch.dict(sys.modules, {"cqlib_tianyan": fake_module}), \
             patch.dict("os.environ", {"TIANYAN_API_KEY": "test-only-secret"}), \
             patch.object(sys, "argv", argv), redirect_stdout(self.output), \
             redirect_stderr(io.StringIO()):
            runpy.run_path(str(SCRIPT), run_name="__main__")

    def test_explicit_mode_ephemeral_login_and_task_ids(self):
        self.run_template()
        self.platform_class.login.assert_called_once_with("test-only-secret", save_credentials=False)
        self.backend.run_with_mode.assert_called_once_with(["X Q0\nM Q0\n"], 8, mode="disabled")
        self.task.wait.assert_called_once_with(timeout_secs=120.0, poll_interval_secs=5.0)
        self.assertIn("task-1", self.output.getvalue())
        self.assertNotIn("test-only-secret", self.output.getvalue())

    def test_timeout_preserves_ids_without_resubmitting(self):
        self.task.wait.side_effect = TimeoutError("still pending")
        with self.assertRaises(TimeoutError):
            self.run_template()
        self.backend.run_with_mode.assert_called_once()
        self.assertIn("Submitted task IDs:", self.output.getvalue())
        self.assertIn("task-1", self.output.getvalue())

    def test_mismatched_result_id_is_rejected(self):
        self.task.wait.return_value = [SimpleNamespace(task_id="wrong-task")]
        with self.assertRaisesRegex(ValueError, "task IDs"):
            self.run_template()

    def test_invalid_duration_is_rejected_before_login(self):
        for duration in ("nan", "inf", "0", "-1"):
            with self.subTest(duration=duration), self.assertRaises(SystemExit):
                self.run_template("--timeout", duration)
        self.platform_class.login.assert_not_called()


if __name__ == "__main__":
    unittest.main()
