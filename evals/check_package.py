#!/usr/bin/env python3
"""Mechanical package checks. Usage: python evals/check_package.py <skill-folder> [--zip file.zip]"""
import os, re, sys, zipfile, json
root = os.path.abspath(sys.argv[1]); fails = []; ok = []
def chk(c, m): (ok if c else fails).append(m)
sk = open(os.path.join(root, "SKILL.md"), encoding="utf-8").read()
fm = re.match(r"---\n(.*?)\n---\n", sk, re.S); chk(bool(fm), "SKILL.md has frontmatter")
meta = dict(l.split(": ", 1) for l in fm.group(1).splitlines() if ": " in l) if fm else {}
chk(set(meta) <= {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}, f"only spec frontmatter keys: {sorted(meta)}")
chk(meta.get("name") == os.path.basename(root), "name matches folder name")
chk(re.fullmatch(r"[a-z0-9-]{1,64}", meta.get("name", "")) is not None, "name is lowercase kebab-case")
chk(0 < len(meta.get("description", "")) <= 200, f"description <= 200 chars ({len(meta.get('description',''))})")
chk(len(sk.splitlines()) < 500, f"SKILL.md under 500 lines ({len(sk.splitlines())})")
for pth in sorted(set(re.findall(r"`((?:references|scripts|assets|examples|evals|docs)/[A-Za-z0-9_./*<>-]+)`", sk))):
    if any(c in pth for c in "*<>"): continue
    chk(os.path.exists(os.path.join(root, pth)), f"SKILL.md path exists: {pth}")
# every reference file is mentioned in SKILL.md (no orphans)
for f in os.listdir(os.path.join(root, "references")):
    if f.endswith(".md") and f != "README.md": chk(f in sk or f in ("INDEX.md",), f"reference routed from SKILL.md: {f}")
# no empty files, no secrets
secret = re.compile(r"(sk-[A-Za-z0-9]{20,}|api[_-]?key\s*[:=]\s*['\"][^'\"]{8,}|BEGIN (RSA|PRIVATE) KEY|AKIA[0-9A-Z]{16})", re.I)
for d, _, fs in os.walk(root):
    for f in fs:
        p = os.path.join(d, f); rel = os.path.relpath(p, root)
        if "__pycache__" in rel: continue
        chk(os.path.getsize(p) > 0, f"non-empty: {rel}")
        if f.endswith((".md", ".py", ".json", ".jsonl", ".html")): chk(not secret.search(open(p, encoding="utf-8", errors="ignore").read()), f"no secret patterns: {rel}")
for d, _, fs in os.walk(root):
    chk(not (not fs and not _ and "__pycache__" not in d), f"no empty folder: {os.path.relpath(d, root)}")
# internal markdown links
for d, _, fs in os.walk(root):
    for f in fs:
        if f.endswith(".md"):
            for l in re.findall(r"\]\(([^)#]+\.md)\)", open(os.path.join(d, f), encoding="utf-8").read()):
                if not l.startswith("http"): chk(os.path.exists(os.path.join(d, l)), f"link ok: {os.path.relpath(os.path.join(d,f),root)} -> {l}")
if "--zip" in sys.argv:
    z = zipfile.ZipFile(sys.argv[sys.argv.index("--zip") + 1]); names = z.namelist()
    chk(all(n.startswith(os.path.basename(root) + "/") for n in names), "ZIP: every entry inside the skill folder (no loose root files)")
    chk(f"{os.path.basename(root)}/SKILL.md" in names, "ZIP: SKILL.md present")
    chk(not any("__pycache__" in n for n in names), "ZIP: no caches")
print(f"PASS {len(ok)}  FAIL {len(fails)}")
for m in fails: print("FAIL:", m)
sys.exit(1 if fails else 0)
