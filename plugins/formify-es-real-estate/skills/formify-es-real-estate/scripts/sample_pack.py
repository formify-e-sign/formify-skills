#!/usr/bin/env python3
"""Builds the sample pack: every document type with example data, ready to be sent to the user's own e-mail
through Formify (references/sample-pack.md). Reads assets/samples/documents.json (same shape as tests/documents.json,
plus "message" per document) and writes one PDF per document and sample_pack.json (title, pdf, pages, message,
first signer's signatureBox) into --out.

  python3 scripts/sample_pack.py --out sample-pack [--organisation "Name"] [--lang en]
"""
import argparse, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SAMPLES = os.path.join(ROOT, "assets", "samples")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="sample-pack")
    ap.add_argument("--organisation", default="", help="organisation name for the header, if already known")
    ap.add_argument("--lang", default="en")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    cases = json.load(open(os.path.join(SAMPLES, "documents.json"), encoding="utf-8"))
    result = []
    for n, c in enumerate(cases, 1):
        data = json.load(open(os.path.join(SAMPLES, c["data"]), encoding="utf-8"))
        if a.organisation:
            for k in ("org_name", "organisation_name", "agency_name"):
                if k in data:
                    data[k] = a.organisation
        tmp = os.path.join(a.out, c["name"] + ".data.json")
        json.dump(data, open(tmp, "w", encoding="utf-8"), ensure_ascii=False)
        body, pdf = os.path.join(a.out, c["name"] + ".html"), os.path.join(a.out, c["name"] + ".pdf")
        cmd = [sys.executable, os.path.join(HERE, "fill.py"), "--template", os.path.join(ROOT, c["template"]), "--data", tmp, "--out", body, "--own", ""]
        if c.get("variant"):
            cmd += ["--variant", c["variant"]]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode:
            sys.exit("fill failed for %s: %s" % (c["name"], r.stdout + r.stderr))
        r = subprocess.run([sys.executable, os.path.join(HERE, "render_pdf.py"), "--html", body, "--signers", os.path.join(SAMPLES, c["signers"]),
                            "--out", pdf, "--profile", c.get("profile", "professional"), "--title", c["title"], "--ref", c["reference"], "--lang", a.lang],
                           capture_output=True, text=True)
        if r.returncode:
            sys.exit("render failed for %s: %s" % (c["name"], r.stdout + r.stderr))
        meta = json.load(open(os.path.splitext(pdf)[0] + ".signatures.json", encoding="utf-8"))
        os.remove(tmp)
        title = "%d. %s" % (n, c["title"])
        result.append({"name": c["name"], "title": title, "pdf": os.path.abspath(pdf), "pages": meta["pages"],
                       "message": c.get("message", "Sample %d of %d: %s." % (n, len(cases), c["title"])),
                       "signatureBox": meta["signers"][0]["signatureBox"] if meta["signers"] else None})
        print("%s  (%d pages)" % (title, meta["pages"]))
    json.dump(result, open(os.path.join(a.out, "sample_pack.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("OK:", os.path.join(a.out, "sample_pack.json"))


if __name__ == "__main__":
    main()
