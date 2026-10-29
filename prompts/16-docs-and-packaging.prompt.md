phase 7, docs and packaging. write the real README.md (replace the stub) covering:

- what the project is in a couple of sentences, plus a short features list
- quick start: clone, venv, install, run the server (python server.py, then open http://127.0.0.1:5000), and how to run the tests (the browser tests need chrome + playwright and skip themselves otherwise)
- how to play (difficulty picker, new game, buttons or keyboard, win/lose)
- project layout, one line per file or folder
- REST API reference for the three endpoints: request and response JSON, a curl example for each, the status codes, and the error format. the examples have to match what the server really returns
- how the browser talks to the server: a short walkthrough of what happens when you click a letter (fetch POST to /api/games/<id>/guess, flask validates it and updates the game, JSON comes back, the page redraws from it), plus how to see that in chrome devtools (network tab)
- design decisions and where we deviate from Specification.md: the difficulty word lengths, six wrong guesses everywhere, repeated guesses rejected with a 400, unexpected fields rejected, the state JSON being a superset of the spec's examples, and what's out of scope (terminal client, bots, evaluation, leaderboard, logging/replay)
- known limitations: games live in memory so they're lost on restart or redeploy, one gunicorn worker is required for that reason, and render's free tier sleeps when idle so the first request afterwards can take a minute or so
- a deployment section with the gunicorn command and a placeholder for the render URL, we'll fill it in when we deploy
- a line saying every prompt sent to the coding agent is logged in prompts/

keep it accurate and not bloated. also check that .gitignore and the requirements files cover everything a clean clone needs, and tick whichever phase 7 boxes you actually verified. leave the "fresh clone" one unchecked, I'll check that myself. no commits.
