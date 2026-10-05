#!/usr/bin/env python3
"""
fill.py: fills an HTML template from a JSON data file.

  python3 fill.py --template ../assets/templates/03_reservation.html --data data.json --out body.html
                  [--optional financing,viewing_log] [--variant CCCat] [--own my-templates]

- Replaces every {{field}} with data[field]. Missing fields are left as {{field}}, listed at the end, and the
  script exits 1 without touching an existing output file.
- Values are HTML-escaped. Two exceptions: keys ending in "_html" (only an inline PNG/JPEG data-URI <img> is
  accepted, for the logo) and the tag <br> (kept, so an address or a register line can break lines).
- Blocks <!-- OPTIONAL: name --> ... <!-- /OPTIONAL --> are kept only if "name" is in --optional (or in
  data["optional"]); an optional name the template does not have is an error, not a silent no-op.
- Variants: <!-- VARIANT X --> ... <!-- /VARIANT X --> is active by default; a commented variant
  <!-- VARIANT Y: ... --> is activated with --variant Y. An unknown variant is an error.
- Fields with the _tr suffix (translated column) that are missing fall back to the value without the suffix
  (names, figures, dates); prose must be translated explicitly. Single-language segments never use _tr.
- Form field: a value {"field": "pdf_name", "width": 160, "attributes": "tink-...", "height": 120,
  "read_only": true, "required": false} inserts a blank that render_pdf.py turns into a PDF form field
  (AcroForm) the signer fills in Formify. "width"/"height" in pt (default 160 x 13). Templates may also carry
  fixed <span class="pdf-field"> blanks (ID-scan pattern, references/id-scan.md); all markers are numbered here.
- Own templates: if --own (default "my-templates") holds a file with the template's name, that copy is used
  (references/own-templates.md) and its base version is printed.
Standard library only.
"""
import argparse, base64, html, json, os, re, sys, tempfile


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--optional", default="")
    ap.add_argument("--variant", default="")
    ap.add_argument("--own", default="my-templates",
                    help="folder with the user's own copies of templates; a file with the same name wins (empty = ignore)")
    a = ap.parse_args()

    if a.own:
        own = os.path.join(a.own, os.path.basename(a.template))
        if os.path.exists(own):
            head = open(own, encoding="utf-8").read(300)
            m = re.search(r"OWN:\s*base\s+\S+\s+(v[\d.]+)", head)
            print("Own template: %s (base %s)" % (own, m.group(1) if m else "no version"))
            a.template = own

    data = json.load(open(a.data, encoding="utf-8"))
    tpl = open(a.template, encoding="utf-8").read()
    opt = set(x.strip() for x in a.optional.split(",") if x.strip()) | set(data.get("optional", []))
    variant = a.variant or data.get("variant", "")

    available_variants = set(re.findall(r"<!--\s*VARIANT ([\w-]+)", tpl))
    available_options = set(re.findall(r"<!--\s*OPTIONAL:\s*([\w-]+)", tpl))
    if variant and variant not in available_variants:
        sys.exit("Unknown variant: " + variant)
    if opt - available_options:
        sys.exit("Unknown optional blocks: " + ", ".join(sorted(opt - available_options)))

    # Drop the template's leading comments (its header, and the OWN line of a user's copy)
    while re.match(r"\s*<!--", tpl):
        tpl = re.sub(r"^\s*<!--.*?-->\s*", "", tpl, count=1, flags=re.S)

    # Variants
    if variant:
        tpl = re.sub(r"<!--\s*VARIANT " + re.escape(variant) + r"\b([^\n]*)\n(.*?)\n\s*-->", lambda m: m.group(2), tpl, flags=re.S)
        tpl = re.sub(r"<!--\s*VARIANT (?!" + re.escape(variant) + r"\b)([\w-]+)[^>]*-->.*?<!--\s*/VARIANT \1\s*-->", "", tpl, flags=re.S)
    else:
        tpl = re.sub(r"<!--\s*VARIANT [\w-]+[^\n>]*:[^\n]*\n.*?\n\s*-->", "", tpl, flags=re.S)
        tpl = re.sub(r"<!--\s*VARIANT [\w-]+[^>]*-->", "", tpl)
        tpl = re.sub(r"<!--\s*/VARIANT [\w-]+\s*-->", "", tpl)

    # Optional blocks
    tpl = re.sub(r"<!--\s*OPTIONAL:\s*([\w-]+)\s*-->(.*?)<!--\s*/OPTIONAL\s*-->",
                 lambda m: m.group(2) if m.group(1).strip() in opt else "", tpl, flags=re.S)

    # Fields
    missing = set()
    counter = [0]

    def blank(v):
        name = v.get("field") or "field%d" % counter[0]
        if v.get("attributes"):
            name = name + "|" + v["attributes"]
        width = int(v.get("width", 160))
        counter[0] += 1
        extra, style, cls = "", "width:%dpt" % width, "pdf-field"
        if v.get("height"):
            extra += ' data-height="%d"' % int(v["height"])
            style = "width:%dpt !important;height:%dpt !important" % (width, int(v["height"]))
            cls += " image"
        if v.get("read_only"):
            extra += ' data-readonly="1"'
        if v.get("required") is False:
            extra += ' data-required="0"'
        return ('<span class="%s" data-name="%s" data-width="%d"%s style="%s"><span class="field-mark">FIELDMARK</span><span class="field-end">FIELDEND</span></span>'
                % (cls, html.escape(name, quote=True), width, extra, style))

    def text(k, value):
        if k.endswith("_html"):
            if not value:
                return ""
            m = re.fullmatch(r'<img src="data:image/(png|jpeg);base64,([A-Za-z0-9+/=]+)"[^<>]*/?>', str(value))
            if not m:
                raise ValueError(k + " must be an inline PNG/JPEG image only")
            raw = base64.b64decode(m.group(2), validate=True)
            ok = raw.startswith(b"\x89PNG\r\n\x1a\n") if m.group(1) == "png" else raw.startswith(b"\xff\xd8")
            if not ok:
                raise ValueError(k + ": image content does not match its type")
            return str(value)
        if not isinstance(value, (str, int, float, bool)):
            raise ValueError("Unsupported value type for " + k)
        s = html.escape(str(value), quote=False)
        return re.sub(r"&lt;br\s*/?&gt;", "<br>", s)

    def field(m):
        k = m.group(1).strip()
        if k in data and isinstance(data[k], dict) and "field" in data[k]:
            return blank(data[k])
        if k in data and data[k] is not None:
            return text(k, data[k])
        if k.endswith("_tr") and k[:-3] in data and data[k[:-3]] is not None:
            v = data[k[:-3]]
            return blank(v) if isinstance(v, dict) and "field" in v else text(k, v)
        missing.add(k)
        return m.group(0)
    out = re.sub(r"\{\{\s*([\w\.]+)\s*\}\}", field, tpl)

    # Number every field marker in document order (template-fixed and data-driven alike)
    num = [0]
    def number(m):
        num[0] += 1
        return "FIELDMARK%d" % (num[0] - 1)
    out = re.sub(r"FIELDMARK\d*", number, out)
    num[0] = 0
    def number_end(m):
        num[0] += 1
        return "FIELDEND%d" % (num[0] - 1)
    out = re.sub(r"FIELDEND\d*", number_end, out)
    # A translated value that is a field leaves a lone slash: remove it
    out = re.sub(r'\s*<span class="tr-val">/\s*</span>', "", out)

    if missing:
        print("Unfilled fields: " + ", ".join(sorted(missing)))
        sys.exit(1)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(os.path.abspath(a.out)) or ".", prefix=".fill-")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(out)
    os.replace(tmp, a.out)
    print(f"OK: {a.out}")


if __name__ == "__main__":
    main()
