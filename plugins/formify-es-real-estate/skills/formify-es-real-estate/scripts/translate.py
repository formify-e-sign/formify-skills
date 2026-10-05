#!/usr/bin/env python3
"""
translate.py: extracts from an HTML document everything that must be translated when the client's language
is not the one the template's second column was written in, and puts the translations back. It avoids the
easiest mistake to make by hand: breaking the nested tables of the right-hand column.

Step 1 (extract):   python3 translate.py extract body.html cells.json
   Writes cells.json with one entry per translated-column cell (<td class="tr">, with its complete inner
   HTML, nested tables included) and one per bilingual label (h1/h2/h3 headings, <th> headers,
   <td class="k"> labels and notes of the form "Master / Second"), plus the half-labels of the form layout
   (<span class="tr-lbl">/ Second label</span> and <span class="tr-val">/ second value</span>).
Step 2 (translate): edit the "text" field of every entry. In cells keep the HTML tags (<span class="num">,
   <table class="data">, <p>, <b>, <span class="checkbox">) and translate only the text. In bilingual labels
   keep the master-language half and replace the second half: "Qué / Vad".
Step 3 (insert):    python3 translate.py insert body.html cells.json body.html [--strict]
   Replaces every fragment with its translation and warns about every entry left untranslated
   (identical to the original) except those you mark with "same": true. The warning never stops a
   command chain: exit code 0 unless --strict is given, then 1.
Standard library only.
"""
import json, re, sys

STRICT = "--strict" in sys.argv
sys.argv = [a for a in sys.argv if a != "--strict"]


def tr_cells(s):
    """Returns [(inner_start, inner_end)] of every <td class="tr"...>...</td>, nesting aware."""
    out = []
    for m in re.finditer(r'<td class="tr"[^>]*>', s):
        i = m.end(); depth = 1; j = i
        while depth and j < len(s):
            nxt_open = re.compile(r'<td\b').search(s, j)
            nxt_close = s.find('</td>', j)
            if nxt_close == -1:
                break
            if nxt_open and nxt_open.start() < nxt_close:
                depth += 1; j = nxt_open.end()
            else:
                depth -= 1
                if depth == 0:
                    out.append((i, nxt_close)); break
                j = nxt_close + 5
    return out


def labels(s):
    """Elements whose text is bilingual 'Master / Second' outside the tr cells, and the translated halves of the
    form layout (<span class="tr-lbl">, <span class="tr-val">)."""
    out = []
    # The closing tag must match the opening element (h1, td, span...), not the first one that appears.
    pat = re.compile(r'<(?P<tag>h1|h2|h3|th|div|td|span)(?P<attr> class="title"| class="note"| class="k"| class="tr-lbl"| class="tr-val"|)(?=[\s>])[^>]*>(?P<inner>.*?)</(?P=tag)>', re.S)
    allowed = ('h1', 'h2', 'h3', 'th', 'div class="title"', 'div class="note"', 'td class="k"', 'span class="tr-lbl"', 'span class="tr-val"')
    tr_ranges = tr_cells(s)
    pos = 0
    while True:
        m = pat.search(s, pos)
        if not m:
            break
        pos = m.start() + 1  # keep searching inside the element even if this one is not extracted
        kind = m.group('tag') + m.group('attr')
        if kind not in allowed:
            continue
        inner = m.group('inner')
        is_span = m.group('tag') == 'span'
        if ' / ' not in inner and m.group('tag') != 'th' and not is_span:
            continue
        if any(a <= m.start() < b for a, b in tr_ranges):
            continue  # already inside a translated cell
        if any(a <= m.start() < b for a, b in out):
            continue  # already inside another extracted label
        out.append((m.start('inner'), m.end('inner')))
    return out


def extract(html_path, json_path):
    s = open(html_path, encoding='utf-8').read()
    entries = []
    for a, b in tr_cells(s):
        entries.append({"type": "cell", "start": a, "end": b, "original": s[a:b], "text": s[a:b]})
    for a, b in labels(s):
        entries.append({"type": "label", "start": a, "end": b, "original": s[a:b], "text": s[a:b]})
    entries.sort(key=lambda e: e["start"])
    for n, e in enumerate(entries):
        e["id"] = n
    json.dump(entries, open(json_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"{len(entries)} fragments in {json_path} ({sum(1 for e in entries if e['type']=='cell')} cells, {sum(1 for e in entries if e['type']=='label')} labels)")


def insert(html_path, json_path, out_path):
    s = open(html_path, encoding='utf-8').read()
    entries = json.load(open(json_path, encoding='utf-8'))
    untranslated = [e["id"] for e in entries if e["text"] == e["original"] and not e.get("same")]
    if untranslated:
        print(f"WARNING: {len(untranslated)} fragments not translated (ids {untranslated[:12]}{'...' if len(untranslated) > 12 else ''}). Mark \"same\": true if they must stay as they are.")
    for e in sorted(entries, key=lambda e: e["start"], reverse=True):
        if s[e["start"]:e["end"]] != e["original"]:
            sys.exit(f"The HTML changed since extraction (fragment {e['id']}). Extract again.")
        s = s[:e["start"]] + e["text"] + s[e["end"]:]
    open(out_path, 'w', encoding='utf-8').write(s)
    # structure check: same number of <td and </td>, <table and </table>, <tr and </tr>
    for tag in ("td", "table", "tr"):
        o = len(re.findall(rf"<{tag}\b", s)); c = s.count(f"</{tag}>")
        if o != c:
            sys.exit(f"Broken structure: {o} <{tag}> against {c} </{tag}>. Check the cells with nested tables.")
    print(f"OK: {out_path}")
    if untranslated and STRICT:
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "extract":
        extract(sys.argv[2], sys.argv[3])
    elif len(sys.argv) >= 5 and sys.argv[1] == "insert":
        insert(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print(__doc__); sys.exit(2)
