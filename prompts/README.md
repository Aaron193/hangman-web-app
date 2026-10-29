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
- `NN-name.events.jsonl` is the full event stream (commands run, file edits, messages).
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
| 05 | [prompt](05-word-management.prompt.md) · [partial events](05-word-management.events.jsonl) (no response) | Phase 2: word lists, `WordManager`, tests | Stalled. The network dropped mid-run and Codex sat idle for about 21 minutes with no new events, so the reviewer stopped it. The word lists and `word_manager.py` had been written; the tests had not. Partial log kept as-is. |
| 06 | [prompt](06-word-management-resume.prompt.md) · [response](06-word-management-resume.response.md) | Resume the stalled Phase 2 session and finish the tests | Approved after one content fix. 22 tests pass. Lists independently validated (130 / 116 / 94 words, no duplicates, length rules met). Loader uses module-relative paths and an injectable RNG. Review spotted two bad words (`livingroom`, `froggy`). |
| 07 | [prompt](07-word-list-fixes.prompt.md) · [response](07-word-list-fixes.response.md) | Replace the two bad words | Approved. Swapped for `rainstorm` and `fridge`; counts, rules and tests unchanged. |
