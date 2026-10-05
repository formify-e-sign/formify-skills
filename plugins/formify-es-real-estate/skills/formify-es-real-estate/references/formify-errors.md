<!-- generated from core/references/formify-errors.md by build_vertical.py; edit the core file, not this copy -->
# Formify MCP errors: retry or reconnect

Read the error before acting; three different things have been called "session expired".
- `Error dialing https://api.anthropic.com/...`: the client's own proxy lost contact, nothing to do with Formify. Retry the call once.
- HTTP 404 `Session not found or expired`: the MCP session was idle for more than 30 minutes; the client starts a new one by itself. Retry once; if it repeats, report it.
- HTTP 401 `Token expired` or `Missing Bearer token`: the Formify token has run out (one hour in some clients). Ask the user to reconnect Formify in the client. This is the only case that needs a reconnect.
- The connector disappears from the client or sticks on the wrong login: the client's OAuth cache. Remove and re-add the connector in the client.
- `Formify API error (4xx): ...`: validation, missing permission or an object that does not exist; the message is Formify's own. Fix the input; never retry the same call unchanged.
- `Formify API error (500)`: one retry after a few seconds; seen once on `get_link` right after `create_link` and once on `create_document`.
- HTTP 429 `Too many requests`: 60 calls per minute per session. Wait a minute.
Tell the user which call failed and what you are doing: retry once, or leave the PDF and `signatures.json` for a manual upload. Never claim a document was sent unless `send_draft` returned success.
