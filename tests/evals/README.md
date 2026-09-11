# Output-quality evals

Seventeen cases, seventy-two assertions, five skills. These measure **what a skill produces**.
`tests/release/` measures **which skill fires and which tool it calls**. Neither replaces the
other, and the distinction matters when reading a result: a skill can route perfectly and
still write a bad document.

## Why the cases are shaped this way

Every assertion is written so a **baseline run without the skill can fail it**. That is the
only thing an eval measures — the delta. An assertion the model satisfies unprompted inflates
the with-skill pass rate and says nothing, and the eval guidance calls for removing those once
the first run shows which they are.

The clearest example is `formify-pdf-forms` case 1. Asked for a form with a signature, a model
with no skill draws a line or places a widget, because that is what a signature looks like on
paper. Formify paints its signing overlay in that zone and a widget collides with it, so the
correct output is *labelled empty space*. Three assertions test exactly that, and the baseline
should fail all three.

The same logic picked the rest: the ID scan that must place **two** boxes rather than one, the
identity capture that stores no image, the assurance ranking that must **not** be produced, the
reminder that must exclude anyone who already signed, and the expired link that must be
attributed to the ten-minute window rather than to single use.

## Placement, deliberately not the documented one

The convention is `evals/evals.json` inside the skill directory. These live here instead,
because `package.json` publishes `skills/` wholesale — an `evals/` folder inside a skill would
install into every user's agent directory and ship in the npm tarball. Copy the relevant file
into the skill directory when running a tool that expects the convention, and remove it
afterwards.

## Running them

`skill-creator` from the official marketplace automates the loop — a subagent per case, a
with-skill and a without-skill arm, assertion grading with evidence, and a `benchmark.json`
carrying the pass-rate, time and token delta:

```sh
/plugin marketplace add anthropics/claude-plugins-official
/plugin install skill-creator@claude-plugins-official
```

`claude plugin eval` covers the same ground natively with `--ablation with-without`, and is
the better tool once it is out of early access.

## What a result does and does not establish

Assertions are graded against outputs, and a PASS needs quoted evidence rather than the
benefit of the doubt. A section titled "Summary" holding one vague sentence fails an assertion
asking for a summary.

None of this touches the live Formify service. No case sends a document, and none should be
rewritten to — an invitation is a real, unrecallable email.
