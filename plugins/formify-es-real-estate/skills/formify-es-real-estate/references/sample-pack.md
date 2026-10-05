# The sample pack: the six documents to the user's inbox, or as drafts

Purpose: before building anything, the user can see the six documents as they will arrive to a client: as Formify documents in their own inbox, bilingual, with the boxes, the clauses and the signature area. Example data throughout (Inmobiliaria Ejemplo, Anna Andersson, Jan de Vries); the only personal data used is the user's own name and e-mail, as the single signer of each document.

Requirements: the Formify tools are connected and `get_current_user` answers. If not, say so in one line and offer the PDFs in the chat instead (`sample_pack.py` still produces them).

## Steps

1. `python3 scripts/sample_pack.py --out sample-pack [--organisation "<agency name from memory, if known>"] [--lang en]`. Seven PDFs (document 5, KYC, has a buyer and a seller form), in the order of the opening question (colaboración first) and `sample-pack/sample_pack.json` with, per document: `titulo` (numbered, Spanish / English), `pdf`, `paginas`, `mensaje` (invitation text) and `signatureBox` (the first signer's box, page 0-indexed).
2. Name and e-mail of the signer: the user (from memory or from `get_current_user`). Do not ask; confirm in the closing message.
3. Ask which way: "Send them to <e-mail>, or save them as drafts in your Formify account?" Then, for each entry, in order 1 to 6: `request_file_upload_url(fileName)` → run the returned curl command with the PDF path → `upload_file(uploadId)` → `create_draft(fileId, name=titulo, language=en|es|sv, sharingSetting=private, personalMessage=mensaje, signeeDetails=[{fullName, emailAddress, signatureType, signaturePlacement: "existing", signatureBox}])` with `signatureType` = "face_liveness" for the two KYC forms (5a, 5b; "digital_ink" only if `signatureFaceLiveness` is off) and "digital_ink" for the rest` → `send_draft(draftId)` in the send mode; in the draft mode stop after `create_draft`. The user asked for the pack, so no separate "send now?" question per document; one confirmation before the first send ("I will send the six documents to <e-mail>, one e-mail each. Go ahead?") is enough.
4. Closing message, short. Send mode: "Seven e-mails from Formify are on their way to <e-mail>, numbered 1 to 6 (5a and 5b are the two KYC forms). Nothing needs to be signed; open them and browse. When you are ready, tell me which document you want to make first." Mention that these documents count as sent documents in their Formify account. Draft mode: "Six drafts are saved in your Formify account under the titles 1 to 6; nothing has been sent. Tell me when you want one of them sent to you." The drafts appear in the app's Drafts view (checked 2026-09-08).

## Rules

- Never ask the user for agency data before the pack; the pack is the way to see the documents in one minute.
- If an upload fails with 401 or a network error, start again from `request_file_upload_url` for that document; never retry `upload_file` with the same uploadId.
- Invitation language: `en`, `es` or `sv` (Formify's invitation languages); pick the user's language when it is one of these, else English.
- After the pack, the wizard starts from "What do you want to do?" as usual; the pack changes nothing in the memory file except a line `sample_pack_sent: <date>` so it moves from the first to the last position of the opening question (it stays available there and under settings).
