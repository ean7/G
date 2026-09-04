import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validator", ROOT / "scripts/validate_close.py")
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class ClosePackageTests(unittest.TestCase):
    def test_validator(self):
        self.assertEqual([], validator.validate())

    def test_snapshot_has_both_reporting_blocks(self):
        data = json.loads((ROOT / "data/live_snapshot.json").read_text())
        projects = {task["project"] for task in data["tasks"]}
        self.assertTrue(any("MetaTeam" in project for project in projects))
        self.assertTrue(any("Борд" in project or "Board" in project for project in projects))

    def test_unavailable_gates_fail_closed(self):
        manifest = json.loads((ROOT / "manifest.json").read_text())
        for key in ("workbook_available", "validator_86_of_86", "drive_raw_readback", "operating_acceptance"):
            self.assertFalse(manifest[key])


if __name__ == "__main__":
    unittest.main()
