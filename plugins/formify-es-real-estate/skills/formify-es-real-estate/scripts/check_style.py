#!/usr/bin/env python3
"""
check_style.py: reviews a document's HTML before rendering. The generic checks are built in; the language-
and segment-specific ones come from references/style.json, so this script is never edited per segment.

Built-in checks (always on):
  1. Unfilled markers: {{...}}, [[...]], REQUIRED, TODO, XXX.
  2. Dashes used as a pause (" - ", " – ", " — ") outside fixed legal blocks (Formify house rule).
  3. Mentions of AI, assistants, model names, or disclaimer wording. These must never appear in a document.
  4. Filler phrases of generated text (English built in; the master language's list comes from style.json).

From style.json (all optional):
  "anglicisms":      [[regex, "better: ..."], ...]     checked in the master-language column only
  "filler_phrases":  [regex, ...]                       checked in the whole text
  "forbidden":       [regex, ...]                       extra AI/disclaimer patterns for the master language
  "per_document":    {"doc": [[regex, "why"], ...]}     document-specific forbidden wording
  "required_text":   {"doc": [["literal", "message if missing"], ...]}
  "fixed_block_classes": ["legal-fixed", "fixed-form"]  blocks exempt from the dash rule (default shown)

Usage: python3 check_style.py document.html [--doc <document type>] [--style ../references/style.json]
Exit code 0 when there are no warnings, 1 when there are. Warnings show the fragment and, for markers, the line.
Standard library only.
"""
import re, sys, os, json, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_STYLE = os.path.join(HERE, "..", "references", "style.json")

BUILTIN_FILLERS = [
    r"\bit is important to note\b", r"\bplease note\b", r"\bin today's\b", r"\bit is worth (noting|mentioning)\b",
    r"\bin conclusion\b", r"\bfurthermore\b,", r"\bdelve\b",
]
BUILTIN_FORBIDDEN = [
    r"\bartificial intelligence\b", r"\bAI[- ]generated\b", r"\bAI[- ]assisted\b", r"\bAI\b(?=[^A-Za-z])",
    r"\bnot legal advice\b", r"\bdisclaimer\b", r"\bgenerated (by|with)\b.*\b(assistant|model)\b",
    r"\bChatGPT\b", r"\bClaude\b", r"\bFormify is not\b", r"\blegal advis(e|o)r\b",
]


def strip_tags(s):
    return re.sub(r"<[^>]+>", " ", s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("--doc", default="")
    ap.add_argument("--style", default=DEFAULT_STYLE)
    a = ap.parse_args()
    raw = open(a.html, encoding="utf-8").read()
    style = {}
    if os.path.exists(a.style):
        style = json.load(open(a.style, encoding="utf-8"))

    warnings = []

    # 1. Markers
    for m in re.finditer(r"\{\{[^}]*\}\}|\[\[[^\]]*\]\]|\bREQUIRED\b|\bTODO\b|\bXXX\b", raw):
        warnings.append(("unfilled marker", m.group(0), raw[:m.start()].count("\n") + 1))

    # 2. Dashes as a pause, outside fixed blocks
    fixed = style.get("fixed_block_classes", ["legal-fixed", "fixed-form"])
    cls = "|".join(re.escape(c) for c in fixed) or "legal-fixed"
    without_fixed = re.sub(r'<div class="(' + cls + r')[^"]*">.*?</div>\s*(?=<(?:div|h2|h3|table|p)|$)', " ", raw, flags=re.S)
    text = strip_tags(without_fixed)
    # Master column only for anglicisms: drop translated cells, headers and the form-layout translated halves
    master_only = re.sub(r'<td class="tr"[^>]*>.*?</td>', " ", without_fixed, flags=re.S)
    master_only = re.sub(r"<th[^>]*>.*?</th>", " ", master_only, flags=re.S)
    master_only = re.sub(r'<span class="tr-(lbl|val)">.*?</span>', " ", master_only, flags=re.S)
    text_master = strip_tags(master_only)
    for m in re.finditer(r"\s[–—]\s|\s-\s|\w—\w|[.,;:]\s*[–—]", text):
        ctx = text[max(0, m.start() - 40): m.end() + 40].replace("\n", " ")
        warnings.append(("dash used as a pause", ctx.strip(), None))

    # 3. Anglicisms / translation tells (master column)
    for pat, alt in style.get("anglicisms", []):
        for m in re.finditer(pat, text_master, flags=re.I):
            ctx = text_master[max(0, m.start() - 30): m.end() + 30].replace("\n", " ")
            warnings.append((f"anglicism or calque, better: {alt}", ctx.strip(), None))

    # 4. Filler phrases
    for pat in BUILTIN_FILLERS + style.get("filler_phrases", []):
        for m in re.finditer(pat, text, flags=re.I):
            ctx = text[max(0, m.start() - 30): m.end() + 30].replace("\n", " ")
            warnings.append(("filler phrase of generated text", ctx.strip(), None))

    # 5. Per document
    for pat, why in style.get("per_document", {}).get(a.doc, []):
        for m in re.finditer(pat, text, flags=re.I):
            ctx = text[max(0, m.start() - 40): m.end() + 40].replace("\n", " ")
            warnings.append((f"{a.doc}: {why}", ctx.strip(), None))
    for literal, msg in style.get("required_text", {}).get(a.doc, []):
        if literal not in raw:
            warnings.append((f"{a.doc}: {msg}", "", None))

    # 6. AI and disclaimer wording
    for pat in BUILTIN_FORBIDDEN + style.get("forbidden", []):
        for m in re.finditer(pat, text, flags=re.I):
            ctx = text[max(0, m.start() - 30): m.end() + 30].replace("\n", " ")
            warnings.append(("AI mention or disclaimer wording: remove from the document", ctx.strip(), None))

    if not warnings:
        print("OK: no style warnings.")
        sys.exit(0)
    print(f"{len(warnings)} warning(s):")
    for kind, frag, line in warnings:
        loc = f" (line {line})" if line else ""
        print(f"- {kind}{loc}: «{frag}»")
    sys.exit(1)


if __name__ == "__main__":
    main()
