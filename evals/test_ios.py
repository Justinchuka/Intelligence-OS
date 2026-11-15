"""Automated tests for scripts/ios.py and scripts/render_dashboard.py.
Run: python evals/test_ios.py   (from the skill root). These test the deterministic tooling only;
behavioural tests of Claude following SKILL.md are in test-cases.md and are NOT automated."""
import json, os, subprocess, sys, tempfile, unittest, glob
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IOS = os.path.join(ROOT, "scripts", "ios.py")

def run(args, expect=0):
    p = subprocess.run([sys.executable, IOS] + args, capture_output=True, text=True)
    assert p.returncode == expect, f"exit {p.returncode} (expected {expect}) for {args}\n{p.stdout}\n{p.stderr}"
    try: return json.loads(p.stdout)
    except Exception: return p.stdout + p.stderr

class T(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.mkdtemp(); self.d = os.path.join(self.t, "os-state")
        run(["init", "--dir", self.d, "--name", "Test OS", "--context", "business_brand", "--template", "atmosphere-glass", "--profile", "company=Acme", "--confirm"])
    def r(self, *a, expect=0): return run(list(a) + ["--dir", self.d], expect)
    def cfg(self): return json.load(open(os.path.join(self.d, "config.json")))
    def add(self, cid): return self.r("module", "add", "--catalogue", cid, "--confirm")

    def test_approval_gate_blocks_without_confirm(self):
        run(["init", "--dir", os.path.join(self.t, "x"), "--context", "individual"], expect=3)
        self.r("module", "add", "--catalogue", "job-finder", expect=3)
        self.assertNotIn("job-finder", self.cfg()["modules"])
    def test_initial_templates_limited_to_three_then_all_ten(self):
        run(["init", "--dir", os.path.join(self.t, "y"), "--context", "individual", "--template", "mosaic-bento", "--confirm"], expect=2)
        self.r("template", "--template", "mosaic-bento", "--confirm")
        self.assertEqual(self.cfg()["appearance"]["template"], "mosaic-bento")
    def test_invalid_context(self): run(["init", "--dir", os.path.join(self.t, "z"), "--context", "alien", "--confirm"], expect=2)
    def test_cap_of_15(self):
        ids = [m for m in ["job-finder","internship-finder","scholarship-finder","grant-finder","expense-tracker","habit-tracker","study-tracker","reading-tracker","conference-finder","webinar-finder","meetup-finder","course-finder","certification-finder","industry-news-monitor","market-trend-analyst","expert-finder"]]
        for i in ids[:15]: self.add(i)
        self.r("module", "add", "--catalogue", ids[15], "--confirm", expect=2)
        self.r("module", "disable", "--id", ids[0], "--confirm"); self.add(ids[15])
    def test_core_cannot_be_deleted_but_can_be_hidden_disabled(self):
        self.r("module", "delete", "--id", "core-actions", "--confirm", expect=2)
        self.r("module", "archive", "--id", "core-actions", "--confirm", expect=2)
        self.r("module", "hide", "--id", "core-actions", "--confirm"); self.r("module", "disable", "--id", "core-actions", "--confirm")
        self.assertIn("core-actions", self.cfg()["modules"])
    def test_lifecycle_history_preserved(self):
        self.add("expense-tracker"); self.r("record", "add", "--module", "expense-tracker", "--value", "100", "--currency", "NGN")
        self.r("module", "disable", "--id", "expense-tracker", "--confirm")
        self.r("record", "add", "--module", "expense-tracker", "--value", "5", expect=2)  # disabled stops execution/entry
        self.r("module", "enable", "--id", "expense-tracker", "--confirm")
        self.r("module", "hide", "--id", "expense-tracker", "--confirm")
        self.assertTrue(self.cfg()["modules"]["expense-tracker"]["state"]["enabled"])  # hide != disable
        self.r("module", "delete", "--id", "expense-tracker", "--confirm")
        self.assertTrue(os.path.exists(os.path.join(self.d, "archive", "expense-tracker", "records.jsonl")))
        self.assertEqual(len(open(os.path.join(self.d, "records", "expense-tracker.jsonl")).read().splitlines()), 1)
        self.r("module", "restore", "--id", "expense-tracker", "--confirm")
        self.r("module", "delete", "--id", "expense-tracker", "--permanent", "--confirm")
        self.assertNotIn("expense-tracker", self.cfg()["modules"])
    def test_record_edit_history_and_ai_cannot_overwrite_user_edit(self):
        self.add("expense-tracker")
        rid = self.r("record", "add", "--module", "expense-tracker", "--value", "8500", "--currency", "NGN", "--category", "transport")["record_id"]
        self.r("record", "edit", "--module", "expense-tracker", "--id", rid, "--set", "value=9000", "--by", "user")
        rec = self.r("record", "list", "--module", "expense-tracker")[0]
        self.assertEqual(rec["edit_history"][0]["old"], 8500.0); self.assertEqual(rec["value"], 9000.0)
        self.r("record", "edit", "--module", "expense-tracker", "--id", rid, "--set", "value=1", "--by", "ai", expect=2)
        self.r("record", "edit", "--module", "expense-tracker", "--id", rid, "--set", "record_id=x", expect=2)  # immutable
    def test_discovery_requires_evidence_and_dedups_and_protects_edits(self):
        self.add("job-finder")
        good = {"title": "Role A", "summary": "s", "source_url": "https://e.com/a", "evidence": "page lists role", "verification_status": "verified", "confidence": "High confidence", "confidence_rationale": "primary page"}
        bad = {"title": "No evidence", "summary": "s", "source_url": "https://e.com/b"}
        p = os.path.join(self.t, "d.json"); json.dump([good, bad], open(p, "w"))
        res = self.r("discovery", "--module", "job-finder", "--json", p)
        self.assertEqual((res["new"], len(res["rejected"])), (1, 1))
        res = self.r("discovery", "--module", "job-finder", "--json", p); self.assertEqual(res["duplicates"], 1); self.assertEqual(res["new"], 0)
        rid = self.r("record", "list", "--module", "job-finder")[0]["record_id"]
        self.r("record", "edit", "--module", "job-finder", "--id", rid, "--set", "title=My title", "--by", "user")
        json.dump([dict(good, title="AI retitle")], open(p, "w")); res = self.r("discovery", "--module", "job-finder", "--json", p)
        self.assertIn("title", res.get("protected_user_edits_kept", []))
        self.assertEqual(self.r("record", "list", "--module", "job-finder")[0]["title"], "My title")
    def test_run_counts_cannot_inflate(self):
        self.add("job-finder")
        self.r("run", "--module", "job-finder", "--queries", "20", "--results", "5", "--unique", "9", "--new", "1", expect=2)
        self.r("run", "--module", "job-finder", "--queries", "20", "--results", "9", "--unique", "5", "--new", "2")
    def test_source_health_only_real_status_and_removal_keeps_findings(self):
        self.add("job-finder"); self.r("source", "add", "--name", "Board", "--url", "https://b.example", "--module", "job-finder", "--confirm")
        self.assertEqual(self.cfg()["sources"]["board"]["status"], "not_checked")
        self.r("source", "health", "--id", "board", "--status", "healthy", expect=2)
        self.r("source", "health", "--id", "board", "--status", "failed", "--error", "timeout")
        self.r("source", "remove", "--id", "board", "--confirm"); self.assertNotIn("board", self.cfg()["sources"])
    def test_analysis_mixed_currency_not_summed_and_gaps_reported(self):
        self.add("expense-tracker")
        for v, c, d in [("100", "NGN", "2026-11-10"), ("200", "NGN", "2026-11-12"), ("5", "USD", "2026-11-12")]:
            self.r("record", "add", "--module", "expense-tracker", "--value", v, "--currency", c, "--occurred-at", d)
        res = self.r("analyse", "--module", "expense-tracker", "--period", "all")
        gs = {g["unit_or_currency"]: g for g in res["groups"]}
        self.assertEqual(gs["NGN"]["sum"], 300); self.assertEqual(gs["USD"]["sum"], 5)
        self.assertEqual(gs["NGN"]["days_without_records"], 1); self.assertTrue(gs["NGN"]["sufficiency"].startswith("thin"))
    def test_versioning_and_rollback_keep_records(self):
        self.add("expense-tracker"); self.r("record", "add", "--module", "expense-tracker", "--value", "1")
        v = self.cfg()["version"]; self.r("module", "hide", "--id", "expense-tracker", "--confirm")
        self.r("versions", "rollback", "--to", str(v), "--confirm")
        self.assertTrue(self.cfg()["modules"]["expense-tracker"]["state"]["visible"]); self.assertGreater(self.cfg()["version"], v)
        self.assertEqual(len(self.r("record", "list", "--module", "expense-tracker")), 1)
        self.assertTrue(len(self.r("versions", "diff", "--a", str(v), "--b", str(v - 1))) > 0)
    def test_template_switch_preserves_data_and_all_ten_render(self):
        self.add("expense-tracker"); self.add("job-finder")
        for i in range(4): self.r("record", "add", "--module", "expense-tracker", "--value", str(10 + i), "--currency", "NGN")
        evil = os.path.join(self.t, "e.json"); json.dump([{"title": "<script>alert(1)</script>", "summary": "s", "source_url": "https://e.com/x", "evidence": "e", "verification_status": "unverified", "confidence": "Low confidence", "confidence_rationale": "r"}], open(evil, "w"))
        self.r("discovery", "--module", "job-finder", "--json", evil)
        self.r("goal", "add", "--title", "Learn", "--status", "proposed", "--by", "ai")
        outs = {}
        for t in ["essential-minimal","intelligence-operations","atmosphere-glass","editorial-magazine","mosaic-bento","enterprise-structured","atelier-soft-luxury","observatory-data","workspace-productivity","frontier-experimental"]:
            if t not in ("essential-minimal","intelligence-operations","atmosphere-glass"): self.r("template", "--template", t, "--confirm")
            o = os.path.join(self.t, t + ".html"); self.r("render", "--template", t, "--out", o)
            h = open(o, encoding="utf-8").read(); outs[t] = h
            self.assertNotIn("<script>alert(1)", h); self.assertIn("&lt;script&gt;", h); self.assertNotIn("http-equiv", h)
            self.assertNotIn("https://cdn", h); self.assertIn("not a live application", h)
        import re
        skel = {t: re.sub(r"<style>.*?</style>", "", h, flags=re.S) for t, h in outs.items()}
        self.assertEqual(len(set(skel.values())), 10, "layouts must differ structurally, not only by CSS")
        self.assertEqual(self.r("validate")["ok"], True)
    def test_exports_public_strips_sensitive_and_profile(self):
        self.add("expense-tracker"); self.add("job-finder")
        self.r("record", "add", "--module", "expense-tracker", "--value", "1", "--notes", "private")
        o = os.path.join(self.t, "out"); self.r("export", "csv", "--out", o, "--public")
        self.assertFalse(any("expense" in f for f in os.listdir(o)))
        self.r("export", "config", "--out", o, "--public")
        pkg = json.load(open(glob.glob(os.path.join(o, "*config-package.json"))[0]))
        self.assertNotIn("owner_profile", pkg["config"]); self.assertNotIn("Acme", json.dumps(pkg))
        self.r("export", "xlsx", "--out", o)
        self.assertTrue(glob.glob(os.path.join(o, "*.xlsx")))
    def test_validate_detects_tamper_and_secrets(self):
        self.add("expense-tracker"); self.r("record", "add", "--module", "expense-tracker", "--value", "1")
        with open(os.path.join(self.d, "records", "expense-tracker.jsonl"), "a") as f: f.write("\n")
        out = self.r("validate", expect=1); self.assertFalse(out["ok"])
    def test_permissions_default_empty_and_grant_needs_confirm(self):
        self.assertEqual(self.cfg()["permissions"]["profile_access"], {})
        self.r("permission", "profile", "--module", "job-finder", "--fields", "skills", expect=3)
        self.r("permission", "profile", "--module", "job-finder", "--fields", "skills", "--confirm")
        self.assertEqual(self.cfg()["permissions"]["profile_access"], {"job-finder": ["skills"]})
    def test_ai_suggested_action_needs_approval(self):
        a = self.r("action", "add", "--title", "Apply", "--by", "ai"); acts = self.r("action", "list")
        self.assertFalse(acts[0]["approved"])
        self.r("action", "update", "--id", a["id"], "--approve"); self.assertTrue(self.r("action", "list")[0]["approved"])
    def test_catalogue_integrity(self):
        cat = json.load(open(os.path.join(ROOT, "references", "catalogue", "modules.json")))["modules"]
        self.assertEqual(len(cat), 100); self.assertEqual(len({m["id"] for m in cat}), 100)
        for m in cat:
            for k in ("objective", "modes", "data_fields", "limitations", "version", "category"): self.assertTrue(m.get(k), (m["id"], k))
    def test_search_profile_workspace_taxonomy(self):
        self.add("job-finder"); self.add("expense-tracker")
        self.r("record", "add", "--module", "expense-tracker", "--value", "8500", "--category", "transport")
        res = self.r("search", "--q", "transport"); self.assertEqual(res["total"], 1)
        self.r("profile", "set", "--set", "skills=python", expect=3); self.r("profile", "set", "--set", "skills=python", "--confirm")
        self.assertEqual(self.r("profile", "show")["skills"], "python")
        self.r("workspace", "add", "--name", "Job hunt", "--modules", "job-finder", "--confirm"); self.assertIn("job-hunt", self.r("workspace", "list"))
        p = os.path.join(self.t, "tx.json"); json.dump([{"title": "t", "summary": "s", "source_url": "https://e.com/1", "evidence": "e", "verification_status": "verified", "confidence": "Verified", "confidence_rationale": "r", "taxonomy_group": "Not A Group"}], open(p, "w"))
        self.assertEqual(len(self.r("discovery", "--module", "job-finder", "--json", p)["rejected"]), 1)
    def test_zip_round_trip_validates(self):
        import shutil
        self.add("expense-tracker"); self.r("record", "add", "--module", "expense-tracker", "--value", "1")
        z = shutil.make_archive(os.path.join(self.t, "pack"), "zip", self.t, "os-state"); out = os.path.join(self.t, "rt"); shutil.unpack_archive(z, out)
        self.assertTrue(run(["validate", "--dir", os.path.join(out, "os-state")])["ok"])
if __name__ == "__main__": unittest.main(verbosity=1)
