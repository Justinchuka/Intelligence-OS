"""Renders a static, self-contained HTML dashboard from an Intelligence OS state pack.
Ten genuinely different layout systems share one data model. No external scripts or fonts.
All data is HTML-escaped. Output is a snapshot, not a live app."""
import html, json
from collections import defaultdict
E = lambda x: html.escape("" if x is None else str(x), quote=True)

SECTIONS = ["Overview", "Discoveries", "Trackers", "Goals", "Actions", "Analysis", "Library", "Reports", "History", "Administration"]

def model(s):
    c = s.cfg; mods = c["modules"]
    disc, trk, counts = [], [], {}
    for mid, m in mods.items():
        if m["state"]["archived"]: continue
        rows = s.read(f"records/{mid}.jsonl"); counts[mid] = len(rows)
        if "discovery" in m.get("modes", []): disc += [dict(r, _m=m["name"]) for r in rows]
        if "tracking" in m.get("modes", []) and m["state"]["visible"]: trk.append((m, rows))
    disc.sort(key=lambda r: r.get("discovered_at", ""), reverse=True)
    return dict(cfg=c, name=c["os"]["name"], tagline=c["os"].get("tagline", ""), mono=c["os"].get("monogram", "IO"),
        mods=[m for m in mods.values() if not m["state"]["archived"]], disc=disc, trk=trk, counts=counts,
        goals=s.read("goals.jsonl"), actions=s.read("actions.jsonl"), decisions=s.read("decisions.jsonl"),
        runs=s.read("logs/runs.jsonl"), sources=list(c["sources"].values()), version=c["version"], updated=c.get("updated_at", ""))

def spark(vals, w=140, h=34):
    v = [x for x in vals if isinstance(x, (int, float))]
    if len(v) < 2: return '<span class="muted">not enough data</span>'
    lo, hi = min(v), max(v); rng = (hi - lo) or 1
    pts = " ".join(f"{i * w / (len(v) - 1):.1f},{h - 3 - (x - lo) / rng * (h - 6):.1f}" for i, x in enumerate(v))
    return f'<svg class="spark" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="trend"><polyline fill="none" stroke="currentColor" stroke-width="2" points="{pts}"/></svg>'

def bars(pairs, w=360):
    if not pairs: return '<p class="muted">No records yet.</p>'
    mx = max(v for _, v in pairs) or 1; rows = []
    for i, (k, v) in enumerate(pairs):
        rows.append(f'<text x="0" y="{i*22+14}" font-size="11" fill="currentColor">{E(k[:26])}</text><rect x="150" y="{i*22+4}" width="{v/mx*(w-190):.1f}" height="12" rx="2" fill="currentColor" opacity=".55"/><text x="{155+v/mx*(w-190):.1f}" y="{i*22+14}" font-size="11" fill="currentColor">{v}</text>')
    return f'<svg viewBox="0 0 {w} {len(pairs)*22+6}" width="100%" style="max-width:{w}px" role="img" aria-label="records per module">{"".join(rows)}</svg>'

def tbl(head, rows, cls=""):
    if not rows: return '<p class="muted">Nothing recorded.</p>'
    return f'<div class="scroll"><table class="{cls}"><thead><tr>{"".join(f"<th>{E(h)}</th>" for h in head)}</tr></thead><tbody>' + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>"

def conf(r): return f'<span class="chip">{E(r.get("confidence","Unverified"))}</span>'
def link(r):
    u = r.get("source_url") or ""
    return f'<a href="{E(u)}" rel="noopener noreferrer nofollow">{E(r.get("source_name") or u[:40])}</a>' if u.startswith(("http://", "https://")) else E(r.get("reference", ""))

