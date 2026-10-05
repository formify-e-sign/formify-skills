<!-- generated from core/references/signatures.md by build_vertical.py; edit the core file, not this copy -->
# Signature areas: Formify's own rules (copied from the formify-pdf-forms skill, September 2026)

How the skeleton applies them: `scripts/render_pdf.py` lays out every signature area exactly as described below. A 0.5 pt rule, a bold 12 pt heading with the party's role, a 9 pt subtitle with the person's name (only to tell two signers of the same role apart; the name, date, IP and source are written by Formify inside the field), then pure white space: 58 pt for the field plus 20 pt of padding for standard signing, and 58 + 15 + 138 + 20 pt when an ID scan box follows. Nothing is drawn where the field goes: no line, no box, no "Signature" label. Two areas sit side by side (219 pt each, 55 pt apart) inside the 493 pt text width; each row moves to the next page only if it does not fit. Coordinates are whole numbers, top-left origin, page index from 0. If a document needs a different placement, edit `render_pdf.py`, never the coordinates by hand. Never guess a placement: this file is the rule.

# Signature Box Design Guide for Formify PDF Forms

This guide covers everything about how signature boxes work in Formify and how to design
PDF forms that accommodate them properly. **This is the most critical design consideration**
when creating PDF forms for Formify.

## Table of Contents

