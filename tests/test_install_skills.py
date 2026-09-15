"""Filesystem behavior of the offline installer, isolated in temporary directories."""

import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("install_skills", ROOT / "scripts/install_skills.py")
installer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(installer)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.target = Path(self.temporary.name) / "agent skills"

    def test_selected_skill_contains_references_and_assets(self):
        installer.install(self.target, ["cqlib"])
        self.assertEqual([p.name for p in self.target.iterdir()], ["cqlib"])
        for relative in ("SKILL.md", "agents/openai.yaml", "references/c.md",
                         "assets/rust/core_workflow.rs"):
            self.assertEqual((self.target / "cqlib" / relative).read_bytes(),
                             (ROOT / "skills/cqlib" / relative).read_bytes())

    def test_dry_run_creates_nothing(self):
        installer.install(self.target, installer.SKILLS, dry_run=True)
        self.assertFalse(self.target.exists())

    def test_all_five_install_without_repository_entrypoint(self):
        installer.install(self.target, installer.SKILLS)
        self.assertEqual({path.name for path in self.target.iterdir()}, set(installer.SKILLS))
        self.assertFalse((self.target / "SKILL.md").exists())
        for name in installer.SKILLS:
            self.assertTrue((self.target / name / "SKILL.md").is_file())

    def test_preflight_prevents_partial_install_or_overwrite(self):
        installer.install(self.target, ["cqlib-vqe"])
        sentinel = self.target / "cqlib-vqe/SKILL.md"
        sentinel.write_text("user content", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            installer.install(self.target, ["cqlib", "cqlib-vqe"])
        self.assertFalse((self.target / "cqlib").exists())
        self.assertEqual(sentinel.read_text(), "user content")

    def test_replace_keeps_backup_outside_discovery_and_preserves_legacy(self):
        installer.install(self.target, ["cqlib"])
        (self.target / "cqlib/SKILL.md").write_text("user content", encoding="utf-8")
        legacy = self.target / "cqlib-python"
        legacy.mkdir()
        backup = installer.install(self.target, ["cqlib"], replace=True)
        self.assertEqual((backup / "cqlib/SKILL.md").read_text(), "user content")
        self.assertFalse(backup.is_relative_to(self.target))
        self.assertTrue(legacy.is_dir())
        self.assertTrue((self.target / "cqlib/SKILL.md").read_text().startswith("---"))

    def test_broken_symlink_is_not_followed_or_silently_overwritten(self):
        self.target.mkdir()
        missing = Path(self.temporary.name) / "missing"
        (self.target / "cqlib").symlink_to(missing, target_is_directory=True)
        with self.assertRaises(FileExistsError):
            installer.install(self.target, ["cqlib"])
        backup = installer.install(self.target, ["cqlib"], replace=True)
        self.assertTrue((backup / "cqlib").is_symlink())
        self.assertFalse(missing.exists())

    def test_publish_failure_restores_previous_installations(self):
        installer.install(self.target, ["cqlib"])
        original = self.target / "cqlib/SKILL.md"
        original.write_text("user content", encoding="utf-8")
        rename = Path.rename

        def fail_second_publish(path, destination):
            if path.name == "cqlib-vqe" and path.parent.name.startswith(".cqlib-install-"):
                raise OSError("simulated publish failure")
            return rename(path, destination)

        with patch.object(Path, "rename", fail_second_publish):
            with self.assertRaisesRegex(OSError, "simulated"):
                installer.install(self.target, ["cqlib", "cqlib-vqe"], replace=True)
        self.assertEqual(original.read_text(), "user content")
        self.assertFalse((self.target / "cqlib-vqe").exists())

    def test_source_directory_and_path_traversal_are_rejected(self):
        with self.assertRaises(ValueError):
            installer.install(ROOT / "skills", ["cqlib"], dry_run=True)
        with self.assertRaises(ValueError):
            installer.install(self.target, ["../cqlib"], dry_run=True)


if __name__ == "__main__":
    unittest.main()