def parts(m):
    P = {}
    P["Overview"] = (f'<div class="stats"><div class="stat"><b>{len([x for x in m["mods"] if x["state"]["enabled"]])}</b><span>enabled modules</span></div><div class="stat"><b>{sum(m["counts"].values())}</b><span>records stored</span></div><div class="stat"><b>{len(m["goals"])}</b><span>goals</span></div><div class="stat"><b>{len([a for a in m["actions"] if a["status"] not in ("Completed","Cancelled")])}</b><span>open actions</span></div></div>'
        + bars([(x["name"], m["counts"].get(x["id"], 0)) for x in m["mods"] if m["counts"].get(x["id"])]))
    P["Discoveries"] = tbl(["Finding", "Module", "Group", "Verification", "Confidence", "Source", "Found"], [[E(r.get("title")), E(r["_m"]), E(r.get("taxonomy_group","")), E(r.get("verification_status")), conf(r), link(r), E(str(r.get("discovered_at", ""))[:10])] for r in m["disc"][:40]], "sortable")
    t = ""
    for mod, rows in m["trk"]:
        vals = [r.get("value") for r in rows]; last = rows[-1] if rows else {}
        t += f'<div class="trk"><h4>{E(mod["name"])}</h4><p>{spark(vals)} <span class="muted">{len(rows)} records' + (f'; latest {E(last.get("value"))} {E(last.get("unit") or last.get("currency") or "")} on {E(str(last.get("occurred_at",""))[:10])}' if rows else "") + "</span></p></div>"
    P["Trackers"] = t or '<p class="muted">No tracking modules with data.</p>'
    P["Goals"] = tbl(["Goal", "Status", "Description"], [[E(g["title"]), E(g["status"]), E(g.get("description"))] for g in m["goals"]])
    P["Actions"] = tbl(["Action", "Status", "Suggested by", "Approved"], [[E(a["title"]), E(a["status"]), E(a["suggested_by"]), "yes" if a["approved"] else "awaiting approval"] for a in m["actions"]])
    P["Analysis"] = '<p class="muted">Run <code>ios.py analyse</code> for period summaries; this snapshot shows record counts and trends only. Observations, interpretations and recommendations are kept separate in reports.</p>'
    P["Library"] = '<p class="muted">Logical folders: Discoveries, Opportunities, Research, Trackers, Analyses, Goals &amp; Actions, Sources, Decisions, Reports, Exports, Configuration, Archive. Physical storage is this state pack plus files you download.</p>'
    P["Reports"] = '<p class="muted">Exports available through ios.py: CSV, XLSX (if openpyxl), configuration package, this HTML snapshot.</p>'
    P["History"] = tbl(["Run", "Module", "Checks", "Queries", "Results", "Unique", "New", "Updated", "Failures"], [[E(r["at"][:16]), E(r["module_id"]), r["source_checks"], r["queries"], r["results"], r["unique"], r["new"], r["updated"], r["failures"]] for r in m["runs"][-20:]]) + "<h4>Decisions</h4>" + tbl(["Decision", "Outcome"], [[E(d["title"]), E(d["status"])] for d in m["decisions"]])
    P["Administration"] = tbl(["Module", "Origin", "Modes", "Enabled", "Visible"], [[E(x["name"]), E(x["origin"]), E(",".join(x["modes"])), "yes" if x["state"]["enabled"] else "no", "yes" if x["state"]["visible"] else "no"] for x in m["mods"]]) + "<h4>Source health (only real checks)</h4>" + tbl(["Source", "Status", "Last checked"], [[E(x["name"]), E(x["status"]), E(x["last_checked"] or "never")] for x in m["sources"]])
    return P

