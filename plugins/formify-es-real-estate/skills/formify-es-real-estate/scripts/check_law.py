#!/usr/bin/env python3
"""
check_law.py: "takes the temperature" of the legal provisions a document depends on.

Reads references/controls.json. Each control has: id, documents it affects, provision, official url,
key_sentence (a literal fragment of the provision as it read at the last verification), verified (date) and
what_to_review. The script downloads the official page and checks that the sentence is still there.

Result per control:
  UNCHANGED     the literal sentence is still on the official page
  REVIEW        the page answers but the sentence is not there (possible amendment or format change)
  NOT CHECKED   the page could not be downloaded (no network, blocked, timeout): check with the agent's web tool

Usage: python3 check_law.py --doc <document type> [--region XX] [--all] [--json] [--controls ../references/controls.json]
Standard library only. Never stops the flow: it reports and continues.
"""
import argparse, json, os, re, sys, urllib.request, html as htmlmod

HERE = os.path.dirname(os.path.abspath(__file__))
CONTROLS = os.path.join(HERE, "..", "references", "controls.json")


def normalise(s):
    s = htmlmod.unescape(s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace(" ", " ")
    s = re.sub(r"\s+", " ", s)
    return s.lower()


def download(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; formify-skill-check/1.0)"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
    for enc in ("utf-8", "latin-1"):
        try:
            return data.decode(enc)
        except Exception:
            continue
    return data.decode("utf-8", "ignore")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--doc", default="")
    ap.add_argument("--region", default="")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--controls", default=CONTROLS)
    a = ap.parse_args()

    controls = json.load(open(a.controls, encoding="utf-8"))
    sel = []
    for c in controls:
        if a.all:
            sel.append(c); continue
        if a.doc and a.doc not in c.get("documents", []):
            continue
        regs = c.get("regions")
        if regs and a.region and a.region not in regs:
            continue
        if regs and not a.region:
            continue
        sel.append(c)

    out = []
    cache = {}
    for c in sel:
        url = c["url"]
        status, detail = "NOT CHECKED", ""
        try:
            if url not in cache:
                cache[url] = normalise(download(url))
            page = cache[url]
            sentence = normalise(c["key_sentence"])
            if sentence in page:
                status = "UNCHANGED"
            else:
                status = "REVIEW"
                detail = "the reference sentence is not on the official page"
        except Exception as e:
            detail = f"{type(e).__name__}: {e}"
        out.append({"id": c["id"], "provision": c["provision"], "status": status, "detail": detail,
                    "verified": c.get("verified"), "url": url, "what_to_review": c.get("what_to_review", "")})

    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return
    if not out:
        print("No controls for that selection.")
        return
    for o in out:
        line = f"[{o['status']}] {o['id']} {o['provision']} (last verified {o['verified']})"
        if o["detail"]:
            line += f": {o['detail']}"
        if o["status"] != "UNCHANGED" and o["what_to_review"]:
            line += f" → {o['what_to_review']}"
        print(line)
    n_rev = sum(1 for o in out if o["status"] == "REVIEW")
    n_nc = sum(1 for o in out if o["status"] == "NOT CHECKED")
    print(f"\nSummary: {len(out)} controls, {n_rev} to review, {n_nc} not checked.")


if __name__ == "__main__":
    main()
