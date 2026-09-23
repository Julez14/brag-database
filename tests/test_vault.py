import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "skills/brag-database/scripts/vault.py"
spec = importlib.util.spec_from_file_location("vault", SCRIPT)
vault = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vault)


class SaveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()

    def test_creates_complete_unicode_note_and_does_not_clobber(self):
        payload = {"path": "Clubs/2026-09 Example — Events.md", "content": "# Draft\nA fictional café event.\n"}
        result = vault.save_note(self.root, payload)
        self.assertEqual(Path(result["path"]).read_text(), payload["content"])
        with self.assertRaises(ValueError):
            vault.save_note(self.root, {**payload, "content": "replacement"})
        self.assertEqual(Path(result["path"]).read_text(), payload["content"])
        self.assertFalse(list(self.root.rglob("*.tmp")))

    def test_revisions_require_current_content_hash(self):
        payload = {"path": "Career/note.md", "content": "Original answer"}
        result = vault.save_note(self.root, payload)
        updated = vault.save_note(self.root, {**payload, "content": "Revised answer", "expected_sha256": result["sha256"]})
        self.assertEqual(Path(updated["path"]).read_text(), "Revised answer")
        with self.assertRaises(ValueError):
            vault.save_note(self.root, {**payload, "expected_sha256": result["sha256"]})
        Path(updated["path"]).unlink()
        with self.assertRaises(ValueError):
            vault.save_note(self.root, {**payload, "expected_sha256": updated["sha256"]})

    def test_rejects_paths_outside_notes(self):
        for name in ["../outside.md", "/tmp/outside.md", ".obsidian/config.md", "Career/../../outside.md", "Career/data.json"]:
            with self.subTest(name=name), self.assertRaises(ValueError):
                vault.save_note(self.root, {"path": name, "content": "no"})
        with tempfile.TemporaryDirectory() as outside:
            (self.root / "escape").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError):
                vault.save_note(self.root, {"path": "escape/outside.md", "content": "no"})


if __name__ == "__main__":
    unittest.main()