BASE = """*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}body{margin:0;font:15px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
h1,h2,h3,h4{line-height:1.2;margin:.2em 0 .5em}.muted{opacity:.65}a{color:inherit}.scroll{overflow-x:auto}table{border-collapse:collapse;width:100%}th,td{text-align:left;padding:.45em .6em;vertical-align:top}
.chip{white-space:nowrap;display:inline-block;padding:.05em .55em;border-radius:99px;font-size:.8em;border:1px solid currentColor}.stats{display:flex;flex-wrap:wrap;gap:1rem;margin-bottom:1rem}.stat b{display:block;font-size:2rem;line-height:1}
.spark{vertical-align:middle}code{font-family:ui-monospace,monospace;font-size:.9em}.hidden{display:none!important}
.snap{font-size:.8em;opacity:.65}
body *{min-width:0}img,svg{max-width:100%}.scroll{max-width:100%}p,h1,h2,h3,h4{overflow-wrap:break-word}th,td{min-width:5.5em}nav{display:flex;flex-wrap:wrap;gap:.2rem .8rem}aside nav,.q nav{flex-direction:column}.spark{width:140px!important;max-width:100%}input{max-width:100%}"""
JS = """<script>(function(){var t=document.querySelectorAll('[data-tab]');var s=document.querySelectorAll('[data-sec]');function show(n){s.forEach(function(x){x.classList.toggle('hidden',x.dataset.sec!==n&&document.body.dataset.tabs==='1')});t.forEach(function(x){x.classList.toggle('on',x.dataset.tab===n)})}t.forEach(function(x){x.addEventListener('click',function(e){e.preventDefault();show(x.dataset.tab)})});
var q=document.getElementById('q');if(q)q.addEventListener('input',function(){var v=q.value.toLowerCase();document.querySelectorAll('tbody tr').forEach(function(r){r.classList.toggle('hidden',v&&r.textContent.toLowerCase().indexOf(v)<0)})});if(document.body.dataset.tabs==='1')show('Overview')})();</script>"""
def head(m, css, tabs=False):
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(m["name"])}</title><style>{BASE}{css}</style></head><body data-tabs="{1 if tabs else 0}">'
def foot(m): return f'<p class="snap">Static snapshot generated from state pack · config v{m["version"]} · {E(m["updated"])} · not a live application</p>{JS}</body></html>'
def sec(P, names, wrap="section"): return "".join(f'<{wrap} data-sec="{n}" id="{n}"><h2>{n}</h2>{P[n]}</{wrap}>' for n in names)
def nav(names, cls="nav"): return f'<nav class="{cls}">' + "".join(f'<a href="#{n}" data-tab="{n}">{n}</a>' for n in names) + "</nav>"
def navlinks(names): return "".join(f'<a href="#{n}" data-tab="{n}">{n}</a>' for n in names)
def lead(m):
    r = m["disc"][0] if m["disc"] else None
    return f'<h2>{E(r["title"])}</h2><p>{E(r.get("summary"))}</p><p>{conf(r)} {link(r)}</p>' if r else '<h2>No discoveries yet</h2><p class="muted">Run a discovery module to populate this space.</p>'

def t_essential(m, P):
    css = "body{background:#fafaf8;color:#1c1c1c;font-family:Georgia,'Times New Roman',serif}main{max-width:720px;margin:0 auto;padding:4rem 1.25rem}h1{font-size:2.6rem;font-weight:400;letter-spacing:-.02em}h2{font-weight:400;font-size:1.5rem;margin-top:3.2rem;border-top:1px solid #ddd;padding-top:1.2rem}nav a{margin-right:1rem;font-family:system-ui;font-size:.85rem;color:#666;text-decoration:none}th{font-family:system-ui;font-size:.75rem;text-transform:uppercase;letter-spacing:.08em;color:#777;border-bottom:1px solid #ddd}td{border-bottom:1px solid #eee}"
    return head(m, css) + f'<main><h1>{E(m["name"])}</h1><p class="muted">{E(m["tagline"])}</p>{nav(SECTIONS)}{sec(P, SECTIONS)}</main>' + foot(m)
