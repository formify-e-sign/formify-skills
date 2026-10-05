#!/usr/bin/env python3
"""Route 5 of the PDF ladder: the hand-over, document text plus a complete field specification.

Written whenever no PDF can be made here, and also next to every standard-library PDF so that the
recipient can check what was built. One fixed shape, the developer's (formify-pdf-forms,
references/hand-over.md): 1 text, 2 field table, 3 signature areas, 4 what remains.

    python3 scripts/handover.py --html body.html --signers signers.json --out "<title>-spec.md" \
        --title "<title>" [--reason "why no PDF was produced here"]
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stdlib_pdf import parse_blocks, lay_out, winansi_problems  # noqa: E402


def kind_of(f):
    n = f["name"]
    if "tink-upload-attachment" in n:
        return "upload"
    if "tink-scan-id" in n or "tink-uploaded-image" in n or f.get("read_only") and "scan" in n:
        return "image"
    if f["height"] > 30:
        return "multiline"
    return "text"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", required=True)
    ap.add_argument("--signers", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--title", default="Document")
    ap.add_argument("--reason", default="No renderer and no PDF library here, so this is the complete specification.")
    a = ap.parse_args()

    body = open(a.html, encoding="utf-8").read()
    signers = json.load(open(a.signers, encoding="utf-8"))
    if isinstance(signers, dict):
        signers = signers.get("signers", [])
    blocks, fields = parse_blocks(body)

    # Pages from the standard-library layout when the text allows it; "-" otherwise.
    pages = {}
    all_text = " ".join(c["text"] for b in blocks if b[0] == "row" for c in b[1])
    if not winansi_problems(all_text):
        form = lay_out(blocks, signers, {}, [a.title])
        for w in form.widgets:
            pages[w["name"]] = w["page"] + 1

    out = ["# " + a.title + ": hand-over", "", a.reason, "", "## 1. Text", ""]
    headers = []
    last_section = ""
    anchors = {}
    for b in blocks:
        if b[0] == "h":
            out.append("#" * min(b[1] + 1, 4) + " " + b[2])
            out.append("")
            last_section = b[2]
            headers = []
        elif b[0] == "p":
            out.append(b[1])
            out.append("")
        elif b[0] == "sig":
            out.append("(signature areas)")
            out.append("")
        elif b[0] == "row":
            cells = b[1]
            if any(c.get("cab") for c in cells):
                headers = [c["text"] for c in cells]
                out.append("| " + " | ".join(t or " " for t in headers) + " |")
                out.append("|" + "---|" * len(headers))
                continue
            key = next((c["text"] for c in cells if c["k"]), "")
            others = [c["text"] for c in cells if not c["k"]]
            for c in cells:
                for f in c["fields"]:
                    col = cells.index(c)
                    anchors[f["name"]] = key or last_section
                    if col < len(headers) and headers[col]:
                        anchors[f["name"]] = (key + " (" + headers[col] + ")") if key else headers[col]
            if headers:
                out.append("| " + " | ".join([key] + others) + " |")
            elif any(len(t) > 80 for t in others):
                if key:
                    out.append("**" + key + "**")
                    out.append("")
                for t in others:
                    out.append(t)
                    out.append("")
            else:
                out.append((key + ": " if key else "") + " / ".join(t for t in others if t))
                out.append("")

    out += ["", "## 2. Fields", "",
            "| # | name | label | kind | required | options | read-only | page | anchor | size |",
            "|---|---|---|---|---|---|---|---|---|---|"]
    for i, f in enumerate(fields, 1):
        k = kind_of(f)
        size = "%d × %d" % (f["width"], f["height"]) if k in ("image", "upload") else "-"
        label = anchors.get(f["name"], f["name"].split("|")[0])
        out.append("| %d | %s | %s | %s | %s | - | %s | %s | \"%s\" | %s |" % (
            i, f["name"].replace("|", "\\|"), label, k, "yes" if f["required"] and not f["read_only"] else "no",
            "yes" if f["read_only"] else "no", pages.get(f["name"], "-"), label, size))

    out += ["", "## 3. Signatures", ""]
    for s in signers:
        cap = s.get("role", "") + (" / " + s["role_tr"] if s.get("role_tr") and s["role_tr"] != s.get("role") else "")
        line = "- " + cap + (" (" + s["name"] + ")" if s.get("name") else "") + ": after the closing paragraph, empty space of 219 × 58 pt, caption only"
        if s.get("id_scan"):
            line += ", ID-scan placeholder 218 × 138 pt beside it"
        out.append(line)
    out += ["", "## 4. What remains", "",
            "Open this in an assistant with a PDF library (Claude Desktop has one, and this skill's scripts produce the exact layout wherever a browser or WeasyPrint exists) and ask for the PDF; every field above is already decided.", ""]
    open(a.out, "w", encoding="utf-8").write("\n".join(out))
    print("wrote " + a.out)


if __name__ == "__main__":
    main()
