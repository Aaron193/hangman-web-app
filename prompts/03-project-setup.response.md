Phase 1 setup is in place, with one local Git task still blocked.

- Created the requested project layout, Flask `server:app` stub, smoke test, README, `.gitignore`, and [AGENTS.md](/home/dev/Desktop/college/senior/sem1/cse4095/hangman-web-app/AGENTS.md).
- Created `.venv` and pinned the installed Flask, Gunicorn, and pytest versions in [requirements.txt](/home/dev/Desktop/college/senior/sem1/cse4095/hangman-web-app/requirements.txt).
- Checked the two verified setup items in [TODO.md](/home/dev/Desktop/college/senior/sem1/cse4095/hangman-web-app/TODO.md). Local Git initialization and the separately listed GitHub task remain unchecked.

Verification used `.venv/bin/python -m pip install -r requirements.txt`, `.venv/bin/python -m pip check`, and `.venv/bin/python -m pytest` (one test passed). I also checked that `server:app` is a Flask application and used `git check-ignore` with a temporary repository to verify the ignore rules and that `prompts/` remains eligible for tracking.

**Git initialization did not complete:** `git init -b main` failed because the existing `.git` directory is read-only in this environment. You can run `git init -b main` locally once that directory is writable. No commit, push, or GitHub repository was created.