def t_ops(m, P):
    css = "body{background:#0b0f14;color:#d7e0ea;font-size:13px}.app{display:grid;grid-template-columns:200px 1fr;min-height:100vh}aside{background:#0f151d;border-right:1px solid #1e2a38;padding:1rem;position:sticky;top:0;height:100vh}aside a{display:block;padding:.35rem .5rem;color:#8aa0b6;text-decoration:none;border-left:2px solid transparent}aside a.on,aside a:hover{color:#4ade80;border-color:#4ade80}.strip{display:flex;gap:2rem;padding:.6rem 1rem;background:#0f151d;border-bottom:1px solid #1e2a38;font-family:ui-monospace,monospace}.grid{display:grid;grid-template-columns:repeat(12,1fr);gap:.6rem;padding:.8rem}section{grid-column:span 6;background:#111923;border:1px solid #1e2a38;padding:.7rem}section[data-sec=Overview],section[data-sec=Discoveries]{grid-column:span 12}th{color:#6b8199;border-bottom:1px solid #1e2a38}td{border-bottom:1px solid #16202c}.stat b{color:#4ade80}@media(max-width:760px){.app{grid-template-columns:1fr}aside{position:static;height:auto}section{grid-column:span 12}}"
    return head(m, css, True) + f'<div class="app"><aside><h3>{E(m["mono"])} {E(m["name"])}</h3>{nav(SECTIONS,"")}</aside><div><div class="strip"><span>MODULES {len(m["mods"])}</span><span>RECORDS {sum(m["counts"].values())}</span><span>SOURCES {len(m["sources"])}</span><span>RUNS {len(m["runs"])}</span><input id="q" placeholder="filter rows" style="margin-left:auto;background:#0b0f14;color:inherit;border:1px solid #1e2a38"></div><div class="grid">{sec(P, SECTIONS)}</div></div></div>' + foot(m)
def t_glass(m, P):
    css = "body{background:linear-gradient(135deg,#5b6cf0,#b06ae0 45%,#f08aa8);background-attachment:fixed;color:#fff;min-height:100vh}header{text-align:center;padding:2rem 1rem 0}.pill{display:inline-flex;gap:.3rem;flex-wrap:wrap;justify-content:center;background:rgba(255,255,255,.18);backdrop-filter:blur(14px);padding:.35rem;border-radius:99px;margin-top:1rem}.pill a{padding:.3rem .8rem;border-radius:99px;text-decoration:none}.pill a.on{background:rgba(255,255,255,.3)}main{max-width:1000px;margin:1.5rem auto;padding:0 1rem;display:grid;gap:1.2rem}section{background:rgba(255,255,255,.16);backdrop-filter:blur(18px);border:1px solid rgba(255,255,255,.35);border-radius:22px;padding:1.2rem 1.4rem;box-shadow:0 20px 50px rgba(30,20,80,.25)}section:nth-child(even){transform:translateX(18px)}section:nth-child(odd){transform:translateX(-18px)}th,td{border-bottom:1px solid rgba(255,255,255,.25)}@media(max-width:760px){section{transform:none!important}}"
    return head(m, css, True) + f'<header><h1>{E(m["name"])}</h1><div class="muted">{E(m["tagline"])}</div><div class="pill">{navlinks(SECTIONS)}</div></header><main>{sec(P, SECTIONS)}</main>' + foot(m)
def t_editorial(m, P):
    css = "body{background:#f4efe6;color:#201a14;font-family:Georgia,serif}.mast{border-top:6px double #201a14;border-bottom:1px solid #201a14;text-align:center;padding:1rem}.mast h1{font-size:3.2rem;margin:0;letter-spacing:.04em}.wrap{display:grid;grid-template-columns:2fr 1fr;gap:2rem;max-width:1100px;margin:1.5rem auto;padding:0 1rem}.lead{grid-column:1;border-bottom:1px solid #201a14}.lead h2{font-size:2.4rem}.side{grid-column:2;grid-row:1/span 3;border-left:1px solid #201a14;padding-left:1.2rem}h2{font-style:italic}@media(max-width:760px){.wrap{grid-template-columns:1fr}.side{grid-column:1;grid-row:auto;border:0;padding:0}}"
    return head(m, css) + f'<div class="mast"><h1>{E(m["name"])}</h1><div>{E(m["tagline"])}</div></div><div class="wrap"><article class="lead">{lead(m)}</article><div>{sec(P,["Discoveries","Goals","Analysis"])}</div><aside class="side">{sec(P,["Overview","Trackers","Actions","Library","Reports","History","Administration"],"div")}</aside></div>' + foot(m)
