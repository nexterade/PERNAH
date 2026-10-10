import ast
import json
import re
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$")
RELEASE = re.compile(r"^0\.2\.0-dev\.(\d+)$")


class ReleaseIntegrityTests(unittest.TestCase):
    def test_version_is_valid_and_matches_release_artifact(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertRegex(version, SEMVER)
        self.assertRegex(version, RELEASE)
        self.assertEqual(version, "0.2.0-dev.71")

    def test_versioned_documents_are_synchronized(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        required = [
            "PERNAH_BOOT.md", "PERNAH_CONTINUATION.md", "PERNAH_PROJECT_STATE.json",
            "README.md", "docs/STATE.md", "docs/CHANGELOG.md", "docs/RELEASE-MANIFEST.md"
        ]
        for rel in required:
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn(version, text, rel)
        state = json.loads((ROOT / "PERNAH_PROJECT_STATE.json").read_text(encoding="utf-8"))
        self.assertEqual(state["version"], version)

    def test_release_lineage_is_monotonic_and_changelog_declares_parent(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        n = int(RELEASE.fullmatch(version).group(1))
        manifest = (ROOT / "docs/RELEASE-MANIFEST.md").read_text(encoding="utf-8")
        m = re.search(r"## " + re.escape(version) + r".*?Parent artifact:\s*`PERNAH-v0\.2\.0-dev\.(\d+)(?:-[0-9A-Za-z.-]+)?\.zip`", manifest, re.S)
        self.assertIsNotNone(m)
        self.assertLess(int(m.group(1)), n)
        self.assertIn(f"## {version}", (ROOT / "docs/CHANGELOG.md").read_text(encoding="utf-8"))
        current_block = re.search(r"## Current artifact(.*?)(?=\n## |\Z)", manifest, re.S)
        self.assertIsNotNone(current_block)
        self.assertIn(f"`{version}`", current_block.group(1))

    def test_required_documentation_surfaces_are_in_consistency_gate(self):
        required = [
            ROOT / "docs" / "Creation-Chronicle.html",
            ROOT / "docs" / "Glosarium.html",
            ROOT / "docs" / "CHECKPOINT.md",
            ROOT / "docs" / "STATE.md",
            ROOT / "docs" / "BACKLOG.md",
            ROOT / "docs" / "CHANGELOG.md",
            ROOT / "docs" / "SECURITY.md",
        ]
        for path in required:
            self.assertTrue(path.is_file(), str(path))
        checkpoint = (ROOT / "docs/CHECKPOINT.md").read_text(encoding="utf-8")
        self.assertIn("docs/Creation-Chronicle.html", checkpoint)
        self.assertIn("docs/Glosarium.html", checkpoint)
        self.assertIn("Artifact Compliance Gate", checkpoint)

    def test_flat_root_layout_of_project_tree(self):
        forbidden_wrapper = ROOT.name
        for path in ROOT.iterdir():
            self.assertNotEqual(path.name, forbidden_wrapper)
        self.assertTrue((ROOT / "docs").is_dir())
        self.assertTrue((ROOT / "pernah").is_dir())
        self.assertTrue((ROOT / "tests").is_dir())
        self.assertTrue((ROOT / "VERSION").is_file())

    def test_all_release_tests_use_unittest_discovery_contract(self):
        offenders = []
        tests_root = ROOT / "tests"
        for path in sorted(tests_root.glob("test_*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_"):
                    offenders.append(f"{path.name}:{node.name}")
        self.assertEqual(
            offenders,
            [],
            "top-level test functions bypass the canonical unittest discovery gate: " + ", ".join(offenders),
        )

    def test_knowledge_surface_impact_contract_exists(self):
        text = (ROOT / "docs/CHECKPOINT.md").read_text(encoding="utf-8")
        for phrase in [
            "3.34.2 KNOWLEDGE-SURFACE IMPACT CHECK",
            "BOTH",
            "GLOSSARY",
            "CHRONICLE",
            "NONE",
            "Glossary menjawab",
            "Chronicle menjawab",
        ]:
            self.assertIn(phrase, text)
        self.assertIn("Knowledge-Surface Impact Check", (ROOT / "docs/Creation-Chronicle.html").read_text(encoding="utf-8"))
        self.assertIn("Human Touch", (ROOT / "docs/Glosarium.html").read_text(encoding="utf-8"))

    def test_prompt_translation_contract_exists(self):
        text = (ROOT / "docs/CHECKPOINT.md").read_text(encoding="utf-8")
        for phrase in [
            "RAW IDEA / INTENT", "REQUIREMENTS", "CONSTRAINTS", "OPEN QUESTIONS",
            "ACCEPTANCE CRITERIA", "EXECUTION PROMPT / PLAN", "AI TIDAK BOLEH mengarang intent"
        ]:
            self.assertIn(phrase, text)

    def test_exact_zip_is_flat_root_when_requested(self):
        import os
        artifact = os.environ.get("PERNAH_ARTIFACT")
        if not artifact:
            self.skipTest("PERNAH_ARTIFACT not set; exact packaged artifact is checked by release preflight")
        with zipfile.ZipFile(artifact) as zf:
            names = [n for n in zf.namelist() if n and not n.endswith("/")]
            self.assertTrue(names)
            top = {n.split("/", 1)[0] for n in names}
            self.assertIn("docs", top)
            self.assertIn("pernah", top)
            self.assertIn("tests", top)
            self.assertNotIn(Path(artifact).stem, top)
            self.assertFalse(any(
                "__pycache__/" in n
                or n.endswith(".pyc")
                or n.endswith(".pyo")
                or n == ".pytest_cache"
                or n.startswith(".pytest_cache/")
                for n in names
            ))
            self.assertIn("VERSION", names)
            version = zf.read("VERSION").decode().strip()
            self.assertEqual(version, (ROOT / "VERSION").read_text().strip())


if __name__ == "__main__":
    unittest.main()
