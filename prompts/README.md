# Prompt log

Record of every prompt sent to the Codex CLI while building this project, and what came back.

## Who did what

- **Prompts:** written by Claude Code (Claude), acting as the prompter and reviewer on the student's behalf.
- **Implementation:** Codex CLI 0.165.0, model `gpt-6.1-terra`, reasoning effort `medium`, `workspace-write` sandbox.
- **Review:** after each Codex run, Claude checks the diff, runs the tests and the app, and sends follow-up prompts for anything that isn't right before the phase is committed.

## Files

One set per turn, numbered in the order sent:

- `NN-name.prompt.md` is the exact text sent to Codex.
- `NN-name.response.md` is Codex's final message for that turn.
- `NN-name.events.jsonl` is the full event stream (commands run with their output, file edits, messages). These are kept on the author's disk only and are not committed, because they contain verbatim command output, including course materials.
- `runs.tsv` has the start time, end time, and exit status of each turn.

## Command used for every turn

```bash
codex exec --ignore-user-config -m gpt-6.1-terra \
  -c 'model_reasoning_effort="medium"' \
  -c 'sandbox_workspace_write.network_access=true' \
  -s workspace-write --json -o NN-name.response.md - < NN-name.prompt.md > NN-name.events.jsonl
```

Follow-ups within the same Codex session use `codex exec resume <thread id>` with the same options. The thread id is in the first event of the previous turn's `.events.jsonl`, and `runs.tsv` records which thread each turn ran in.

## Index

