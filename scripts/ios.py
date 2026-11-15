#!/usr/bin/env python3
"""Intelligence OS state tool (deterministic, stdlib only; openpyxl optional for xlsx).

Operates on an `os-state/` folder (the portable state pack). It performs NO web access,
NO scheduling and NO AI calls. Meaningful changes require --confirm so the owner's
approval is enforced at the tool level. Run `python ios.py --help`.
"""
import argparse, csv, datetime as dt, hashlib, json, os, re, secrets, shutil, sys
from collections import defaultdict

SCHEMA = 1
HERE = os.path.dirname(os.path.abspath(__file__))
CATALOGUE = os.path.join(HERE, "..", "references", "catalogue", "modules.json")
INITIAL_TEMPLATES = ["essential-minimal", "intelligence-operations", "atmosphere-glass"]
ALL_TEMPLATES = INITIAL_TEMPLATES + ["editorial-magazine", "mosaic-bento", "enterprise-structured",
    "atelier-soft-luxury", "observatory-data", "workspace-productivity", "frontier-experimental"]
CONTEXTS = ["individual", "business_brand", "team_org", "project_research"]
VERIF = ["Verified", "High confidence", "Moderate confidence", "Low confidence", "Unverified"]
VSTATUS = ["verified", "unverified", "estimate", "reported_claim", "hypothesis"]
TAXONOMY = ["Latest Developments", "Opportunities", "Resources", "Trends & Emerging Signals", "Events & Activities", "Organisations & Ecosystem", "Research & Knowledge", "Funding & Support", "People & Networks", "Changes & Alerts"]
SENSITIVE = {"fitness-activity-tracker": "health", "habit-tracker": "personal", "personal-finance-tracker": "finance",
    "expense-tracker": "finance", "organisation-people-tracker": "personal_data",
    "community-member-directory": "personal_data", "relationship-follow-up-tracker": "personal_data"}
CORE = [("core-overview", "Overview"), ("core-quick-capture", "Quick Capture"), ("core-goals", "Goals & Objectives"),
    ("core-actions", "Action Centre"), ("core-analysis", "Analysis Centre"), ("core-library", "Intelligence Library"),
    ("core-decisions", "Decision Log"), ("core-alerts", "Alerts"), ("core-source-health", "Source Health"),
    ("core-search", "Universal Search")]

def now(): return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
def nid(p): return f"{p}_{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%d%H%M%S')}{secrets.token_hex(3)}"
def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
def die(msg, code=2): print("ERROR: " + msg, file=sys.stderr); sys.exit(code)
def out(obj): print(json.dumps(obj, indent=2, ensure_ascii=False) if not isinstance(obj, str) else obj)

