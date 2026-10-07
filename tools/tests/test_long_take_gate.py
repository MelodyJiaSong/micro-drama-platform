import hashlib
import json
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace
from pathlib import Path

from tools.long_take_gate import check_inputs, check_endpoints, freeze_inputs, scan


class LongTakeGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "planning").mkdir()
        self.shot = self.root / "shot01.md"
        self.asset = self.root / "reference.png"
        self.asset.write_bytes(b"approved reference")
        self.evidence = self.root / "review.md"
        self.evidence.write_text("independent input review", encoding="utf-8")
        self.route = self.root / "route.json"
        self.route.write_text(json.dumps({"fixed_lens": True, "no_camera_cuts": True, "min_clearance_m": 1.8}), encoding="utf-8")
        self.prompt = "连续一镜到底，禁止叠化、溶解"
        self.contract = {"prompt_sha256": hashlib.sha256(self.prompt.encode()).hexdigest(),
                         "references": [{"path": str(self.asset), "sha256": hashlib.sha256(self.asset.read_bytes()).hexdigest()}],
                         "input_review": {"status": "passed"},
                         "evidence": [{"path": str(self.evidence), "sha256": hashlib.sha256(self.evidence.read_bytes()).hexdigest()}, {"path": str(self.route), "sha256": hashlib.sha256(self.route.read_bytes()).hexdigest()}],
                         "item_owners": {"hammer": "hero"}, "route_readback": str(self.route)}
        self.save()

    def save(self):
        (self.root / "planning/continuous_take.json").write_text(json.dumps(self.contract), encoding="utf-8")

    def check(self):
        return check_inputs(self.shot, self.prompt, [self.asset])

    def test_current_approved_inputs(self):
        self.assertEqual(self.check(), [])

    def test_changed_prompt_requires_recheck(self):
        self.prompt += "changed"
        self.assertTrue(any("prompt" in x for x in self.check()))

    def test_changed_reference_invalidates_review(self):
        self.asset.write_bytes(b"other session changed image")
        self.assertTrue(any("参考" in x for x in self.check()))

    def test_changed_evidence_is_rejected(self):
        self.evidence.write_text("changed verdict", encoding="utf-8")
        self.assertTrue(any("证据" in x for x in self.check()))

    def test_unreviewed_input_is_blocked(self):
        self.contract["input_review"]["status"] = "pending"
        self.save()
        self.assertTrue(any("未解决" in x for x in self.check()))

    def test_roof_collision_is_blocked(self):
        self.route.write_text(json.dumps({"fixed_lens": True, "no_camera_cuts": True, "min_clearance_m": 0.2}), encoding="utf-8")
        self.assertTrue(any("净空" in x for x in self.check()))

    def test_missing_final_full_body_evidence_is_blocked(self):
        self.contract["final_framing_constraints"] = {"actors": ["hero"], "max_fraction": .4, "min_foot_margin": .15, "min_hold_s": 1.5}
        self.save()
        self.assertTrue(any("全身" in x for x in self.check()))
        self.assertTrue(any("停稳" in x for x in self.check()))

    def test_second_endpoint_drift_requires_approved_uploaded_anchor(self):
        self.contract["endpoint_drift_count"] = 2
        self.save()
        self.assertTrue(any("重复漂移" in x for x in self.check()))
        self.contract["terminal_framing"] = {"status":"passed","path":str(self.asset),
                                           "sha256":hashlib.sha256(self.asset.read_bytes()).hexdigest(),
                                           "actors":{"hero":{"all_in_frame":True,"fraction":.22,"foot_margin":.38}}}
        self.save()
        self.assertEqual(self.check(), [])

    def test_terminal_anchor_cannot_omit_a_required_actor(self):
        self.contract["endpoint_drift_count"] = 2
        self.contract["final_framing_constraints"] = {"actors":["hero", "officer"], "max_fraction":.4, "min_foot_margin":.15, "min_hold_s":1.5}
        self.contract["terminal_framing"] = {"status":"passed", "path":str(self.asset),
                                           "sha256":hashlib.sha256(self.asset.read_bytes()).hexdigest(),
                                           "actors":{"hero":{"all_in_frame":True,"fraction":.22,"foot_margin":.38}}}
        self.save()
        self.assertTrue(any("终点构图帧的人物框" in x for x in self.check()))

    def test_third_drift_rejects_ordinary_reference_mode(self):
        self.contract["endpoint_drift_count"] = 3
        self.save()
        self.assertTrue(any("必须切换明确首尾帧模式" in x for x in self.check()))

    def test_endpoint_mode_checks_actual_roles_and_identity_sources(self):
        first = self.root / "first.png"
        first.write_bytes(b"approved aerial start")
        row = lambda p: {"path":str(p), "sha256":hashlib.sha256(p.read_bytes()).hexdigest(), "status":"passed"}
        identity = self.root / "characters/hero/views.png"
        identity.parent.mkdir(parents=True)
        identity.write_bytes(b"approved hero")
        self.contract["terminal_framing"] = row(self.asset)
        self.contract["endpoint_control"] = {"first":row(first),"last":row(self.asset),"characters":["hero"],"identity_sources":[{**row(identity),"character":"hero"}]}
        self.assertEqual(check_endpoints(self.contract, [first, self.asset]), [])
        self.contract["endpoint_control"]["last"]["sha256"] = "other frame"
        self.assertTrue(any("last" in x for x in check_endpoints(self.contract, [first, self.asset])))
        self.contract["endpoint_control"]["last"] = row(self.asset)
        identity.write_bytes(b"different person")
        self.assertTrue(any("身份来源已变" in x for x in check_endpoints(self.contract, [first, self.asset])))

    def test_frozen_evidence_preserves_bytes_when_live_review_changes(self):
        self.shot.write_text(f"## Seedance prompt\n\n```text\n{self.prompt}\n```\n",encoding="utf-8")
        output = self.root / "immutable_inputs"
        index = freeze_inputs(self.shot, output)
        evidence = next(row for row in index["files"] if row["original"]==str(self.evidence.resolve()))
        self.evidence.write_text("later review revision",encoding="utf-8")
        self.assertEqual(Path(evidence["snapshot"]).read_text(encoding="utf-8"), "independent input review")
        self.assertEqual(hashlib.sha256(Path(evidence["snapshot"]).read_bytes()).hexdigest(),evidence["sha256"])

    def test_stale_evidence_cannot_be_frozen_as_approved_input(self):
        self.shot.write_text(f"## Seedance prompt\n\n```text\n{self.prompt}\n```\n",encoding="utf-8")
        self.evidence.write_text("changed before submission",encoding="utf-8")
        with self.assertRaisesRegex(ValueError,"未通过输入"):
            freeze_inputs(self.shot, self.root/"stale_snapshot")

    def test_scan_uses_actual_pts_without_duplicating_frames(self):
        video = self.root / "take.mp4"
        video.write_bytes(b"variable fps fixture")
        pts = [0.0, 0.04, 0.1]
        probe = {"streams": [{"avg_frame_rate": "30/1"}], "format": {"duration": "0.14"},
                 "frames": [{"best_effort_timestamp_time": str(t)} for t in pts]}
        commands = []
        def run(argv, **kwargs):
            commands.append(argv)
            if argv[0] == "ffprobe":
                return SimpleNamespace(stdout=json.dumps(probe))
            if "scale=192:108" in argv:
                return SimpleNamespace(stdout=b"\x00" * (192*108) + b"\x01" * (192*108) + b"\xff" * (192*108))
            return SimpleNamespace(stdout=b"\x00" * (480*270*3))
        with patch("tools.long_take_gate.subprocess.run", side_effect=run):
            scan(video, self.root / "scan")
        report = json.loads((self.root / "scan/continuity_scan.json").read_text(encoding="utf-8"))
        self.assertEqual(report["decoded_frames"], 3)
        self.assertEqual(report["candidates"][0]["t"], 0.1)
        self.assertIn("passthrough", next(c for c in commands if "scale=192:108" in c))

    def test_scan_rejects_pts_frame_count_mismatch(self):
        video = self.root / "bad.mp4"
        video.write_bytes(b"bad fixture")
        probe = {"streams": [{"avg_frame_rate": "24/1"}], "format": {"duration": "1"},
                 "frames": [{"best_effort_timestamp_time": "0"}]}
        results = [SimpleNamespace(stdout=json.dumps(probe)), SimpleNamespace(stdout=b"\x00"*(192*108*2))]
        with patch("tools.long_take_gate.subprocess.run", side_effect=results):
            with self.assertRaisesRegex(ValueError, "PTS"):
                scan(video, self.root / "bad_scan")


if __name__ == "__main__":
    unittest.main()
