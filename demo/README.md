# demo

One directory per install channel, named after the channel it shows. A recording only belongs
here if it demonstrates a path `README.md` actually tells someone to take.

| Directory | Channel | State |
|---|---|---|
| `claude-desktop/` | Claude Desktop, claude.ai chat and Cowork — the plugin path | recorded 2026-09-10 |
| `codex/` | Codex CLI and the Codex desktop app | recorded 2026-09-10 |

## What is in `claude-desktop/`

Three GIFs, one per step of the plugin install, referenced from `README.md` beside the step
each one shows:

| File | Step |
|---|---|
| `1-add-marketplace.gif` | Customize → Plugins → Add marketplace → `formify-e-sign/formify-skills` → Sync → Add |
| `2-connect-account.gif` | Connectors tab → Connect → sign in → Connected |
| `3-what-you-get.gif` | the installed plugin: description, categories, four skills, connector |

## What is in `codex/`

One GIF. The Codex recording covers a single action — adding the marketplace — because from
there the flow is the same as Claude's and the CLI covers the rest in two commands.

| File | Step |
|---|---|
| `1-add-marketplace.gif` | Plugins → Add → Add plugin marketplace → `formify-e-sign/formify-skills` → Add marketplace |

Nothing is blurred in it: the recording carries no conversation list, no browser, and no
account names. Only the local home-directory path appears, in the marketplace list.

## Rules for anything added here

- **GIF, not MP4.** GitHub renders an `.mp4` committed to a repository as a download link, not
  as a player. Video only plays when GitHub hosts it, which means it cannot live in the repo.
  A GIF always renders and plays on its own.
- **One GIF per step, not one film.** Someone installing watches the step they are on. A GIF
  sits beside its own instruction; an 85-second recording at the top of the page gets skipped.
- **Blur before committing.** The source recording carried a chat sidebar full of real
  conversation titles, browser tabs with a personal address, and internal account names. All
  three are blurred in what ships. Check every frame of a new recording for the same three.
- **No audio, no wallpaper.** Crop to the application window.
- **Budget: roughly 2 MB per GIF.** 820 px wide, 10 fps, 96-colour palette hits that for this
  material. Speed up the slow parts rather than cutting the frame rate further.

The blurred full-length master of the Claude Desktop recording is not committed — it is kept
outside the repository for the channels where video is accepted, such as LinkedIn and the
Smithery listing.