def t_bento(m, P):
    css = "body{background:#eef1f5;color:#12151a}.bento{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:minmax(150px,auto);gap:12px;padding:16px;max-width:1200px;margin:auto}section{background:#fff;border-radius:20px;padding:1rem;overflow:auto}section:nth-child(1){grid-column:span 2;grid-row:span 2;background:#12151a;color:#fff}section:nth-child(2){grid-column:span 2}section:nth-child(3){grid-row:span 2}section:nth-child(6){grid-column:span 2}section:nth-child(9){grid-column:span 2}h1{padding:16px 16px 0;max-width:1200px;margin:auto}@media(max-width:760px){.bento{grid-template-columns:1fr 1fr}section:nth-child(n){grid-column:span 2;grid-row:auto}}"
    return head(m, css) + f'<h1>{E(m["name"])}</h1><div class="bento">{sec(P, SECTIONS)}</div>' + foot(m)
def t_enterprise(m, P):
    css = "body{background:#f3f4f6;color:#111827}.top{background:#1f2a44;color:#fff;padding:.7rem 1rem;display:flex;gap:1rem;align-items:center}.shell{display:grid;grid-template-columns:230px 1fr}aside{background:#fff;border-right:1px solid #d1d5db;min-height:100vh;padding:.6rem}aside a{display:block;padding:.5rem .7rem;text-decoration:none;border-radius:4px}aside a.on{background:#e0e7ff;font-weight:600}.crumb{padding:.7rem 1rem;color:#6b7280}main{padding:0 1rem 2rem}section{background:#fff;border:1px solid #d1d5db;border-radius:6px;padding:1rem;margin-bottom:1rem}th{background:#f9fafb;border-bottom:2px solid #d1d5db}td{border-bottom:1px solid #e5e7eb}tr:nth-child(even) td{background:#fafafa}@media(max-width:760px){.shell{grid-template-columns:1fr}}"
    return head(m, css, True) + f'<div class="top"><b>{E(m["mono"])}</b> {E(m["name"])}<input id="q" placeholder="Filter table rows" style="margin-left:auto"></div><div class="shell"><aside>{nav(SECTIONS,"")}</aside><div><div class="crumb">Home / {E(m["name"])}</div><main>{sec(P, SECTIONS)}</main></div></div>' + foot(m)
def t_atelier(m, P):
    css = "body{background:#fbf3ee;color:#4a3a36;font-family:'Palatino Linotype',Palatino,serif}main{max-width:860px;margin:0 auto;padding:3rem 1rem;text-align:center}h1{font-weight:400;font-size:2.4rem;color:#9a6b5f}section{background:#fffaf6;border:1px solid #ecd9cf;border-radius:28px;padding:1.6rem;margin:1.4rem 0;text-align:left;box-shadow:0 8px 30px #e9d3c8}h2{text-align:center;font-weight:400;color:#9a6b5f;letter-spacing:.12em;text-transform:uppercase;font-size:1rem}th,td{border-bottom:1px solid #f0e2da}"
    return head(m, css) + f'<main><h1>{E(m["name"])}</h1><p>{E(m["tagline"])}</p>{sec(P, SECTIONS)}</main>' + foot(m)
