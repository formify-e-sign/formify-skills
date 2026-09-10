# Placing a signature on an existing page

Open this when the signature goes somewhere other than a new page at the end of the
document.

## The coordinate system

- Origin is the **top-left corner** of the page.
- `x` increases to the right, `y` increases **downward**.
- `(x, y)` is always the **top-left corner of the field**, never its centre.
- Everything is in PDF points. 1 point = 1/72 inch.
- **Pages are numbered from zero.** The first page is `0`.

## Field sizes at scale 1.0

| Field | Width | Height |
|---|---|---|
| Signature | **219 pt** | **58 pt** |
| ID scan placeholder | **218 pt** | **138 pt** |

Scale accepts 0.25 to 1.5. The **top-left corner stays fixed** — only the right and bottom
edges move. Effective size is the base size multiplied by the scale.

## Page sizes — check, never assume

| Page | Points |
|---|---|
| A4 (210 × 297 mm) | 595 × 842 |
| US Letter (8.5 × 11 in) | 612 × 792 |

Conversion from millimetres: `pt = mm × 72 / 25.4`.

## Worked placements

**Signature, bottom-right of A4:**
`x = 595 − 219 = 376`, `y = 842 − 58 = 784`, `page = 0`

**Signature, bottom-right of US Letter:**
`x = 612 − 219 = 393`, `y = 792 − 58 = 734`, `page = 0`

**ID scan box, bottom-right of A4:**
`x = 595 − 218 = 377`, `y = 842 − 138 = 704`, `page = 0`

**ID scan box, bottom-right of US Letter:**
`x = 612 − 218 = 394`, `y = 792 − 138 = 654`, `page = 0`

## Coordinates must be whole numbers

The schema accepts a decimal. The backend does not use it: a fractional value is discarded
rather than rounded, and `74.7` is stored as `0`. The field then sits in the top-left corner
of the page and the document sends anyway.

Round every coordinate to an integer before sending. This is the single most damaging
placement mistake, because nothing reports it.

## ID-scan signing needs both boxes

`digital_ink_id_scan` requires a signature box **and** an ID scan box. Configuring only the
signature box fails at send time.

The two must not overlap. Stacked in the bottom-right corner of A4, ID scan above the
signature with a small gap:

```
ID scan   x = 377, y = 690        (218 × 138)
Signature x = 376, y = 784        (219 × 58)
```

That needs roughly **220 points of clear vertical space**: 138 + 58 plus separation. Plan
for it when the document is designed, not when it is sent.

## Overlap is not detected

Formify does not check whether two fields collide, and a field is **fully opaque** —
whatever sits behind it is hidden in the signed document. Nothing warns you, at any stage.

Two rules follow:

1. No two fields may share a page and overlap.
2. Never place a field over text the signer needs to read.

Where space is short, reduce the scale rather than moving the field onto content.

## Several signers on one page

Each signer needs their own box. Stack them down the page, ordered as the signature block
reads, with clear separation:

```
Signer 1   x = 60,  y = 640
Signer 2   x = 60,  y = 720
Signer 3   x = 60,  y = 800
```

An 80-point step leaves 22 points of gap between 58-point fields. If any signer uses ID
scan, that signer needs about 220 points to themselves and the others move down.

When there is not enough room on the existing page, use a new page at the end instead. It is
always the safer choice, and it is the default for a reason.

## When a template already places the signature

A template carries its own pre-configured signature position. Do not send coordinates unless
the user explicitly wants to override it — an override with a wrong page size is worse than
the template's own placement.

## Drafts validate late

Coordinates are optional while a draft is being saved and fully validated only when the
draft is sent. A draft that saves cleanly can still fail at send. Preview the rendered PDF
before sending: fields without valid coordinates do not appear in the preview but remain in
the draft data, so a missing field in the preview is a real signal.
