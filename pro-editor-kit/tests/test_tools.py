"""pro-editor-kit tool tests. Run:  python3 -m unittest discover -s pro-editor-kit/tests -v
Render tests need ffmpeg/ffprobe on PATH and are skipped otherwise."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KIT / "tools"))

import autocut  # noqa: E402
import beat_grid  # noqa: E402
import captions  # noqa: E402
import motion_lint  # noqa: E402
import sfx_map  # noqa: E402
import validate  # noqa: E402
from _common import load_words  # noqa: E402

SAMPLE = KIT / "examples" / "words.sample.json"
HAVE_FFMPEG = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))


class AutocutTest(unittest.TestCase):
    def setUp(self):
        self.words = load_words(SAMPLE)
        self.plan, self.retimed = autocut.build(self.words, fps=30, duration=14.7)

    def test_drops_filler_stutter_and_retake(self):
        d = self.plan["stats"]["dropped_words"]
        self.assertEqual(d["filler"], 1)
        self.assertEqual(d["stutter"], 2)          # first "I think"
        self.assertEqual(d["retake"], 4)           # first "most edits fail because"
        text = " ".join(w["word"] for w in self.retimed)
        self.assertIn("most edits fail because they move too much.", text)
        self.assertEqual(text.count("most edits"), 1)
        self.assertNotIn("um", text.split())

    def test_ranges_are_frame_aligned_monotonic_and_shorter(self):
        keep = self.plan["keep"]
        for k in keep:
            self.assertAlmostEqual(k["start"] * 30, round(k["start"] * 30), places=4)
            self.assertLess(k["start"], k["end"])
        for a, b in zip(keep, keep[1:]):
            self.assertLessEqual(a["end"], b["start"])
        self.assertLess(self.plan["stats"]["output_seconds"], self.plan["stats"]["source_seconds"] - 4)

    def test_retimed_words_fit_output(self):
        out = self.plan["stats"]["output_seconds"]
        for a, b in zip(self.retimed, self.retimed[1:]):
            self.assertLessEqual(a["start"], b["start"])
        self.assertLessEqual(self.retimed[-1]["end"], out + 1e-6)

    def test_alternating_punch_in(self):
        zooms = [k["zoom"] for k in self.plan["keep"]]
        for a, b in zip(zooms, zooms[1:]):
            self.assertNotEqual(a, b)

    def test_accepts_engine_shapes(self):
        with tempfile.TemporaryDirectory() as d:
            for shape in ({"segments": [{"words": [{"word": " hi", "start": 0, "end": 0.2}]}]},
                          {"word_segments": [{"word": "hi", "start": 0, "end": 0.2}, {"word": "2024"}]},
                          {"results": {"channels": [{"alternatives": [{"words": [{"word": "hi", "start": 0, "end": 0.2}]}]}]}},
                          [{"text": "hi", "startMs": 0, "endMs": 200}]):
                p = Path(d) / "w.json"
                p.write_text(json.dumps(shape))
                self.assertEqual(load_words(p)[0]["word"], "hi")


class CaptionsTest(unittest.TestCase):
    def test_reel_pages(self):
        words = autocut.build(load_words(SAMPLE), fps=30)[1]
        pages, _ = captions.build(words, 30, "reel")
        for p in pages:
            self.assertLessEqual(len(p["words"]), 5)
            self.assertLessEqual(sum(w["emphasis"] for w in p["words"]), 1)
            self.assertLess(p["start"], p["end"])
        for a, b in zip(pages, pages[1:]):
            self.assertLessEqual(a["end"], b["start"] + 1e-9)
        self.assertFalse([p for p in pages if len(p["words"]) == 1], "orphan single-word page")
        emph = [w["text"] for p in pages for w in p["words"] if w["emphasis"]]
        self.assertIn("25%", emph)

    def test_srt_format(self):
        pages, _ = captions.build(load_words(SAMPLE), 30, "youtube")
        srt = captions.to_srt(pages)
        self.assertTrue(srt.startswith("1\n00:00:00,500 --> "))

    def test_remotion_shape(self):
        caps = captions.to_remotion(load_words(SAMPLE))
        self.assertEqual(set(caps[0]), {"text", "startMs", "endMs", "timestampMs", "confidence"})
        self.assertTrue(caps[1]["text"].startswith(" "))


class LintTest(unittest.TestCase):
    BAD = """import {useCurrentFrame, interpolate, spring} from 'remotion';