def t_observatory(m, P):
    css = "body{background:#0a1020;color:#dbe6ff}header{padding:1rem 1.5rem}.hero{padding:1rem 1.5rem;border-bottom:1px solid #20305a}.hero svg{max-height:220px}.cols{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;padding:1.5rem}.trk{padding:.5rem;border-left:3px solid #6ea8ff;margin-bottom:.8rem;color:#6ea8ff}.trk h4,.trk p{color:#dbe6ff}@media(max-width:760px){.cols{grid-template-columns:1fr}}"
    return head(m, css) + f'<header><h1>{E(m["name"])}</h1></header><div class="hero"><h2>Records per module</h2>{bars([(x["name"], m["counts"].get(x["id"], 0)) for x in m["mods"] if m["counts"].get(x["id"])], 700)}</div><div class="hero">{sec(P,["Trackers"],"div")}</div><div class="cols"><div>{sec(P,["Discoveries","History"],"div")}</div><div>{sec(P,["Overview","Goals","Actions","Analysis","Library","Reports","Administration"],"div")}</div></div>' + foot(m)
def t_workspace(m, P):
    css = "body{background:#f6f7f9;color:#1f2933}.ws{display:grid;grid-template-columns:200px 1.2fr 1fr;gap:1rem;padding:1rem;align-items:start}.col{background:#fff;border:1px solid #dde1e6;border-radius:8px;padding:.8rem}.col h3{margin-top:0}.q a{display:block;padding:.3rem 0;text-decoration:none}@media(max-width:900px){.ws{grid-template-columns:1fr}}"
    return head(m, css) + f'<div class="ws"><div class="col q"><h3>Queue</h3>{nav(SECTIONS,"")}<p class="muted">{len([a for a in m["actions"] if a["status"]=="Not started"])} not started<br>{len([a for a in m["actions"] if a["status"]=="In progress"])} in progress</p></div><div class="col">{sec(P,["Actions","Goals","Discoveries"],"div")}</div><div class="col">{sec(P,["Overview","History","Trackers","Analysis","Library","Reports","Administration"],"div")}</div></div>' + foot(m)
def t_frontier(m, P):
    css = "body{background:#111;color:#f2f2f2;scroll-snap-type:y proximity}.v{position:fixed;left:0;top:0;bottom:0;width:48px;writing-mode:vertical-rl;background:#ff4d2e;color:#111;padding:.6rem 0;text-align:center;font-weight:700;letter-spacing:.2em}.rail{position:fixed;right:12px;top:12px;display:flex;flex-direction:column;gap:.2rem;font-size:.75rem;z-index:2;text-align:right}.rail a{text-decoration:none;opacity:.7}.f{min-height:80vh;margin-left:72px;padding:2rem;scroll-snap-align:start;border-bottom:1px solid #333}.f h2{font-size:clamp(2rem,7vw,5rem);margin:0;color:#ff4d2e;transform:rotate(-2deg)}.f:nth-of-type(even){margin-left:18vw;background:#181818}.big{font-size:clamp(3rem,14vw,10rem);font-weight:800;line-height:.9;color:#ff4d2e}@media(max-width:760px){.f:nth-of-type(even){margin-left:72px}.rail{display:none}}"
    big = f'<div class="big">{sum(m["counts"].values())}</div><div class="muted">records · {len(m["mods"])} modules</div>'
    return head(m, css) + f'<div class="v">{E(m["name"])}</div><div class="rail">{navlinks(SECTIONS)}</div>' + "".join(f'<section class="f" data-sec="{n}" id="{n}"><h2>{n}</h2>{big if n=="Overview" else ""}{P[n]}</section>' for n in SECTIONS) + foot(m)

TEMPLATES = {"essential-minimal": t_essential, "intelligence-operations": t_ops, "atmosphere-glass": t_glass, "editorial-magazine": t_editorial,
    "mosaic-bento": t_bento, "enterprise-structured": t_enterprise, "atelier-soft-luxury": t_atelier, "observatory-data": t_observatory,
    "workspace-productivity": t_workspace, "frontier-experimental": t_frontier}

def render(s, template):
    m = model(s); return TEMPLATES[template](m, parts(m))