class State:
    def __init__(self, root):
        self.root = root
        self.cfg_path = os.path.join(root, "config.json")
        if not os.path.exists(self.cfg_path): die(f"no state pack at {root} (config.json missing); run init")
        self.cfg = json.load(open(self.cfg_path, encoding="utf-8"))
    def p(self, *a): return os.path.join(self.root, *a)
    def save(self, why, actor="owner"):
        self.cfg["version"] += 1
        self.cfg["updated_at"] = now()
        os.makedirs(self.p("versions"), exist_ok=True)
        snap = dict(self.cfg); snap["_version_note"] = why
        json.dump(snap, open(self.p("versions", f"v{self.cfg['version']:04d}.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        json.dump(self.cfg, open(self.cfg_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        self.audit("config_change", why, actor)
        self.manifest()
    def audit(self, kind, detail, actor="owner"):
        os.makedirs(self.p("logs"), exist_ok=True)
        with open(self.p("logs", "audit.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps({"at": now(), "kind": kind, "detail": detail, "actor": actor}, ensure_ascii=False) + "\n")
    def read(self, rel):
        path = self.p(*rel.split("/"))
        if not os.path.exists(path): return []
        return [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
    def write(self, rel, rows):
        path = self.p(*rel.split("/")); os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            for r in rows: f.write(json.dumps(r, ensure_ascii=False) + "\n")
    def append(self, rel, row):
        path = self.p(*rel.split("/")); os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a", encoding="utf-8") as f: f.write(json.dumps(row, ensure_ascii=False) + "\n")
    def manifest(self):
        files = {}
        for d, _, fs in os.walk(self.root):
            for fn in fs:
                if fn == "manifest.json": continue
                full = os.path.join(d, fn); rel = os.path.relpath(full, self.root).replace(os.sep, "/")
                files[rel] = hashlib.sha256(open(full, "rb").read()).hexdigest()
        counts = {m: len(self.read(f"records/{m}.jsonl")) for m in self.cfg["modules"]}
        mf = {"schema_version": SCHEMA, "os_id": self.cfg["os"]["id"], "name": self.cfg["os"]["name"],
              "config_version": self.cfg["version"], "updated_at": self.cfg.get("updated_at"),
              "record_counts": {k: v for k, v in counts.items() if v}, "files": files,
              "note": "Portable state pack. Not a database; re-upload at the next session."}
        json.dump(mf, open(self.p("manifest.json"), "w", encoding="utf-8"), indent=1)
    def data_hash(self):
        h = hashlib.sha256()
        for d, _, fs in sorted(os.walk(self.p("records"))):
            for fn in sorted(fs): h.update(open(os.path.join(d, fn), "rb").read())
        return h.hexdigest()

def confirm(args, what):
    if not getattr(args, "confirm", False):
        print(f"PLAN (nothing changed): {what}\nRe-run with --confirm after the owner has approved.")
        sys.exit(3)

def active_custom(cfg):
    return [m for m in cfg["modules"].values() if m["origin"] in ("catalogue", "custom") and m["state"]["enabled"] and not m["state"]["archived"]]

# ---------------- commands ----------------
def cmd_init(a):
    if a.context not in CONTEXTS: die(f"context must be one of {CONTEXTS}")
    if a.template not in INITIAL_TEMPLATES: die(f"at setup only these templates are offered: {INITIAL_TEMPLATES}")
    if os.path.exists(os.path.join(a.dir, "config.json")): die("state pack already exists here")
    confirm(a, f"create state pack '{a.name}' ({a.context}, template {a.template}) in {a.dir}")
    name = a.name or "My Intelligence OS"
    cfg = {"schema_version": SCHEMA, "version": 0, "created_at": now(),
        "os": {"id": nid("os"), "name": name, "name_origin": a.name_origin, "context": a.context, "tagline": a.tagline or "", "monogram": a.monogram or name[:2].upper()},
        "owner_profile": dict(kv.split("=", 1) for kv in (a.profile or [])),
        "appearance": {"template": a.template, "preset": "expanded", "custom_template": None},
        "limits": {"max_custom_features": 15}, "modules": {}, "sources": {},
        "permissions": {"profile_access": {}, "module_access": {}, "sensitive_sharing": ["health", "finance", "personal_data"]},
        "workflows": {}, "alerts": {"mode": "in_session", "muted": []}}
    for mid, nm in CORE:
        cfg["modules"][mid] = {"id": mid, "name": nm, "origin": "core", "category": "Core", "version": "1.0.0", "modes": ["core"],
            "state": {"enabled": True, "visible": True, "archived": False}, "limitations": "Core feature."}
    os.makedirs(a.dir, exist_ok=True)
    json.dump(cfg, open(os.path.join(a.dir, "config.json"), "w", encoding="utf-8"))
    s = State(a.dir); s.save("initial configuration")
    out({"ok": True, "os_id": cfg["os"]["id"], "config_version": s.cfg["version"]})

def cmd_rename(a):
    s = State(a.dir); confirm(a, f"rename OS to '{a.name}'")
    s.cfg["os"]["name"] = a.name; s.cfg["os"]["name_origin"] = "user"; s.save(f"rename to {a.name}"); out({"ok": True, "version": s.cfg["version"]})

def cmd_template(a):
    s = State(a.dir)
    if a.template not in ALL_TEMPLATES: die(f"unknown template; choose from {ALL_TEMPLATES}")
    confirm(a, f"change appearance to {a.template} (data untouched)")
    before = s.data_hash(); s.cfg["appearance"]["template"] = a.template
    if a.preset: s.cfg["appearance"]["preset"] = a.preset
    s.save(f"appearance -> {a.template}")
    assert before == s.data_hash(), "data changed during template switch"
    out({"ok": True, "template": a.template, "data_hash_unchanged": True})

def cmd_module(a):
    s = State(a.dir); mods = s.cfg["modules"]; act = a.action
    if act == "list":
        out([{ "id": m["id"], "name": m["name"], "origin": m["origin"], **m["state"]} for m in mods.values()]); return
    if act == "add":
        if a.catalogue:
            cat = {m["id"]: m for m in json.load(open(CATALOGUE, encoding="utf-8"))["modules"]}
            if a.catalogue not in cat: die("unknown catalogue id; see references/catalogue/INDEX.md")
            m = dict(cat[a.catalogue])
            if m["id"] in SENSITIVE: m["sensitive"] = SENSITIVE[m["id"]]
        else:
            if not a.name: die("--name required for a custom module")
            m = {"id": slug(a.name), "name": a.name, "category": "Custom", "version": "1.0.0", "origin": "custom",
                 "objective": a.objective or "", "modes": (a.modes or "tracking").split(","),
                 "data_fields": [{"name": f, "type": "string"} for f in (a.fields or "value;unit;occurred_at").split(";")],
                 "limitations": a.limitations or "Custom module; behaviour defined by the owner."}
        if m["id"] in mods: die("module already exists (use enable/restore)")
        cap = s.cfg["limits"]["max_custom_features"]
        if len(active_custom(s.cfg)) + 1 > cap: die(f"would exceed the limit of {cap} active custom features; disable/archive one or change the limit explicitly")
        m.setdefault("execution", {"depth": "standard", "frequency": "manual"})
        m.setdefault("permissions", {"profile_fields": [], "reads_modules": [], "external_side_effects": "none"})
        m["state"] = {"enabled": True, "visible": True, "archived": False}
        confirm(a, f"add module '{m['name']}' ({','.join(m['modes'])}); active custom features after: {len(active_custom(s.cfg)) + 1}/{cap}")
        mods[m["id"]] = m; s.save(f"add module {m['id']}"); out({"ok": True, "id": m["id"], "version": s.cfg["version"]}); return
    if a.id not in mods: die("unknown module id")
    m = mods[a.id]
    if act in ("enable", "disable", "hide", "show"):
        confirm(a, f"{act} {a.id}")
        if act == "enable":
            if m["origin"] != "core" and len(active_custom(s.cfg)) + (0 if m["state"]["enabled"] else 1) > s.cfg["limits"]["max_custom_features"]: die("limit of active custom features reached")
            m["state"]["enabled"] = True
        elif act == "disable": m["state"]["enabled"] = False
        elif act == "hide": m["state"]["visible"] = False
        elif act == "show": m["state"]["visible"] = True
    elif act == "archive":
        if m["origin"] == "core": die("core modules cannot be archived or deleted; disable or hide them")
        confirm(a, f"archive {a.id} (config and records moved to archive/, history preserved)")
        m["state"].update(archived=True, enabled=False)
        os.makedirs(s.p("archive", a.id), exist_ok=True)
        rp = s.p("records", f"{a.id}.jsonl")
        if os.path.exists(rp): shutil.copy2(rp, s.p("archive", a.id, "records.jsonl"))
    elif act == "restore":
        if not m["state"]["archived"]: die("module is not archived")
        confirm(a, f"restore {a.id}")
        if len(active_custom(s.cfg)) + 1 > s.cfg["limits"]["max_custom_features"]: die("limit of active custom features reached")
        m["state"].update(archived=False, enabled=True)
    elif act == "delete":
        if m["origin"] == "core": die("core (default) modules cannot be deleted; disable or hide them")
        if a.permanent:
            confirm(a, f"PERMANENTLY erase module {a.id}, its records and archive. This cannot be undone (config versions may still contain the definition)")
            for p in (s.p("records", f"{a.id}.jsonl"), ): 
                if os.path.exists(p): os.remove(p)
            shutil.rmtree(s.p("archive", a.id), ignore_errors=True)
            del mods[a.id]; s.audit("permanent_delete", a.id)
            s.save(f"permanently delete module {a.id}"); out({"ok": True, "permanent": True}); return
        confirm(a, f"delete custom module {a.id}: archives configuration and history (not permanent erase)")
        m["state"].update(archived=True, enabled=False, visible=False)
        os.makedirs(s.p("archive", a.id), exist_ok=True)
        rp = s.p("records", f"{a.id}.jsonl")
        if os.path.exists(rp): shutil.copy2(rp, s.p("archive", a.id, "records.jsonl"))
        json.dump(m, open(s.p("archive", a.id, "module.json"), "w"), indent=1)
    s.save(f"{act} module {a.id}"); out({"ok": True, "state": m["state"], "version": s.cfg["version"]})

def cmd_record(a):
    s = State(a.dir)
    if a.action == "list":
        rows = s.read(f"records/{a.module}.jsonl"); out(rows[-a.limit:]); return
    if a.module not in s.cfg["modules"]: die("unknown module")
    mod = s.cfg["modules"][a.module]
    if mod["state"]["archived"] or not mod["state"]["enabled"]: die("module is disabled or archived; enable it first")
    rel = f"records/{a.module}.jsonl"
    if a.action == "add":
        rec = {"record_id": nid("rec"), "module_id": a.module, "value": _num(a.value), "unit": a.unit, "currency": a.currency,
               "occurred_at": a.occurred_at or now(), "captured_at": now(), "category": a.category, "notes": a.notes,
               "capture_source": a.source, "created_by": a.by, "edited_by": None, "edit_history": [], "field_origin": {}}
        if a.value is None: die("--value is required")
        s.append(rel, rec); s.manifest(); out({"ok": True, "record_id": rec["record_id"], "occurred_at": rec["occurred_at"]}); return
    if a.action == "edit":
        rows = s.read(rel); r = next((x for x in rows if x["record_id"] == a.id), None)
        if not r: die("record not found")
        for kv in a.set:
            k, v = kv.split("=", 1)
            if k in ("record_id", "module_id", "created_by", "captured_at", "edit_history", "field_origin"): die(f"{k} is immutable")
            if a.by == "ai" and r.get("field_origin", {}).get(k) == "user_edited": die(f"'{k}' was edited by the user; AI may not overwrite it")
            old = r.get(k); new = _num(v) if k == "value" else v
            if old == new: continue
            r.setdefault("edit_history", []).append({"at": now(), "by": a.by, "field": k, "old": old, "new": new})
            r[k] = new; r.setdefault("field_origin", {})[k] = "user_edited" if a.by != "ai" else "ai_generated"
        r["edited_by"] = a.by; r["updated_at"] = now()
        s.write(rel, rows); s.manifest(); out({"ok": True, "record": r}); return

def _num(v):
    if v is None: return None
    try: return float(str(v).replace(",", "")) if re.fullmatch(r"-?[\d,]+(\.\d+)?", str(v)) else v
    except ValueError: return v

def cmd_discovery(a):
    s = State(a.dir)
    mod = s.cfg["modules"].get(a.module)
    if not mod or "discovery" not in mod.get("modes", []): die("module is not a discovery-capable module")
    if mod["state"]["archived"] or not mod["state"]["enabled"]: die("module is disabled or archived")
    d = json.load(open(a.json, encoding="utf-8")); rel = f"records/{a.module}.jsonl"; rows = s.read(rel)
    res = {"new": 0, "updated": 0, "duplicates": 0, "rejected": []}
    for item in (d if isinstance(d, list) else [d]):
        miss = [k for k in ("title", "summary", "evidence", "verification_status", "confidence", "confidence_rationale") if not item.get(k)]
        if not (item.get("source_url") or item.get("reference")): miss.append("source_url|reference")
        if item.get("taxonomy_group") and item["taxonomy_group"] not in TAXONOMY: miss.append(f"taxonomy_group in {TAXONOMY}")
        if item.get("verification_status") not in VSTATUS: miss.append(f"verification_status in {VSTATUS}")
        if item.get("confidence") not in VERIF: miss.append(f"confidence in {VERIF}")
        if miss: res["rejected"].append({"title": item.get("title"), "missing_or_invalid": miss}); continue
        key = item.get("source_url") or item.get("reference")
        ex = next((r for r in rows if (r.get("source_url") or r.get("reference")) == key), None)
        if ex:
            changed = {k: v for k, v in item.items() if ex.get(k) != v and k not in ("record_id",)}
            prot = [k for k in changed if ex.get("field_origin", {}).get(k) == "user_edited"]
            for k in prot: changed.pop(k)
            if changed:
                for k, v in changed.items(): ex.setdefault("edit_history", []).append({"at": now(), "by": "ai", "field": k, "old": ex.get(k), "new": v}); ex[k] = v
                ex["updated_at"] = now(); res["updated"] += 1
            else: res["duplicates"] += 1
            if prot: res.setdefault("protected_user_edits_kept", []).extend(prot)
            continue
        rec = {"record_id": nid("rec"), "module_id": a.module, "discovered_at": item.get("discovered_at") or now(), "status": "New",
               "created_at": now(), "updated_at": now(), "edit_history": [], "field_origin": {k: "ai_generated" for k in item}}
        rec.update(item); rows.append(rec); res["new"] += 1
    s.write(rel, rows); s.manifest(); out(res)

def cmd_run(a):
    s = State(a.dir)
    if a.module not in s.cfg["modules"]: die("unknown module")
    n = {k: getattr(a, k) for k in ("source_checks", "queries", "results", "unique", "new", "updated", "failures")}
    if n["unique"] > n["results"] or n["new"] > n["unique"]: die("counts inconsistent: need new <= unique <= results (never present queries as discoveries)")
    s.append("logs/runs.jsonl", {"run_id": nid("run"), "module_id": a.module, "at": now(), "depth": a.depth, **n, "note": a.note})
    s.manifest(); out({"ok": True, "logged": n})

def cmd_source(a):
    s = State(a.dir); src = s.cfg["sources"]
    if a.action == "add":
        confirm(a, f"add source {a.name} to {a.module}")
        sid = slug(a.name); src[sid] = {"id": sid, "name": a.name, "url": a.url, "module_id": a.module, "status": "not_checked", "last_checked": None, "error": None}
        s.save(f"add source {sid}")
    elif a.action == "remove":
        confirm(a, f"remove source {a.id} from future collection (collected findings are kept)")
        src.pop(a.id, None); s.save(f"remove source {a.id}")
    elif a.action == "health":
        if a.id not in src: die("unknown source")
        if a.status not in ("reachable", "failed", "changed"): die("health may only record a real check: reachable|failed|changed")
        src[a.id].update(status=a.status, last_checked=now(), error=a.error); s.save(f"source health {a.id}={a.status}")
    out({"ok": True, "sources": list(src)})

def cmd_permission(a):
    s = State(a.dir); P = s.cfg["permissions"]
    if a.kind == "profile":
        confirm(a, f"allow module {a.module} to read profile fields {a.fields}")
        P["profile_access"].setdefault(a.module, [])
        for f in a.fields: 
            if f not in P["profile_access"][a.module]: P["profile_access"][a.module].append(f)
    else:
        confirm(a, f"allow {a.module} to read {a.fields} from {a.source_module} for: {a.purpose}")
        P["module_access"].setdefault(a.module, []).append({"from": a.source_module, "fields": a.fields, "purpose": a.purpose, "granted_at": now()})
    s.save(f"permission {a.kind} {a.module}"); out({"ok": True, "permissions": P})

def cmd_item(a):  # goals / actions / decisions
    s = State(a.dir); rel = f"{a.kind}s.jsonl"; rows = s.read(rel)
    if a.action == "list": out(rows); return
    if a.action == "add":
        row = {f"{a.kind}_id": nid(a.kind[:3]), "title": a.title, "description": a.description, "status": a.status or ("proposed" if a.kind == "goal" else "Not started" if a.kind == "action" else "recorded"),
               "suggested_by": a.by, "approved": a.by == "user", "links": dict(kv.split("=", 1) for kv in (a.link or [])), "created_at": now(), "updated_at": now(), "history": []}
        if a.kind == "goal": row["target"] = None
        rows.append(row); s.write(rel, rows); out({"ok": True, "id": row[f"{a.kind}_id"]}); return
    if a.action == "update":
        r = next((x for x in rows if x[f"{a.kind}_id"] == a.id), None)
        if not r: die("not found")
        for kv in (a.set or []):
            k, v = kv.split("=", 1); r["history"].append({"at": now(), "field": k, "old": r.get(k), "new": v}); r[k] = v
        if a.approve: r["approved"] = True; r["history"].append({"at": now(), "field": "approved", "old": False, "new": True})
        r["updated_at"] = now(); s.write(rel, rows); out({"ok": True, "item": r})

def cmd_versions(a):
    s = State(a.dir)
    vs = sorted(f for f in os.listdir(s.p("versions")) if f.endswith(".json"))
    if a.action == "list": out([{"file": v, "note": json.load(open(s.p("versions", v))).get("_version_note")} for v in vs]); return
    def load(n): return json.load(open(s.p("versions", f"v{int(n):04d}.json")))
    if a.action == "diff":
        A, B = load(a.a), load(a.b); changes = []
        def walk(x, y, path=""):
            if isinstance(x, dict) and isinstance(y, dict):
                for k in sorted(set(x) | set(y)):
                    if k in ("_version_note", "version", "updated_at"): continue
                    walk(x.get(k), y.get(k), f"{path}/{k}")
            elif x != y: changes.append({"path": path, "from": x, "to": y})
        walk(A, B); out(changes); return
    if a.action == "rollback":
        snap = load(a.to); confirm(a, f"restore configuration to v{int(a.to):04d} (a NEW version is created; records are NOT rolled back)")
        cur = s.cfg["version"]; snap.pop("_version_note", None); snap["version"] = cur
        s.cfg = snap; s.save(f"rollback to v{int(a.to):04d}"); out({"ok": True, "new_version": s.cfg["version"]})

def _period(p, start=None, end=None):
    today = dt.datetime.now(dt.timezone.utc).date()
    m = {"today": (today, today), "yesterday": (today - dt.timedelta(1),) * 2, "7d": (today - dt.timedelta(6), today),
         "30d": (today - dt.timedelta(29), today), "3m": (today - dt.timedelta(90), today), "6m": (today - dt.timedelta(182), today),
         "1y": (today - dt.timedelta(365), today), "all": (dt.date.min, dt.date.max)}
    if p == "custom": return dt.date.fromisoformat(start), dt.date.fromisoformat(end)
    return m[p]

def cmd_analyse(a):
    s = State(a.dir); lo, hi = _period(a.period, a.start, a.end); rows = []
    for mid in a.module:
        for r in s.read(f"records/{mid}.jsonl"):
            try: d = dt.date.fromisoformat(str(r.get("occurred_at", ""))[:10])
            except ValueError: continue
            if lo <= d <= hi: rows.append((mid, d, r))
    groups = defaultdict(list)
    for mid, d, r in rows:
        if isinstance(r.get("value"), (int, float)): groups[(mid, r.get("unit") or r.get("currency") or "")].append((d, r["value"]))
    res = {"period": {"from": str(lo), "to": str(hi)}, "records_in_period": len(rows),
           "records_excluded_non_numeric": sum(1 for _, _, r in rows if not isinstance(r.get("value"), (int, float))), "groups": [], "coverage": {}}
    for (mid, unit), vals in groups.items():
        v = [x for _, x in vals]; days = sorted({d for d, _ in vals})
        span = (days[-1] - days[0]).days + 1
        g = {"module": mid, "unit_or_currency": unit, "n": len(v), "sum": sum(v), "mean": sum(v) / len(v), "min": min(v), "max": max(v),
             "days_with_records": len(days), "span_days": span, "days_without_records": span - len(days)}
        g["sufficiency"] = "thin: avoid firm conclusions" if len(v) < 5 else "ok"
        res["groups"].append(g)
    res["note"] = "Mixed units/currencies are reported separately and never summed. Missing days are gaps, not zeros."
    out(res)

def _rows_for(s, public=False):
    ex = {}
    for mid, m in s.cfg["modules"].items():
        if public and (m.get("sensitive") or any(k in mid for k in ())): continue
        rows = s.read(f"records/{mid}.jsonl")
        if public: rows = [{k: v for k, v in r.items() if k not in ("notes", "edit_history", "created_by", "edited_by")} for r in rows]
        if rows: ex[mid] = rows
    return ex

def cmd_export(a):
    s = State(a.dir); os.makedirs(a.out, exist_ok=True); data = _rows_for(s, a.public)
    if a.kind == "csv":
        for mid, rows in data.items():
            keys = sorted({k for r in rows for k in r if k not in ("edit_history", "field_origin")})
            with open(os.path.join(a.out, f"{dt.date.today()}_{mid}.csv"), "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=keys); w.writeheader()
                for r in rows: w.writerow({k: (json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v) for k, v in r.items() if k in keys})
        out({"ok": True, "files": sorted(os.listdir(a.out))})
    elif a.kind == "config":
        cfg = json.loads(json.dumps(s.cfg))
        if a.public: cfg.pop("owner_profile", None); cfg["permissions"]["profile_access"] = {}
        pkg = {"schema_version": SCHEMA, "exported_at": now(), "public": a.public, "config": cfg,
               "migration_manifest": {"note": "Declarative config; records exported separately. Standalone needs backend, database, auth, storage, integrations, secrets, scheduler, AI-provider config.",
               "record_counts": {k: len(v) for k, v in data.items()}}}
        p = os.path.join(a.out, f"{dt.date.today()}_config-package.json"); json.dump(pkg, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False); out({"ok": True, "file": p})
    elif a.kind == "xlsx":
        try: import openpyxl
        except ImportError: die("openpyxl not available; use `export csv` instead")
        wb = openpyxl.Workbook(); ws = wb.active; ws.title = "Dashboard Overview"
        ws.append(["OS", s.cfg["os"]["name"]]); ws.append(["Config version", s.cfg["version"]]); ws.append(["Exported", now()])
        ws.append(["Note", "Editable export surface; not the canonical database."])
        reg = wb.create_sheet("Feature Registry"); reg.append(["id", "name", "origin", "modes", "enabled", "visible", "archived"])
        arch = wb.create_sheet("Archived Features"); arch.append(["id", "name", "origin"])
        for m in s.cfg["modules"].values():
            reg.append([m["id"], m["name"], m["origin"], ",".join(m["modes"]), m["state"]["enabled"], m["state"]["visible"], m["state"]["archived"]])
            if m["state"]["archived"]: arch.append([m["id"], m["name"], m["origin"]])
        src = wb.create_sheet("Sources Registry"); src.append(["id", "name", "url", "module", "status", "last_checked", "error"])
        for x in s.cfg["sources"].values(): src.append([x["id"], x["name"], x["url"], x["module_id"], x["status"], x["last_checked"], x["error"]])
        sh = wb.create_sheet("Scan History"); sh.append(["run_id", "module", "at", "depth", "source_checks", "queries", "results", "unique", "new", "updated", "failures"])
        for r in s.read("logs/runs.jsonl"): sh.append([r["run_id"], r["module_id"], r["at"], r["depth"], r["source_checks"], r["queries"], r["results"], r["unique"], r["new"], r["updated"], r["failures"]])
        for mid, rows in data.items():
            keys = sorted({k for r in rows for k in r if k not in ("edit_history", "field_origin")})
            w = wb.create_sheet(mid[:31]); w.append(keys)
            for r in rows: w.append([json.dumps(r.get(k), ensure_ascii=False) if isinstance(r.get(k), (dict, list)) else r.get(k) for k in keys])
        p = os.path.join(a.out, f"{dt.date.today()}_intelligence-os.xlsx"); wb.save(p); out({"ok": True, "file": p, "sheets": wb.sheetnames})

def cmd_render(a):
    sys.path.insert(0, HERE)
    import render_dashboard
    s = State(a.dir); t = a.template or s.cfg["appearance"]["template"]
    if t not in ALL_TEMPLATES: die("unknown template")
    html = render_dashboard.render(s, t)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True); open(a.out, "w", encoding="utf-8").write(html)
    out({"ok": True, "file": a.out, "template": t, "note": "Static generated artefact (snapshot), not a live app."})

def cmd_validate(a):
    problems = []
    try: s = State(a.dir)
    except SystemExit: return
    c = s.cfg
    if c.get("schema_version") != SCHEMA: problems.append("schema_version mismatch")
    if c["os"]["context"] not in CONTEXTS: problems.append("invalid context")
    if len(active_custom(c)) > c["limits"]["max_custom_features"]: problems.append("active custom features exceed limit")
    ids = set()
    for mid in c["modules"]:
        for r in s.read(f"records/{mid}.jsonl"):
            if r["record_id"] in ids: problems.append(f"duplicate record_id {r['record_id']}")
            ids.add(r["record_id"])
            if r["module_id"] != mid: problems.append(f"record {r['record_id']} in wrong file")
    for f in (os.listdir(s.p("records")) if os.path.isdir(s.p("records")) else []):
        if f.endswith(".jsonl") and f[:-6] not in c["modules"]: problems.append(f"orphan records file {f}")
    for k in ("api_key", "apikey", "secret", "password", "token"):
        if k in json.dumps(c).lower(): problems.append(f"possible secret-like key '{k}' in config")
    mf = json.load(open(s.p("manifest.json")))
    for rel, h in mf["files"].items():
        full = s.p(*rel.split("/"))
        if not os.path.exists(full): problems.append(f"manifest file missing: {rel}")
        elif hashlib.sha256(open(full, "rb").read()).hexdigest() != h: problems.append(f"modified since manifest: {rel} (run `manifest` after intended edits)")
    out({"ok": not problems, "problems": problems, "config_version": c["version"], "modules": len(c["modules"])})
    sys.exit(0 if not problems else 1)


def cmd_search(a):
    s = State(a.dir); q = a.q.lower(); hits = []
    def add(kind, mid, r, text):
        if q in text.lower(): hits.append({"kind": kind, "module": mid, "id": r.get("record_id") or r.get(f"{kind}_id"), "title": r.get("title") or r.get("category") or str(r.get("value")), "date": str(r.get("occurred_at") or r.get("discovered_at") or r.get("created_at", ""))[:10]})
    for mid, m in s.cfg["modules"].items():
        if m["state"]["archived"] and not a.include_archived: continue
        if a.module and mid not in a.module: continue
        for r in s.read(f"records/{mid}.jsonl"): add("record", mid, r, json.dumps({k: v for k, v in r.items() if k not in ("edit_history", "field_origin")}, ensure_ascii=False))
    if not a.module:
        for kind in ("goal", "action", "decision"):
            for r in s.read(f"{kind}s.jsonl"): add(kind, None, r, json.dumps(r, ensure_ascii=False))
        for mid, m in s.cfg["modules"].items():
            add("module", mid, {"module_id": mid, "title": m["name"]}, m["name"] + " " + str(m.get("objective", "")))
    out({"query": a.q, "searched": "records of non-archived modules, goals, actions, decisions, module definitions (not files outside the state pack)", "hits": hits[:a.limit], "total": len(hits)})

def cmd_profile(a):
    s = State(a.dir)
    if a.action == "show": out(s.cfg["owner_profile"]); return
    confirm(a, f"set profile fields {a.set}")
    for kv in a.set: k, v = kv.split("=", 1); s.cfg["owner_profile"][k] = v
    s.save("profile update"); out({"ok": True})

def cmd_workspace(a):
    s = State(a.dir); W = s.cfg.setdefault("workspaces", {})
    if a.action == "list": out(W); return
    if a.action == "add":
        confirm(a, f"save workspace/view '{a.name}' with modules {a.modules} filters {a.filter}")
        for mid in a.modules or []:
            if mid not in s.cfg["modules"]: die(f"unknown module {mid}")
        W[slug(a.name)] = {"name": a.name, "modules": a.modules or [], "filters": dict(kv.split("=", 1) for kv in (a.filter or [])), "sort": a.sort, "created_at": now()}
    elif a.action == "remove":
        confirm(a, f"remove workspace {a.name}"); W.pop(slug(a.name), None)
    s.save(f"workspace {a.action} {a.name}"); out({"ok": True, "workspaces": list(W)})

def cmd_manifest(a): State(a.dir).manifest(); out({"ok": True})

def main():
    P = argparse.ArgumentParser(prog="ios.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = P.add_subparsers(dest="cmd", required=True)
    def mk(name, fn, dir_=True):
        x = sp.add_parser(name); x.set_defaults(fn=fn)
        if dir_: x.add_argument("--dir", default="os-state")
        x.add_argument("--confirm", action="store_true", help="owner has approved this change")
        return x
    x = mk("init", cmd_init); x.add_argument("--name"); x.add_argument("--name-origin", default="user", choices=["user", "auto_suggested", "temporary"])
    x.add_argument("--context", required=True); x.add_argument("--template", default="essential-minimal"); x.add_argument("--tagline"); x.add_argument("--monogram"); x.add_argument("--profile", nargs="*", help="key=value")
    x = mk("rename", cmd_rename); x.add_argument("--name", required=True)
    x = mk("template", cmd_template); x.add_argument("--template", required=True); x.add_argument("--preset", choices=["compact", "expanded", "research", "monitoring"])
    x = mk("module", cmd_module); x.add_argument("action", choices=["list", "add", "enable", "disable", "hide", "show", "archive", "restore", "delete"])
    x.add_argument("--id"); x.add_argument("--catalogue"); x.add_argument("--name"); x.add_argument("--objective"); x.add_argument("--modes"); x.add_argument("--fields"); x.add_argument("--limitations"); x.add_argument("--permanent", action="store_true")
    x = mk("record", cmd_record); x.add_argument("action", choices=["add", "edit", "list"]); x.add_argument("--module"); x.add_argument("--id"); x.add_argument("--value"); x.add_argument("--unit"); x.add_argument("--currency")
    x.add_argument("--occurred-at", dest="occurred_at"); x.add_argument("--category"); x.add_argument("--notes"); x.add_argument("--source", default="manual", choices=["manual", "quick_capture", "voice", "integration", "import"]); x.add_argument("--by", default="user"); x.add_argument("--set", nargs="*", default=[]); x.add_argument("--limit", type=int, default=20)
    x = mk("discovery", cmd_discovery); x.add_argument("--module", required=True); x.add_argument("--json", required=True)
    x = mk("run", cmd_run); x.add_argument("--module", required=True); x.add_argument("--depth", default="standard", choices=["quick", "standard", "deep"]); x.add_argument("--note")
    for k in ("source_checks", "queries", "results", "unique", "new", "updated", "failures"): x.add_argument("--" + k.replace("_", "-"), dest=k, type=int, default=0)
    x = mk("source", cmd_source); x.add_argument("action", choices=["add", "remove", "health"]); x.add_argument("--id"); x.add_argument("--name"); x.add_argument("--url"); x.add_argument("--module"); x.add_argument("--status"); x.add_argument("--error")
    x = mk("permission", cmd_permission); x.add_argument("kind", choices=["profile", "module"]); x.add_argument("--module", required=True); x.add_argument("--fields", nargs="+", required=True); x.add_argument("--source-module", dest="source_module"); x.add_argument("--purpose", default="")
    for kind in ("goal", "action", "decision"):
        x = mk(kind, cmd_item); x.set_defaults(kind=kind); x.add_argument("action", choices=["add", "update", "list"]); x.add_argument("--id"); x.add_argument("--title"); x.add_argument("--description"); x.add_argument("--status"); x.add_argument("--by", default="user", choices=["user", "ai"]); x.add_argument("--link", nargs="*"); x.add_argument("--set", nargs="*"); x.add_argument("--approve", action="store_true")
    x = mk("versions", cmd_versions); x.add_argument("action", choices=["list", "diff", "rollback"]); x.add_argument("--a"); x.add_argument("--b"); x.add_argument("--to")
    x = mk("analyse", cmd_analyse); x.add_argument("--module", nargs="+", required=True); x.add_argument("--period", default="30d", choices=["today", "yesterday", "7d", "30d", "3m", "6m", "1y", "all", "custom"]); x.add_argument("--start"); x.add_argument("--end")
    x = mk("export", cmd_export); x.add_argument("kind", choices=["csv", "xlsx", "config"]); x.add_argument("--out", default="exports"); x.add_argument("--public", action="store_true")
    x = mk("render", cmd_render); x.add_argument("--template"); x.add_argument("--out", default="exports/dashboard.html")
    x = mk("search", cmd_search); x.add_argument("--q", required=True); x.add_argument("--module", nargs="*"); x.add_argument("--limit", type=int, default=25); x.add_argument("--include-archived", action="store_true")
    x = mk("profile", cmd_profile); x.add_argument("action", choices=["show", "set"]); x.add_argument("--set", nargs="*", default=[])
    x = mk("workspace", cmd_workspace); x.add_argument("action", choices=["list", "add", "remove"]); x.add_argument("--name"); x.add_argument("--modules", nargs="*"); x.add_argument("--filter", nargs="*"); x.add_argument("--sort")
    x = mk("validate", cmd_validate); x = mk("manifest", cmd_manifest)
    a = P.parse_args()
    if a.cmd == "module" and a.action not in ("list", "add") and not a.id: die("--id required")
    if a.cmd == "record" and a.action in ("add", "edit", "list") and not a.module: die("--module required")
    if a.cmd == "permission" and a.kind == "module" and not a.source_module: die("--source-module required")
    a.fn(a)

if __name__ == "__main__": main()