export const A = () => { const frame = useCurrentFrame(); const f = frame;
  const x = interpolate(frame, [0, 30], [0, 1]);
  const ok = interpolate(spring({frame: f, fps: 30, config: {damping: 14}}), [0, 1], [0, 1], {extrapolateRight: 'clamp'});
  const s = spring({frame: f, fps: 30});
  const r = Math.random();
  return <div style={{transition: 'opacity 0.3s'}}><img src="a.png"/></div>; };
"""
    GSAP = """<script>const tl = gsap.timeline(); tl.to('.a', {x: 100, duration: 0.05, ease: 'none'});
const ok = gsap.timeline({ paused: true }); window.__timelines = {main: ok};</script>"""

    def rules(self, name, text):
        return [f["rule"] for f in motion_lint.lint_text(Path(name), text)]

    def test_remotion_rules(self):
        r = self.rules("A.tsx", self.BAD)
        for rid in ("D001", "R001", "R002", "R003", "R005"):
            self.assertIn(rid, r)
        self.assertEqual(r.count("R003"), 1)   # the clamped call must not be flagged
        self.assertEqual(r.count("R005"), 1)   # spring with config must not be flagged

    def test_gsap_rules(self):
        r = self.rules("c.html", self.GSAP)
        self.assertEqual(r.count("G001"), 1)
        self.assertIn("G002", r)
        self.assertIn("G003", r)

    def test_no_false_positives_in_comments_strings_or_bounded_progress(self):
        src = """import {interpolate, spring} from 'remotion';
