"""Tests for scripts/sfx_place.py pure plan logic (no Resolve needed)."""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sfx_place


class TestResolvePath(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.raw = os.path.join(self.tmp, "raw")
        self.proc = os.path.join(self.tmp, "proc")
        os.makedirs(self.raw)
        os.makedirs(self.proc)
        open(os.path.join(self.proc, "pop-14.wav"), "w").close()
        open(os.path.join(self.raw, "gong-10.wav"), "w").close()

    def test_prefers_processed_dir(self):
        self.assertEqual(
            sfx_place.resolve_path("pop-14.wav", self.raw, self.proc),
            os.path.join(self.proc, "pop-14.wav"),
        )

    def test_falls_back_to_raw_dir(self):
        self.assertEqual(
            sfx_place.resolve_path("gong-10.wav", self.raw, self.proc),
            os.path.join(self.raw, "gong-10.wav"),
        )

    def test_missing_returns_none(self):
        self.assertIsNone(sfx_place.resolve_path("nope.wav", self.raw, self.proc))


class TestLoadPlan(unittest.TestCase):
    def test_loads_json_with_sfx_key(self):
        tmp = tempfile.mkdtemp()
        path = os.path.join(tmp, "plan.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"sfx": [{"sfx_file": "pop-14.wav",
                                "timestamp_seconds": 5.0,
                                "duration": 0.5,
                                "reason": "punchline"}]}, f)
        plan = sfx_place.load_plan(path)
        self.assertEqual(plan["sfx"][0]["sfx_file"], "pop-14.wav")

    def test_missing_sfx_key_raises(self):
        tmp = tempfile.mkdtemp()
        path = os.path.join(tmp, "plan.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"foo": 1}, f)
        with self.assertRaises(ValueError):
            sfx_place.load_plan(path)


class TestValidatePlan(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.raw = os.path.join(self.tmp, "raw")
        self.proc = os.path.join(self.tmp, "proc")
        os.makedirs(self.raw)
        os.makedirs(self.proc)
        open(os.path.join(self.proc, "pop-14.wav"), "w").close()

    def _plan(self, **overrides):
        entry = {"sfx_file": "pop-14.wav", "timestamp_seconds": 5.0,
                 "duration": 0.5, "reason": "punchline"}
        entry.update(overrides)
        return {"sfx": [entry]}

    def test_valid_plan_no_errors(self):
        errors, warnings = sfx_place.validate_plan(
            self._plan(), self.raw, self.proc, timeline_duration=60.0)
        self.assertEqual(errors, [])

    def test_missing_file_is_error(self):
        errors, _ = sfx_place.validate_plan(
            self._plan(sfx_file="nope.wav"), self.raw, self.proc, timeline_duration=60.0)
        self.assertTrue(any("not found" in e for e in errors))

    def test_negative_timestamp_is_error(self):
        errors, _ = sfx_place.validate_plan(
            self._plan(timestamp_seconds=-1.0), self.raw, self.proc, timeline_duration=60.0)
        self.assertTrue(any("timestamp" in e for e in errors))

    def test_past_timeline_end_is_error(self):
        errors, _ = sfx_place.validate_plan(
            self._plan(timestamp_seconds=70.0), self.raw, self.proc, timeline_duration=60.0)
        self.assertTrue(any("timeline" in e.lower() or "duration" in e.lower() for e in errors))

    def test_missing_reason_is_warning(self):
        errors, warnings = sfx_place.validate_plan(
            self._plan(reason=""), self.raw, self.proc, timeline_duration=60.0)
        self.assertEqual(errors, [])
        self.assertTrue(any("reason" in w for w in warnings))

    def test_too_close_pair_is_warning(self):
        plan = {"sfx": [
            {"sfx_file": "pop-14.wav", "timestamp_seconds": 5.0, "duration": 0.5, "reason": "a"},
            {"sfx_file": "pop-14.wav", "timestamp_seconds": 5.4, "duration": 0.5, "reason": "b"},
        ]}
        errors, warnings = sfx_place.validate_plan(plan, self.raw, self.proc, timeline_duration=60.0)
        self.assertEqual(errors, [])
        self.assertTrue(any("1s" in w or "spacing" in w.lower() for w in warnings))

    def test_empty_plan_is_error(self):
        errors, _ = sfx_place.validate_plan({"sfx": []}, self.raw, self.proc, timeline_duration=60.0)
        self.assertTrue(errors)


class TestBuildPlacements(unittest.TestCase):
    def test_returns_full_paths(self):
        tmp = tempfile.mkdtemp()
        raw = os.path.join(tmp, "raw")
        proc = os.path.join(tmp, "proc")
        os.makedirs(raw)
        os.makedirs(proc)
        open(os.path.join(proc, "pop-14.wav"), "w").close()
        plan = {"sfx": [{"sfx_file": "pop-14.wav", "timestamp_seconds": 5.0,
                         "duration": 0.5, "reason": "punchline"}]}
        placements = sfx_place.build_placements(plan, raw, proc)
        self.assertEqual(len(placements), 1)
        self.assertEqual(placements[0]["sfx_path"], os.path.join(proc, "pop-14.wav"))
        self.assertEqual(placements[0]["timestamp_seconds"], 5.0)
        self.assertEqual(placements[0]["duration_seconds"], 0.5)
        self.assertEqual(placements[0]["reason"], "punchline")


class TestDryRunOutput(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.raw = os.path.join(self.tmp, "raw")
        self.proc = os.path.join(self.tmp, "proc")
        os.makedirs(self.raw)
        os.makedirs(self.proc)
        open(os.path.join(self.proc, "pop-14.wav"), "w").close()

    def test_dry_run_exits_zero_and_prints(self):
        plan_path = os.path.join(self.tmp, "plan.json")
        with open(plan_path, "w", encoding="utf-8") as f:
            json.dump({"sfx": [
                {"sfx_file": "pop-14.wav", "timestamp_seconds": 5.0,
                 "duration": 0.5, "reason": "punchline"}
            ]}, f)
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = sfx_place.main([
                "--plan", plan_path, "--dry-run",
                "--raw-dir", self.raw, "--processed-dir", self.proc,
            ])
        self.assertEqual(code, 0)
        self.assertIn("pop-14.wav", buf.getvalue())

    def test_invalid_plan_exits_two(self):
        plan_path = os.path.join(self.tmp, "plan.json")
        with open(plan_path, "w", encoding="utf-8") as f:
            json.dump({"sfx": [
                {"sfx_file": "missing.wav", "timestamp_seconds": 5.0,
                 "duration": 0.5, "reason": "x"}
            ]}, f)
        code = sfx_place.main([
            "--plan", plan_path, "--dry-run",
            "--raw-dir", self.raw, "--processed-dir", self.proc,
        ])
        self.assertEqual(code, 2)


class TestPluginJson(unittest.TestCase):
    def test_plugin_json_is_valid(self):
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(root, ".opencode", "skills", "adding-sfx", "kimi.plugin.json")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["name"], "adding-sfx")
        self.assertEqual(data["skills"][0], "./SKILL.md")


if __name__ == "__main__":
    unittest.main()
