#!/usr/bin/env python3
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$")
DEV = re.compile(r"^0\.2\.0-dev\.(\d+)$")

REQUIRED = {
    "VERSION", "README.md", "PERNAH_BOOT.md", "PERNAH_CONTINUATION.md",
    "PERNAH_PROJECT_STATE.json", "docs/CHECKPOINT.md", "docs/STATE.md",
    "docs/BACKLOG.md", "docs/CHANGELOG.md", "docs/RELEASE-MANIFEST.md",
    "docs/SECURITY.md", "docs/Creation-Chronicle.html", "docs/Glosarium.html", "docs/AI-LAYER-PLAN.md",
    "tests", "pernah",
}


def fail(msg):
    print(f"FAIL: {msg}")
    raise SystemExit(1)


def main():
    if len(sys.argv) != 2:
        fail("usage: python3 tests/release_preflight.py PATH_TO_ZIP")
    artifact = Path(sys.argv[1]).resolve()
    if not artifact.is_file():
        fail(f"artifact not found: {artifact}")

    expected_version = artifact.stem.removeprefix("PERNAH-v")
    if not SEMVER.fullmatch(expected_version):
        fail(f"artifact filename does not contain valid SemVer: {expected_version}")
    dev_match = DEV.fullmatch(expected_version)
    if not dev_match:
        fail("release preflight currently expects the PERNAH 0.2.0-dev.N line")

    with zipfile.ZipFile(artifact) as zf:
        names = [n for n in zf.namelist() if n]
        files = {n.rstrip("/") for n in names}
        if "VERSION" not in files:
            fail("VERSION missing from archive")
        version = zf.read("VERSION").decode().strip()
        if version != expected_version:
            fail(f"VERSION={version} does not match artifact filename={expected_version}")

        top = {n.split("/", 1)[0] for n in files}
        if any(n.startswith(expected_version + "/") for n in files):
            fail("archive has a version wrapper directory; flat-root contract violated")
        if "docs" not in top or "pernah" not in top or "tests" not in top:
            fail(f"required root directories missing: {sorted(top)}")
        if any(n.startswith("PERNAH-v") and "/" in n for n in files):
            fail("archive contains an enclosing PERNAH wrapper directory")
        if any(
            "__pycache__/" in n
            or n.endswith(".pyc")
            or n.endswith(".pyo")
            or n == ".pytest_cache"
            or n.startswith(".pytest_cache/")
            for n in files
        ):
            fail("generated test/runtime cache artifact found in ZIP")
        missing = sorted(x for x in REQUIRED if x not in files and not x.endswith(("tests", "pernah")))
        if missing:
            fail("required files missing: " + ", ".join(missing))

        checkpoint = zf.read("docs/CHECKPOINT.md").decode()
        for phrase in [
            "Artifact Compliance Gate",
            "docs/Creation-Chronicle.html",
            "docs/Glosarium.html",
            "RAW IDEA → REQUIREMENT → PROMPT TRANSLATION",
            "HUMAN-TOUCH PROPAGATION / ENFORCEMENT",
            "WEB BACKUP & RECOVERY CONTRACT",
        ]:
            if phrase not in checkpoint:
                fail(f"CHECKPOINT missing required contract: {phrase}")

        manifest = zf.read("docs/RELEASE-MANIFEST.md").decode()
        parent_match = re.search(
            rf"## {re.escape(version)}.*?\*\*Parent artifact:\*\* `PERNAH-v0\.2\.0-dev\.(\d+)(?:-[0-9A-Za-z.-]+)?\.zip`",
            manifest, re.S,
        )
        if not parent_match:
            fail("current release manifest has no valid parent artifact")
        parent_n = int(parent_match.group(1))
        current_n = int(dev_match.group(1))
        if parent_n >= current_n:
            fail(f"non-monotonic development lineage: parent={parent_n}, current={current_n}")

    print(f"PASS: archive structure / flat-root / hygiene / lineage / documentation contract ({version})")

    with tempfile.TemporaryDirectory(prefix="pernah-release-preflight-") as td:
        extract = Path(td) / "artifact"
        extract.mkdir()
        with zipfile.ZipFile(artifact) as zf:
            zf.extractall(extract)
        env = os.environ.copy()
        env["PERNAH_ARTIFACT"] = str(artifact)
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
            cwd=extract, env=env, text=True,
        )
        if result.returncode:
            fail("full test suite failed against exact extracted artifact")

    print("PASS: exact packaged artifact extracted and full suite passed")
    print("PASS: RELEASE PREFLIGHT — DELIVERY ALLOWED")


if __name__ == "__main__":
    main()
