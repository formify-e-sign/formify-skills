<!-- generated from core/references/formify.md by build_vertical.py; edit the core file, not this copy -->
# Formify: upload, draft, preview, send, archive

Read this when the document PDF and its `<title>.signatures.json` exist and the user has approved the draft text. The steps use the Formify MCP tools by name (server version 1.3.0 or later); they work in any client that has the Formify MCP server connected (Claude, ChatGPT, Manus, Codex and others). Every step is a plain tool call plus, where noted, one shell command. Formify templates and public links have their own file, `references/templates-links.md`.

## 0. Do you have the tools?
Check whether tools named `get_account_capabilities`, `upload_file`, `create_draft`, `get_draft_file_url` and `send_draft` (prefixed by the server name, for example `mcp__Formify__create_draft`) exist in your tool list. If they do not: deliver the PDF and `signatures.json` to the user and say, in one sentence, that the document is ready to upload in Formify and that connecting the Formify MCP server lets you send it directly next time. Do not invent REST calls. Stop here.

## 1. Silent capability check
Call `get_account_capabilities` once per session. Note the flags you will need: `signingOrder`, `signatureIdScan`, `signatureFaceLiveness`, `signatureBankId`, `deliverySms`, `deliveryWhatsapp`, `aiAssistant`, `initials`, `templates`, `templatesCreate`, `publicLinks`, `publicLinksCreate`. Never list the flags to the user; use them to decide what to offer. If a document guide asks for an ID scan and `signatureIdScan` is off, fall back to `digital_ink` and tell the user in one sentence.

## 2. Upload the PDF
`upload_file` takes exactly one of four inputs. Which one works depends on the client, not on the file. Choose in this order and stop at the first the client can handle; say in the chat which path you used only if the user asks or if a path failed.

1. **`fileReference`**: the host passes attached files to tools as file references (ChatGPT does: an object with `download_url`, `file_id` and sometimes `mime_type`, `file_name`). Pass it exactly as the host provides it; the server downloads the file itself. Never build the reference yourself and never use a `sandbox:` path: the server accepts https addresses only. If the call arrives without a reference although the file is attached, retry once, then ask the user to attach the PDF to the conversation and try again. The same file sent twice returns the same `fileId` with a `note`; that is not an error.
2. **`url`**: the PDF sits at an https address the server can reach (you published it somewhere the user controls). Works in every client.
3. **`uploadId`**: you can run shell commands and the shell has outbound network access (Claude with code execution, Manus, Codex with `network_access` on). `request_file_upload_url(fileName="<title>.pdf")` returns `uploadId`, `uploadUrl`, `expiresAt` and a ready `curlCommand`. Run it from the directory that holds the PDF, replacing `<path-to-file>`, adding `--fail-with-body --write-out '%{http_code}\n'` at the end so the status is printed; wait for HTTP 200 and `status: "staged"`. Then `upload_file(uploadId=<id>)` and keep the returned `fileId`.
4. **`file` + `fileName`**: none of the above is possible (a sandbox without network, as in the ChatGPT web container when no reference arrives, or Codex without network access). The whole file as base64. Only for files up to roughly 50 kB, only when the complete content is available to you unchanged, never typed by hand. Our documents are usually 15 to 60 kB; above that, ask the user for an https address or attach the file in a client that passes references.