1. [Key Principle](#key-principle)
2. [Signature Box Dimensions](#signature-box-dimensions)
3. [Signature Placement Methods](#signature-placement-methods)
4. [Signing Methods](#signing-methods)
5. [Design Rules for the PDF](#design-rules-for-the-pdf)
6. [What the Signature Box Already Contains](#what-the-signature-box-already-contains)
7. [Correct Heading Pattern](#correct-heading-pattern)
8. [Space Calculation Guide](#space-calculation-guide)
9. [ID Scan Box](#id-scan-box)
10. [Examples](#examples)

---

## Key Principle

**Do NOT create signature boxes in the PDF form.** Signature boxes are added by Formify
*after* the PDF is uploaded — either when creating a template or when sending a document
for signing via the API or Formify UI. Your job when designing the PDF is to **leave
proper space** where signature boxes will be placed later.

---

## Signature Box Dimensions

### Standard signature box (all methods except ID scan)

| Property | Value |
|----------|-------|
| **Width** | 219 points |
| **Height** | 58 points |
| **Scale range** | 0.25 – 1.5 |
| **Default scale** | 1.0 |

At default scale (1.0): **219 × 58 points** (approximately 77 × 20 mm or 3.04 × 0.81 inches)

At maximum scale (1.5): **328.5 × 87 points** (approximately 116 × 31 mm)

### ID scan box (only for `digital_ink_id_scan`)

| Property | Value |
|----------|-------|
| **Width** | 218 points |
| **Height** | 138 points |
| **Scale range** | 0.25 – 1.5 |
| **Default scale** | 1.0 |

At default scale (1.0): **218 × 138 points** (approximately 77 × 49 mm)

---

## Signature Placement Methods

Formify supports two placement methods, chosen when creating the document or template:

### 1. Automatic Placement (`new_page`)

- Adds a new A4 portrait page at the end of the document
- Signature fields are placed automatically on this page
- **Simplest option** — no coordinate planning needed in the PDF
- Not supported for `digital_ink_id_scan` signing method

When using `new_page`, you still benefit from good PDF design (clear headings, logical
structure), but you do NOT need to reserve space for signature boxes within the document
pages themselves.

### 2. Custom Placement (`existing`)

- Signature box is placed at specific coordinates on an existing page
- Requires `signatureBox` properties: `x`, `y`, `page`, and optionally `scale`
- Coordinates are in **PDF points** (1 point = 1/72 inch)
- `x` and `y` specify the top-left corner of the signature box
- `page` is 0-indexed (first page = 0)
- This is where **your PDF design must leave space**

When using `existing` placement, you MUST plan the layout so the signature area is clear
and unobstructed. This is the most common scenario for professional templates.

---

## Signing Methods

The signing method affects what appears in the signature area and how much space is needed:

| Method | Code | Description | Space needed |
|--------|------|-------------|-------------|
| **Digital Ink** | `digital_ink` | Draw signature (SES) | Standard box (219×58) |
| **BankID** | `bankid_identification` | Swedish BankID (AES) | Standard box (219×58) |
| **ID Scan + Ink** | `digital_ink_id_scan` | Scan ID + draw signature | Standard box + ID scan box (218×138) |
| **Face Liveness** | `face_liveness` | ID scan + video selfie | Standard box (219×58) |

For `digital_ink_id_scan`, you need space for BOTH the signature box AND the ID scan box.
Plan accordingly — this requires significantly more vertical space.

---

## Design Rules for the PDF

### Rule 1: White background only

Signature boxes MUST be placed on white (or very light) background. They cannot sit on:
- Colored backgrounds or bands
- Images or graphics
- Patterns or watermarks
- Table cells with background colors

### Rule 2: No overlapping content

The area reserved for the signature box must be completely clear of:
- Text
- Form fields
- Lines or borders
- Other graphical elements

### Rule 3: Sufficient vertical space

Reserve at minimum:
- **100 points** below the heading for a single standard signature box (58pt box + padding)
- **220 points** below the heading if `digital_ink_id_scan` will be used (58pt + 138pt + padding)
- **Additional 20–30 points** between multiple signature boxes if placed vertically

### Rule 4: Heading above, not a drawn box

Place a clear **text heading** above where the signature box will appear. This heading
identifies who should sign there. Do NOT draw a rectangle, border, or placeholder box.

### Rule 5: Do not duplicate signature box information

The signature box already displays certain information automatically (see next section).
Including these as separate form fields in the PDF creates redundancy and confusion.

---

## What the Signature Box Already Contains

When a signee signs a document, the Formify signature box automatically includes:

1. **Full name** — The signee's complete name
2. **Date** — When the signature was applied
3. **IP address** — The signee's IP at time of signing
4. **Source** — How the signing was performed (email link, phone number, etc.)

**Therefore, do NOT add separate form fields for these items near the signature area.**
It would be redundant. The heading above the signature area should only contain:

- The **party identifier** (e.g., "PARTY 1", "PART 2")
- The **role or title** (e.g., "Stakeholder", "CEO", "Customer", "VD")
- The **company name** (if relevant for context)

---

## Correct Heading Pattern

### Simple two-party contract

```
──────────────────────────────
PARTY 1                        ← Heading (bold, 12-14pt)
Authorized signatory           ← Subtitle (optional, 9-10pt)

                               ← White space (≥100pt) for signature box



──────────────────────────────
PARTY 2                        ← Heading
Authorized signatory           ← Subtitle

                               ← White space (≥100pt) for signature box



──────────────────────────────
```

### NDA pattern (as seen in the Formify NDA template)

The NDA template demonstrates the correct approach:

```
PARTY 1
[Company Name] — [Role]

[100+ points of white space for signature box]


PARTY 2
[Company Name] — [Role]

[100+ points of white space for signature box]
```

Key observations from the NDA template:
- Simple, clear headings above each signature area
- No drawn boxes, borders, or placeholder graphics
- Pure white space below each heading
- No duplicate name/date/IP fields

### Multiple signers per party

If a party requires multiple signers:

```
COMPANY ABC — BOARD SIGNATURES

Board Member 1

[white space for signature box]


Board Member 2

[white space for signature box]


Board Member 3

[white space for signature box]
```

---

## Space Calculation Guide

When designing the PDF layout, use these formulas to calculate space needs:

### For `existing` placement with standard signing

```
Space per signer = heading_height + padding + signature_box_height + bottom_margin
                 = ~20pt + 10pt + 58pt + 20pt
                 = ~108pt minimum

Recommended: 120pt per signer
```

### For `existing` placement with ID scan

```
Space per signer = heading_height + padding + signature_box + gap + id_scan_box + bottom_margin
                 = ~20pt + 10pt + 58pt + 15pt + 138pt + 20pt
                 = ~261pt minimum

Recommended: 280pt per signer
```

### Multiple signers on one page

For A4 portrait (842pt height, ~60pt margins top/bottom):
- Usable height: ~722pt
- Subtract page header/section title: ~50pt
- Available for signers: ~672pt

At 120pt per signer: **5 signers per page** (standard signing)
At 280pt per signer: **2 signers per page** (ID scan signing)

If you need more signers than can fit, start a new page for the remaining signatures.

### Coordinates reference (A4 portrait)

| Element | Typical value |
|---------|---------------|
| Page width | 595 points |
| Page height | 842 points |
| Left margin | 50–72 points |
| Right margin | 50–72 points |
| Top margin | 50–72 points |
| Bottom margin | 50–72 points |
| Usable width | ~451–495 points |
| Signature box width | 219 points (at scale 1.0) |

A signature box (219pt wide) fits comfortably within A4 margins with room to spare.

---

## ID Scan Box

When the signing method is `digital_ink_id_scan`, two boxes are required:

1. **signatureBox** — Where the drawn signature appears (219 × 58 points)
2. **idScanBox** — Where the scanned ID image appears (218 × 138 points)

Both must be on the same page and neither can overlap with content or each other.
Typical layout places them vertically:

```
[Heading: Party Name / Role]

[Signature Box — 219 × 58 pt]

[ID Scan Box — 218 × 138 pt]
```

The `signaturePlacement` MUST be `existing` for this signing method — `new_page` is not
supported.

---

## Examples

### Example 1: Simple contract, two parties, `new_page` placement

Since `new_page` auto-generates the signature page, the PDF body just needs good structure.
No special space reservation needed. But you may still want a "Signatures" section heading
at the end of your content for clarity.

### Example 2: Professional template, `existing` placement

For a document where signatures should appear on the last page of content:

```python
# Signature section - leave space for Formify signature boxes
# Party 1 signature area
y_position = 300  # adjust based on content above
c.setFont("Helvetica-Bold", 12)
c.drawString(72, y_position, "PARTY 1 — Company Representative")
# Leave 120pt of white space below (no content until y_position - 120)

# Party 2 signature area
y_position_2 = y_position - 140  # 140pt gap between parties
c.drawString(72, y_position_2, "PARTY 2 — Customer Representative")
# Leave 120pt of white space below
```

### Example 3: KYC form with ID scan

```python
# ID verification and signature section
# Need extra space for ID scan box
y_pos = 400
c.setFont("Helvetica-Bold", 12)
c.drawString(72, y_pos, "IDENTITY VERIFICATION & SIGNATURE")
c.setFont("Helvetica", 9)
c.drawString(72, y_pos - 15, "Verified individual")
# Leave 280pt of white space for signature box + ID scan box
```