| # | Prompt | Purpose | Review outcome |
|---|--------|---------|----------------|
| 01 | [prompt](01-revise-todo.prompt.md) · [response](01-revise-todo.response.md) | Step 1: rewrite TODO.md as a phased plan for the reduced scope (no code) | Approved with polish. 9 phases, all boxes unchecked, spec untouched, decisions and out-of-scope sections added. Needed fixes: dead link, ambiguous JSON field, no cold-start note. |
| 02 | [prompt](02-todo-polish.prompt.md) · [response](02-todo-polish.response.md) | Fix the four polish items in the TODO | Approved. All four edits made, nothing else changed. |
| 03 | [prompt](03-project-setup.prompt.md) · [response](03-project-setup.response.md) | Phase 1: repo layout, venv, pinned requirements, .gitignore, README stub, AGENTS.md | Approved after two fixes. Layout, pins, ignore rules and AGENTS.md were right. Review found that bare `pytest` failed (only `python -m pytest` had been tested), and Codex could not run `git init` because its sandbox write-protects `.git`, so the reviewer ran it. |
| 04 | [prompt](04-pytest-config-and-git.prompt.md) · [response](04-pytest-config-and-git.response.md) | Make plain `pytest` work; check what git would track; tick the git item | Approved. Added `pytest.ini`; bare `pytest`, `python -m pytest` and running from `tests/` all pass. Git item ticked, GitHub item left open. |
| 05 | [prompt](05-word-management.prompt.md) (no response; partial event log kept locally) | Phase 2: word lists, `WordManager`, tests | Stalled. The network dropped mid-run and Codex sat idle for about 21 minutes with no new events, so the reviewer stopped it. The word lists and `word_manager.py` had been written; the tests had not. Partial log kept as-is. |
| 06 | [prompt](06-word-management-resume.prompt.md) · [response](06-word-management-resume.response.md) | Resume the stalled Phase 2 session and finish the tests | Approved after one content fix. 22 tests pass. Lists independently validated (130 / 116 / 94 words, no duplicates, length rules met). Loader uses module-relative paths and an injectable RNG. Review spotted two bad words (`livingroom`, `froggy`). |
| 07 | [prompt](07-word-list-fixes.prompt.md) · [response](07-word-list-fixes.response.md) | Replace the two bad words | Approved. Swapped for `rainstorm` and `fridge`; counts, rules and tests unchanged. |
| 08 | [prompt](08-game-engine.prompt.md) · [response](08-game-engine.response.md) | Phase 3: `HangmanGame`, error classes, `to_dict()`, tests | Approved on the first try. 51 tests pass. Code review: ASCII-only validation uses `fullmatch` (rejects `"a\n"`, `"é"`, full-width `"Ａ"`), errors raised in the requested order (invalid, game over, duplicate), state unchanged after every rejected guess, serialization returns copies, `word` appears only once the game is over, no Flask imports. |
| 09 | [prompt](09-rest-api.prompt.md) · [response](09-rest-api.response.md) | Phase 4: Flask REST API (app factory, validation, JSON errors, static serving) and API tests | Approved after one follow-up. 79 tests pass. Independent black-box check against `gunicorn --workers 1` (reviewer's script, not part of the repo): all endpoints, 29 error cases with JSON bodies and the right codes, 24 complete games over HTTP (12 wins, 12 losses), and the word never present in an in-progress response. Review found two small issues: an import inside a function, and 405 responses missing the `Allow` header. |
| 10 | [prompt](10-api-error-headers.prompt.md) · [response](10-api-error-headers.response.md) | Move the import; keep exception headers (`Allow`) on JSON errors | Approved. 405s now send `Allow: POST, OPTIONS`; error bodies and statuses unchanged; test added; black-box check still green. |
| 11 | [prompt](11-browser-client.prompt.md) · [response](11-browser-client.response.md) | Phase 5: browser client (`static/index.html`, `style.css`, `app.js`) | Not approved as delivered. Code read well (`fetch` only, `textContent` only, no game logic, double-submit guard, error handling), but Codex's own browser check had used mocked responses because its sandbox could not reach the server. The reviewer drove the real UI in headless Chrome against `gunicorn --workers 1` (harness not in the repo) and found a serious bug: **the hangman figure never appeared**. The parts were SVG elements, and `part.hidden = ...` does not work on SVG, so the HTML `hidden` attribute was never removed. |
| 12 | [prompt](12-fix-hangman-figure.prompt.md) · [response](12-fix-hangman-figure.response.md) | Fix the figure (use `toggleAttribute`) and verify on rendered output | Approved. Live run confirmed parts appear in order (head, body, arms, legs) and reset on a new game. |
| 13 | [prompt](13-ui-polish.prompt.md) · [response](13-ui-polish.response.md) | Phone layout (pattern under the drawing, 12-letter word on one line at 375px), green/red outcome banners, focus to New game | Approved. 39 of 39 real-browser checks pass: full win and loss, keyboard and button input, double-submit, injected network/404/400/500 failures, phone viewport, no console errors. |
| 14 | [prompt](14-browser-tests.prompt.md) · [response](14-browser-tests.response.md) | Phase 6: browser regression tests (Playwright on the system Chrome), dev-only requirements file | Approved after independent verification. Codex could not run the browser tests in its own sandbox (Chrome was denied access to the local server), said so, and left the boxes unchecked. Outside the sandbox the full suite passes: 88 tests (9 browser). Mutation check in a scratch copy: re-introducing the SVG bug, a "keyboard stays enabled after the game ends" bug and a "focus not moved to New game" bug each made the browser tests fail, and the unmodified control passed. |
| 15 | [prompt](15-tick-phase-6.prompt.md) · [response](15-tick-phase-6.response.md) | Tick the two Phase 6 boxes that were verified | Approved. The Chrome DevTools box was deliberately left unchecked; it is a manual step for the student. |
| 16 | [prompt](16-docs-and-packaging.prompt.md) · [response](16-docs-and-packaging.response.md) | Phase 7: real README, packaging checks, `.gitignore` | Approved. README covers every requested section. Verified by following it literally from a clean copy of what would be committed: new venv, `pip install -r requirements-dev.txt`, 88 tests pass, `python server.py`, every curl example, and the documented gunicorn command. While doing this the reviewer found a Codex-launched `python server.py` still running on port 5000 from an earlier turn and stopped it; the run script now cleans up such leftovers after every turn. |
| 17 | [prompt](17-readme-verified.prompt.md) · [response](17-readme-verified.response.md) | Tick the fresh-clone box; add README notes on JSON key order, `PORT` and the Windows activate command | Approved. |
| 18 | [prompt](18-render-config.prompt.md) · [response](18-render-config.response.md) | Phase 8: `render.yaml` Blueprint and README deployment steps | Approved. Free Python web service, Python 3.12.3, one gunicorn worker, health check on `/`; Codex checked the fields against Render's docs. The start command was run locally (`/` returned 200, game creation 201, the word was not exposed) and the server was stopped. Only the configuration box was ticked; the push and deploy boxes remain open. |
