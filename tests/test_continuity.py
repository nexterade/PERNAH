import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ContinuityIntegrityTests(unittest.TestCase):
    def test_boot_snapshot_matches_authoritative_version(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        boot = (ROOT / "PERNAH_BOOT.md").read_text(encoding="utf-8")
        self.assertIn(f"- **Version:** `{version}`", boot)
        self.assertIn("CHAT IS EPHEMERAL. ARTIFACT IS CONTINUOUS.", boot)

    def test_machine_state_matches_authoritative_version_and_next_gate(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        state = json.loads((ROOT / "PERNAH_PROJECT_STATE.json").read_text(encoding="utf-8"))
        self.assertEqual(state["version"], version)
        self.assertEqual(state["schema_version"], 3)
        self.assertEqual(state["expected_test_count"], 164)
        self.assertEqual(state["previous_release"], "0.2.0-dev.59")
        self.assertNotIn("dev.55 ZIP", state["next_release_task"])
        self.assertEqual(state["current_next_gate"], "Project Owner human acceptance for Web Backup & Recovery and remaining exact-artifact UX checks; then reassess Milestone 6 readiness.")
        self.assertTrue(state["chat_is_ephemeral"] if "chat_is_ephemeral" in state else state["continuity_layer"]["chat_is_ephemeral"])

    def test_release_manifest_records_parent_and_current_release(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        manifest = (ROOT / "docs" / "RELEASE-MANIFEST.md").read_text(encoding="utf-8")
        self.assertIn(f"**Version:** `{version}`", manifest)
        self.assertIn("PERNAH-v0.2.0-dev.20.zip", manifest)
        self.assertIn("Current artifact SHA-256", manifest)
        current_block = re.search(r"## Current artifact(.*?)(?=\n## |\Z)", manifest, re.S)
        self.assertIsNotNone(current_block)
        self.assertIn(f"`{version}`", current_block.group(1))
        self.assertNotIn("0.2.0-dev.48", current_block.group(1))


    def test_checkpoint_defines_collaborative_ai_style(self):
        checkpoint = (ROOT / "docs" / "CHECKPOINT.md").read_text(encoding="utf-8")
        self.assertIn("CO-DEVELOPER + PARTNER DISKUSI", checkpoint)
        self.assertIn("COST-AWARE / RESOURCE-AWARE", checkpoint)
        self.assertIn("AI tidak boleh menjadi yes-man", checkpoint)

    def test_boot_snapshot_carries_collaboration_style(self):
        boot = (ROOT / "PERNAH_BOOT.md").read_text(encoding="utf-8")
        self.assertIn("Co-Developer and discussion partner", boot)
        self.assertIn("free/local/offline/low-cost", boot)

    def test_continuity_docs_exist_and_are_linked(self):
        for rel in ["PERNAH_BOOT.md", "PERNAH_PROJECT_STATE.json", "docs/RELEASE-MANIFEST.md"]:
            self.assertTrue((ROOT / rel).is_file(), rel)
        checkpoint = (ROOT / "docs" / "CHECKPOINT.md").read_text(encoding="utf-8")
        self.assertIn("CHAT IS EPHEMERAL. ARTIFACT IS CONTINUOUS.", checkpoint)
        self.assertIn("CHECKPOINT → PERNAH_BOOT → README → STATE", checkpoint)

    def test_active_artifact_hygiene_is_clean(self):
        self.assertFalse((ROOT / "Readme.md").exists())
        changelog = (ROOT / "docs" / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertEqual(changelog.count("# PERNAH — Changelog"), 1)
        self.assertNotIn("pernah.manual.capture_text()", changelog)
        self.assertNotIn("99 unique indexed terms", changelog)
        self.assertGreater((ROOT / "docs" / "TUTORIAL.md").stat().st_size, 0)

    def test_ephemeral_is_a_unique_glossary_entry(self):
        html = (ROOT / "docs" / "Glosarium.html").read_text(encoding="utf-8")
        match = re.search(r"const entries = (\[.*?\]);\s*\n\s*const dict", html, re.S)
        self.assertIsNotNone(match)
        entries = json.loads(match.group(1))
        names = [entry[0].casefold() for entry in entries]
        self.assertEqual(names.count("ephemeral"), 1)
        self.assertEqual(names.count("continuity layer"), 1)
        self.assertEqual(names.count("boot snapshot"), 1)
        self.assertEqual(names.count("release manifest"), 1)
        self.assertEqual(len(entries), 154)


if __name__ == "__main__":
    unittest.main()