Rules for the staged path (3):
- One at a time. Only one staged upload can be pending per user. Finish curl and `upload_file` for one file before requesting the next address, also for files that will be merged.
- Ten minutes. The address expires ten minutes after the request.
- The entry is consumed when `upload_file` reads it. If Formify rejects the file (for example a password-protected PDF: "Document could not be opened"), the entry is gone: fix the file and start again from `request_file_upload_url`. Never call `upload_file` twice with the same `uploadId`.
- If you request an address while another is pending, the server refuses with `pendingUpload` and a `nextStep` text. That is expected: follow `nextStep`; do not switch to base64.
- PUT answers: 200 staged, call `upload_file`; 404 expired, consumed or never issued, request a new address; 409 already uploaded to this address, call `upload_file` and do not run curl again; 401 signature wrong or expired, request a new address, never edit it; 413 or 415 too large or not a PDF, fix the file; 429 more than 20 PUTs a minute, wait a minute.
- If curl fails with a network, DNS or "host not in allowlist" error, the sandbox blocks outbound requests to the Formify MCP host (`mcp.formify.eu`, or the host in the `uploadUrl`). Do not rerun the command. In Claude, tell the user to allow it under Settings, Capabilities, Code execution, Domain allowlist (all domains), wait for "done", and start again from `request_file_upload_url`; in other clients use path 4. Never run the same path over and over: say which path failed and why, then switch.

After the upload, `get_file_fields(fileId)` when the document carries form fields (every document with `form_fields` in its `signatures.json`; the identification forms always do). It returns the fields by name; compare with the names in `signatures.json` and stop if one is missing. Formify sets `required: false` on every field regardless of the PDF flag (tested September 2026); that is expected.

