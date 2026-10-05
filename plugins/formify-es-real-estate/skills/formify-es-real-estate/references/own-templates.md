<!-- generated from core/references/own-templates.md by build_vertical.py; edit the core file, not this copy -->
# Own templates: the user's adjustments survive

The skill's templates in `assets/templates/` are never edited. When a user changes something in a document type for good (a wording, a clause added or removed, a row taken out of a box, a different default), the change lives in the user's own copy of that template, in the working folder:

```
<working folder>/
  formify-memory.md
  my-templates/
    03_reservation.html       the user's version; same file name as in assets/templates/
    01_mandate.html
```

`fill.py` looks in `my-templates/` first (option `--own`, default `my-templates`); if a file with the template's name is there, it is used and the script prints "Own template: ... (base vX.Y.Z)". The folder is outside the skill, so a new skill version does not touch it.

## When the user asks for a change

Two kinds of change, and the difference matters:

- **For this document only** ("in this one, take out clause 7"): edit `body.html` after `fill.py`, render, done. Nothing is saved.
- **For every document of this type from now on** ("we never use the mediation sentence", "add a clause about the alarm company", "our key receipts always list the parking remote"): ask once, "Shall I keep this for all your <document type> from now on?" On yes, create or update the own template:
  1. If `my-templates/<file>` does not exist, copy `assets/templates/<file>` there and put this as the first line: `<!-- OWN: base <file> v<skill version from SKILL.md> · <date> -->`.
  2. Apply the change to the own copy, in both columns (master language and, in bilingual segments, the second-language column), keeping the template mechanics untouched: `{{fields}}`, `<!-- OPTIONAL -->` and `<!-- VARIANT -->` blocks, `<!-- SIGNATURES -->`, the `pdf-field` spans with their `FIELDMARK` markers, the `tr-lbl` / `tr-val` spans and the class names. A new clause goes in as a new numbered row of the clauses table, in both columns; a removed clause means renumbering the rows that follow and any reference to them in the text.
  3. Run `check_style.py` on a document built from the own copy before showing it.
  4. Note it in the memory file: `own_template=yes` on that document type's line, and one short line in `notices` saying what was changed (so the next session can tell the user what their version differs in, without reading the HTML).

The user's own clause text is theirs: never rewrite it into the template style, only check it with the style checker and mention a warning once.

## When the skill is updated

`fill.py` prints the base version stored in the own copy. If it is older than the version in `SKILL.md`, say once per session, in one line: "Your own <document type> template is based on an older version of the skill's template; do you want me to carry your changes over to the new one?" On yes: copy the new base to a temporary file, re-apply the user's changes (the `notices` line says what they were; when in doubt, show the user the two versions of the changed clause), replace the own copy, update the OWN line. On no: keep using the own copy; do not ask again in that session.

## Settings

Under "Settings" the user can see which document types have an own template and what was changed, and can reset one to the skill's version (move the own copy to `my-templates/_previous/<file>.<date>` rather than deleting it).
