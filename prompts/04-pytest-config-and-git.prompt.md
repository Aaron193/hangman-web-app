two things on phase 1:

1. plain `pytest` fails with `ModuleNotFoundError: No module named 'server'`, only `python -m pytest` works. make both work (a pytest.ini with the project root on the path and testpaths = tests is probably enough) and check with the bare .venv/bin/pytest too. update the README commands if that changes anything.
2. git init failed in your sandbox so I ran `git init -b main` myself. run `git status` and make sure only the files we want would be tracked (no .venv, no assignment.md or cursor_transcript.md, and prompts/ should be in there). if that checks out, tick the git item in the TODO.

still no commits please.