// no Date.now() here
const label = "const opus = spring({ k: 170 });";
const y = interpolate(progress, [0, 1], [20, 0]);
"""
        self.assertEqual(self.rules("C.tsx", src), [])

    def test_ignore_comment(self):
        self.assertNotIn("D001", self.rules("b.ts", "const r = Math.random(); // motion-lint-ignore D001"))


class SfxAndBeatsTest(unittest.TestCase):
    def test_placement_rules(self):
        plan = json.loads((KIT / "examples" / "scene-plan.sample.json").read_text())
        lib = json.loads((KIT / "examples" / "sfx-library.sample.json").read_text())
        placed, dropped = sfx_map.place(plan["events"], lib)
        roles = [p["role"] for p in placed]
        self.assertIn("whoosh", roles)
        riser = next(p for p in placed if p["role"] == "riser")
        self.assertAlmostEqual(riser["start"], 6.4 - 2.0, places=3)     # riser ends on the reveal
        whoosh = next(p for p in placed if p["role"] == "whoosh")
        self.assertLess(whoosh["start"], 1.6)                              # whoosh peaks on the cut
        self.assertTrue(any("closer than" in d["why"] for d in dropped))   # 1.7/1.75 pops de-stacked

    def test_mix_command_shape(self):
        cmd = sfx_map.mix_command([{"start": 1.0, "file": "a.wav", "gain_db": -12}], "v.mp4", "m.mp3", "o.mp4")
        fc = cmd[cmd.index("-filter_complex") + 1]
        self.assertIn("sidechaincompress", fc)
        self.assertIn("adelay=1000|1000", fc)
        self.assertIn("amix=inputs=3", fc)

    def test_beat_snap(self):
        res = beat_grid.snap([0.98, 1.6], bpm=120, offset=0.0, tolerance=0.05)
        self.assertEqual(res[0]["snapped"], 1.0)
        self.assertEqual(res[1]["snapped"], 1.6)          # 0.1 s from 1.5 > tolerance: speech wins
        self.assertFalse(res[1]["moved"])


class ValidateTest(unittest.TestCase):
    def test_examples_valid(self):
        for ex, sc in (("brief.sample.json", "brief"), ("scene-plan.sample.json", "scene-plan"), ("sfx-library.sample.json", "sfx-library")):
            data = json.loads((KIT / "examples" / ex).read_text())
            schema = json.loads((KIT / "schemas" / f"{sc}.schema.json").read_text())
            self.assertEqual(validate.check(data, schema), [], ex)

    def test_catches_bad_brief(self):
        schema = json.loads((KIT / "schemas" / "brief.schema.json").read_text())
        errs = validate.check({"title": "x", "platform": "myspace", "fps": 29}, schema)
        self.assertTrue(any("platform" in e for e in errs))
        self.assertTrue(any("missing required 'aspect'" in e for e in errs))


@unittest.skipUnless(HAVE_FFMPEG, "ffmpeg/ffprobe not installed")
class RenderTest(unittest.TestCase):
    def ff(self, *args):
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args], check=True)

    def test_autocut_render_then_qa(self):
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / "raw.mp4"
            self.ff("-f", "lavfi", "-i", "testsrc2=size=320x568:rate=30:duration=14.7",
                    "-f", "lavfi", "-i", "sine=frequency=220:sample_rate=48000:duration=14.7",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(src))
            rc = autocut.main([str(SAMPLE), "--fps", "30", "--source", str(src), "--out", str(Path(d) / "cut"), "--render"])
            self.assertEqual(rc, 0)
            plan = json.loads((Path(d) / "cut" / "cut-plan.json").read_text())
            out = Path(d) / "cut" / "cut.mp4"
            dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)],
                                       capture_output=True, text=True).stdout)
            self.assertAlmostEqual(dur, plan["stats"]["output_seconds"], delta=0.1)

    def test_qa_detects_black_and_freeze(self):
        import render_qa
        with tempfile.TemporaryDirectory() as d:
            bad = Path(d) / "bad.mp4"
            # 1 s black, then 2 s of a frozen frame, then 2 s moving; audio far too quiet
            self.ff("-f", "lavfi", "-i", "color=black:size=320x240:rate=30:duration=1",
                    "-f", "lavfi", "-i", "color=0x336699:size=320x240:rate=30:duration=2",
                    "-f", "lavfi", "-i", "testsrc2=size=320x240:rate=30:duration=2",
                    "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000:duration=5",
                    "-filter_complex", "[0:v][1:v][2:v]concat=n=3:v=1:a=0[v];[3:a]volume=-40dB[a]",
                    "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(bad))
            rc = render_qa.main([str(bad), "--fps", "30", "--duration", "5", "--out", str(Path(d) / "qa")])
            self.assertEqual(rc, 1)
            rep = json.loads((Path(d) / "qa" / "qa-report.json").read_text())
            st = {c["check"]: c["status"] for c in rep["checks"]}
            self.assertEqual(st["black_frames"], "FAIL")
            self.assertEqual(st["frozen_frames"], "FAIL")
            self.assertEqual(st["loudness"], "FAIL")
            self.assertEqual(st["duration"], "PASS")
            self.assertTrue((Path(d) / "qa" / "contact-sheet.png").exists())
            # Declaring the intentional black + hold makes those checks pass.
            render_qa.main([str(bad), "--allow-black", "0-1", "--allow-freeze", "1-3", "--out", str(Path(d) / "qa2")])
            st2 = {c["check"]: c["status"] for c in json.loads((Path(d) / "qa2" / "qa-report.json").read_text())["checks"]}
            self.assertEqual(st2["black_frames"], "PASS")
            self.assertEqual(st2["frozen_frames"], "PASS")


if __name__ == "__main__":
    unittest.main()
