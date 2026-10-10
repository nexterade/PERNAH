import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class HumanTouchPolicyTests(unittest.TestCase):
    def test_checkpoint_defines_human_touch_behavior_not_just_permission(self):
        checkpoint = (ROOT / "docs" / "CHECKPOINT.md").read_text()
        self.assertIn("FUN-FACT / HUMAN TOUCH", checkpoint)
        self.assertIn("sesekali gunakan humor ringan, analogi, fun-fact", checkpoint)
        self.assertIn("HUMAN-TOUCH PROPAGATION / ENFORCEMENT", checkpoint)
        self.assertIn("test tidak boleh memaksa setiap respons memiliki fun-fact", checkpoint)

    def test_boot_and_continuation_propagate_human_touch_policy(self):
        boot = (ROOT / "PERNAH_BOOT.md").read_text()
        continuation = (ROOT / "PERNAH_CONTINUATION.md").read_text()
        expected = "Human touch is part of normal collaboration"
        self.assertIn(expected, boot)
        self.assertIn(expected, continuation)
        self.assertIn("never force it", boot)
        self.assertIn("never force it", continuation)

if __name__ == "__main__":
    unittest.main()