## 3. Create the draft
Call `create_draft` with:
- `fileId`, `name` = the draft title from the document guide (human readable, no ".pdf"), `sharingSetting` = "shared" unless the user prefers private.
- `language` = the invitation language. Only `en`, `sv` and `es` exist today. If the client's language is another (Dutch, German, French...), say so in one sentence and pick `en` unless the user prefers `es`; the document itself is bilingual, only the invitation e-mail is limited.
- `personalMessage` (max 500 characters) = the invitation text from the guide, in the client's language when possible.
- `enableSigningOrder` = true when the guide prescribes an order and the capability exists.
- `fields` = the values the organisation pre-fills (never the other party's), with `fieldsReadonlyMode: "filled"`; field names exactly as `get_file_fields` returned them. Never write into a field whose name carries a `tink-*` attribute other than a format check: those are filled by Formify during signing.
- `signeeDetails[]`: for every entry in `<title>.signatures.json`: `fullName`, `emailAddress` (mandatory; ask if missing), `phoneNumber` only if given (with `phoneNumberDeliveryMethod` sms or whatsapp), `signingOrder` per the guide, `signaturePlacement` = "existing", `signatureBox` copied verbatim from `signatures.json` (x, y, page, scale), `idScanBox` copied verbatim when present, `signatureType` = "face_liveness" for the client on an identification (KYC) form, preselected without asking (fall back to "digital_ink" and say so in one sentence only when `signatureFaceLiveness` is off); for other documents "digital_ink_id_scan" when an `idScanBox` exists and the capability is on, "face_liveness" when the user asked for it and it is available, otherwise "digital_ink".
Keep the returned `draftId`. Tested September 2026: neither `create_draft` nor `get_draft` returns a link to the draft in the Formify app; the app link (`documentUrl`) only exists after `send_draft`. `get_draft` returns the signers, the boxes, sharing and language but not the pre-filled field values: the preview (step 4) is the only place to check them.

## 4. Preview: always, with the signature fields drawn
1. Before the first preview of the session, tell the user in two lines that the preview is downloaded from Formify and that the sandbox must be allowed to reach Formify's document host (`docs-api.formify.se` or `docs-api.formify.eu`; the download URL shows which).
2. `get_draft_file_url(draftId)` returns a one-time `downloadUrl` valid ten minutes, as plain JSON text. Download it with your shell (`curl -fsSL -o "<title>-formify-preview.pdf" "<url>"`). Check the file starts with `%PDF` and is larger than 1 KB. Never show the raw download URL. Never call `get_draft_file`. Without a shell, hand the user the URL as a clickable link and say it opens once and expires in ten minutes.
3. Show the downloaded file to the user with your file-presentation tool, with link text that says the file opens inside this chat ("Open preview here"). This is the Formify-rendered PDF with the signature and ID fields drawn and the pre-filled values printed; it is the only file the user should see at this step, never the source PDF.
4. Next to the preview, say that the draft is saved in Formify under its title (there is no app link until it is sent). Do not show any docs-api link.
5. Ask one question with five options: send now; save as draft and do not send; change the signers; move a signature field; change the document text. If the user already chose one of these in the request ("save it as a draft, do not send"), that is the answer: say in one line that the draft is saved under its title on account <accountName from get_current_user>, and do not ask again.
   - Send now: go to step 5.
   - Save as draft: say the draft is saved in Formify under its title, and stop.
   - Change signers: ask what changes, `update_draft` with the complete configuration, then repeat step 4 from 2.
   - Move a field: the fields sit on the fixed signature page; if the user wants them elsewhere, re-run `render_pdf.py` with a different layout or edit `signatures.json`, upload the new PDF (step 2), `update_draft(draftId, fileId=<new>, ...)`, repeat step 4.
   - Change the text: edit the HTML, re-run the style check and `render_pdf.py`, upload, `update_draft`, repeat step 4.
Every loop needs a fresh `get_draft_file_url` call: old URLs are consumed.

Two things tested in September 2026 that bite: coordinates must be whole numbers (a value like 74.7 is stored as 0 and the field lands at the top of the page; `render_pdf.py` already rounds), and `update_draft` replaces the whole configuration: pass `name`, `language`, `personalMessage`, `sharingSetting`, `enableSigningOrder`, `fields` and the complete `signeeDetails` again every time, not only the part you change; a left-out `sharingSetting` becomes private and a left-out `language` becomes English, silently. `duplicate_draft` copies everything and costs nothing; use it when the user wants a second document for another client from the same file.

## 5. Send
`send_draft(draftId)`. No summary, no second confirmation: the preview and the user's "send now" are the confirmation. If validation fails (missing e-mail, missing box), fix with `update_draft` and go back to step 4. After success, one line in the user's language: the title, how many signers received the invitation, and the document URL that `send_draft` returned.

## 5b. Annexes and attachments
Tested September 2026: the API has no way for a signer to upload files during signing, and no separate attachment slot on a document. Every annex (for example proof of payment, registry extracts, certificates, photos) must therefore be inside the PDF before upload: embed images as data URIs and, for PDF annexes the user supplies, merge them into the document with `merge_files` after uploading each part with `upload_file` (one staged upload at a time), then create the draft from the merged `fileId`. Keep the signature page last: run `render_pdf.py` on the body with `--no-signatures`, merge the annex PDFs, then append a separately rendered signature page, or simply ask the user for image versions of the annexes. The attachment pattern for files the signer must supply is `references/attachments.md`.

## 6. After sending
- Signers without a Formify account sign from the e-mail link. If a signer should get the link by hand (a colleague standing next to the user), set `disableInvitationMessage: true` for that signer before sending and fetch the link with `get_recipient_links` afterwards; that link asks for a verification code sent to the contact on file.
- Reminders: `get_document` first, then `send_reminder` for signers whose `signatureStatus` is `awaiting_signature` and whose `reminderCooldown` is 0 (two per signer per hour). Status: `get_document`. Signed file: `get_signed_document_url`. A second document from a sent one: `duplicate_document` gives a new draft, nothing is sent.
- Field values on a sent document: `get_document_fields` lists the fields; `get_document_field_values` can answer 403 on some accounts, then say the values are visible in the Formify app and move on.
- Archive: the signed PDF stays in Formify. Where the segment has a statutory retention period (for example AML/KYC forms), state it and tell the user not to delete those documents.
- Then ask the memory question from `references/memory.md` ("save these settings as your default for this document type?"), and, for a document that qualifies, the template question from `references/templates-links.md`.

## 7. Errors
What heals with a retry and what needs a reconnect: `references/formify-errors.md`. Tell the user which call failed and what you are doing. Never claim a document was sent unless `send_draft` returned success.
