#!/usr/bin/env python3
"""Step 0 of every run: prints the welcome lines, checks the companion skills and reports the platform.
Standard library only. Run it from anywhere:  python3 scripts/start.py
Output is plain text; show the WELCOME block to the user verbatim (translated into the user's language
if they write another one, document names kept in Spanish), then continue with the skill."""
import glob
import os
import platform
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                       # the skill folder
COMPANIONS = ("formify-send-contract", "formify-verify-identity", "formify-pdf-forms", "formify-track-signatures", "formify-share-link")


def welcome():
    p = os.path.join(ROOT, "assets", "welcome.txt")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return f.read().strip()
    return "(assets/welcome.txt is missing: say what this skill produces and ask which document is needed)"


def companions():
    found, missing = [], []
    parents, up = set(), ROOT
    for _ in range(3):                                 # the skill's own folder tree, three levels up
        up = os.path.dirname(up)
        parents.add(up)
    for env in ("CLAUDE_PLUGIN_ROOT", "CODEX_HOME"):
        v = os.environ.get(env)
        if v:
            parents.add(v)
    home = os.path.expanduser("~")
    for rel in (".claude/skills", ".agents/skills", ".codex/skills", ".manus/skills", "skills"):
        parents.add(os.path.join(home, rel))
    for name in COMPANIONS:
        hit = None
        for parent in parents:
            for cand in glob.glob(os.path.join(parent, "**", name, "SKILL.md"), recursive=True)[:1]:
                hit = cand
        (found if hit else missing).append(name)
    return found, missing


def renderer():
    try:
        sys.path.insert(0, HERE)
        from render_pdf import find_chromium  # type: ignore
        ch = find_chromium()
    except Exception:
        ch = None
    weasy = False
    try:
        import weasyprint  # type: ignore  # noqa: F401
        weasy = True
    except Exception:
        pass
    wk = shutil.which("wkhtmltopdf")
    if ch:
        return "browser found: " + ch
    if weasy:
        return "WeasyPrint present (no browser found)"
    if wk:
        return "wkhtmltopdf present (no browser found)"
    return "no renderer found: PDF will not be rendered here; route 1 or 3 of the skill applies"


def main():
    print("WELCOME (show these lines to the user first, every run):")
    print(welcome())
    print()
    found, missing = companions()
    print("COMPANION SKILLS: found %s; missing %s" % (", ".join(found) or "none", ", ".join(missing) or "none"))
    if missing:
        print("  Tell the user which companions are missing and that they come from the same Formify package; continue without them.")
    print("PLATFORM: %s %s, Python %s, %s" % (platform.system(), platform.release(), platform.python_version(), renderer()))
    mem = os.path.join(os.getcwd(), "formify-memory.md")
    print("MEMORY: %s" % ("formify-memory.md found in the working folder (read it, never ask for what it holds)" if os.path.exists(mem)
                         else "no formify-memory.md in the working folder: first run, offer the sample pack and the memory"))


if __name__ == "__main__":
    main()
