ok the plan looks good, let's start on phase 1 (project setup). a few specifics:

- git: run `git init` on a main branch in this folder. don't create the github repo or push anything (I'll sort that out later) and don't commit yet, I want to review first.
- .gitignore: the usual python stuff (.venv, __pycache__, .pytest_cache, .env) plus assignment.md and cursor_transcript.md. prompts/ should stay tracked.
- layout: server.py (flask app named `app`, so `gunicorn server:app` works later), game.py, word_manager.py, static/ (index.html, style.css, app.js), words/ and tests/. stubs are fine, I just want the structure in place.
- python: venv in .venv, requirements.txt with flask, gunicorn and pytest (pin the versions you installed). install everything and make sure pytest actually runs. add one tiny smoke test so there's something for it to run, the app importing is enough.
- README.md: short stub with the setup and test commands for now, we'll flesh it out in phase 7.
- also add a short AGENTS.md with our working rules so I don't have to keep repeating them: work from TODO.md one phase at a time, only tick boxes after verifying, never edit Specification.md, don't open or copy from cursor_transcript.md, don't commit or push (I commit after reviewing), no secrets, keep the game engine independent of flask, and never let the hidden word out of the server while a game is still going.

only tick TODO boxes you verified. the github part of the first item isn't done, so split that into its own unchecked item. when you're done, tell me what you set up and which commands you ran to check it.
