# The hand-over: document plus field specification

Step 5, rung 5 — used when nothing here can write a PDF: no library from the closed list, no
Python. It is also the companion to every PDF built on rung 3 or 4, so the recipient can check
what was built. It has one shape. Do not improvise another: the fixed shape is what lets a
colleague, a different assistant or Formify's own tooling finish the document without asking
a single question.

## Shape

Four parts, in this order, in one message — or, where files exist, one file named
`<document>-spec.md`.

### 1. The document text

The complete text, in the document's language, exactly as it should appear on the page:
headings, numbered clauses, party blocks. Where a field sits inside a sentence, put the
field's name in double braces at that spot: `The tenant, {{tenant_name}}, agrees…`. Nothing
else in the text is a placeholder — no `[insert here]`, no blanks, no underscore runs.

### 2. The field table

One row per field, every column filled. `-` means "none", never "unknown".

| # | name | label | kind | required | options | read-only | page | anchor | size |
|---|---|---|---|---|---|---|---|---|---|

- **name** — the exact AcroForm field name, unique in the document, carrying any `tink-*`
  attributes with their brackets: `buyer_id|tink-scan-id[1]`. Never a display name.
- **label** — what the person sees beside the field, in the document's language.
- **kind** — `text`, `multiline`, `checkbox`, `radio`, `dropdown`, `image`, `upload`.
- **required** — `yes` / `no`.
- **options** — for `radio` and `dropdown`: the values, separated by `;`, no `/` inside any.
- **read-only** — `yes` for every trigger and every auto-filled field, `no` otherwise.
- **page** — 1-based.
- **anchor** — the sentence or label the field sits beside, quoted verbatim, so coordinates
  can be found by searching the text rather than guessed.
- **size** — width × height in points for `image` and `upload` fields, because a captured
  image is stretched to the rectangle exactly. `-` for every other kind.

### 3. Signature areas

One line per signer: caption, page, and the paragraph after which the empty space is
reserved. No box, no line, no widget — the space is empty by rule (step 6) and the caption is
the only ink. Reserve at least 58 points of height per signature; Formify's field is 219 × 58
at full size. Add an ID-scan placeholder of 218 × 138 points beside it only when the signing
method needs one (`references/signature-space.md`).

### 4. What remains

One sentence naming the single step that turns this into a PDF, and where it can happen:
*"Open this in an assistant with a PDF library — Claude Desktop has one — and ask for the PDF;
every field above is already decided."*

## Example fragment

```markdown
## 1. Text
### Deposit receipt
The seller, {{seller_name}}, acknowledges receipt of {{amount}} EUR from the buyer,
{{buyer_name}}, on {{date}}, as deposit under the reservation agreement for the property
at {{property_address}}. …

## 2. Fields
| # | name | label | kind | required | options | read-only | page | anchor | size |
|---|---|---|---|---|---|---|---|---|---|
| 1 | seller_name | Seller | text | yes | - | no | 1 | "The seller," | - |
| 2 | amount | Amount (EUR) | text | yes | - | no | 1 | "receipt of" | - |
| 3 | buyer_name | Buyer | text | yes | - | no | 1 | "from the buyer," | - |
| 4 | buyer_id\|tink-scan-id[1] | Buyer ID | image | yes | - | yes | 1 | "Buyer ID" | 180 × 120 |
| 5 | date | Date | text | yes | - | no | 1 | "on" | - |
| 6 | property_address | Property | text | yes | - | no | 1 | "the property at" | - |

## 3. Signatures
- Seller — page 1, after the closing paragraph
- Buyer — page 1, after the closing paragraph, ID-scan placeholder beside it

## 4. What remains
Ask any assistant with a PDF library for the PDF; every field is decided above.
```

## What the hand-over is not

- Not a summary. Every attribute is written out, because the recipient cannot see this
  conversation.
- Not an apology. Never "I could not make a PDF". Say which rung produced this and why the
  next one was out of reach: *"No PDF library and no Python here, so this is the complete
  specification. In Claude Desktop the same request produces the PDF directly."*
