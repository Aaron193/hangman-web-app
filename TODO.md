# TODO — Web Hangman assignment

This roadmap adapts [Specification.md](Specification.md) to the browser and server scope of assignment.md. Implement one phase at a time. Add and run relevant tests during each phase, review the result, and check a box only after its item has been verified. After each phase, review the code and resolve failures; the user will commit after review. Keep the game engine independent of Flask and the browser; the server is authoritative. Leave Specification.md unchanged and document scope changes or other deviations from it in README.md.

## Decisions for this implementation

- **Difficulty:** Use separate `words/easy.txt`, `words/medium.txt`, and `words/hard.txt` lists of lowercase ASCII words. Easy words have 3–5 letters, medium 6–8, and hard 9 or more. All levels allow six incorrect guesses. Select randomly from the chosen nonempty list; validate and deduplicate entries when loading.
- **Guesses:** Accept exactly one ASCII letter, case-insensitively, and normalize it to lowercase. Reject a repeated guess without changing the game or consuming a chance. Reject guesses after a game ends without changing the game.
- **Game JSON:** Create, retrieve, and successful guess responses use the same object: `game_id` (string), `difficulty` (`easy`, `medium`, or `hard`), `pattern` (space-separated letters and `_` characters), `guessed_letters` (every accepted guess, right and wrong, in order), `incorrect_letters` (only wrong guesses, in order), `remaining_guesses` (integer from 0 to 6), and `status` (`playing`, `won`, or `lost`). Include `word` only when status is `won` or `lost`; never expose it or another answer field while playing.
- **API:** `POST /api/games` accepts a JSON object with `difficulty`; `POST /api/games/{game_id}/guess` accepts a JSON object with `letter`; `GET /api/games/{game_id}` retrieves state. Return JSON errors as `{"error": "..."}`. Use 201 for creation, 200 for successful retrieval or guess, 400 for malformed JSON, invalid or missing fields, or a repeated guess, 404 for an unknown game ID, 409 for a guess on a finished game, and 415 for a POST without a JSON content type. Reject unexpected fields. Keep separate games in memory; a server restart loses them.

## Out of scope

Terminal clients, bots, evaluation, scoring, leaderboards, and logging/replay are excluded from this assignment plan. Persistent storage and accounts are also not needed.

## Phase 1 — Project setup

- [x] Initialize or verify the local Git repository on the main branch; avoid committing secrets, the virtual environment, assignment.md, or cursor_transcript.md.
- [ ] Connect a GitHub repository.
- [x] Create a Python virtual environment, dependency file, and minimal project layout for the engine, server, static assets, word lists, and tests.
- [x] Verify dependencies install and the test command runs in the environment, and document the commands for later use.

## Phase 2 — Word management

- [x] Add suitable word lists for each difficulty using the rules above; load, validate, and deduplicate them and select a random word for a requested level.
- [x] Add and run tests for each level, invalid difficulty, invalid or empty lists, and selection from the appropriate list.

## Phase 3 — Game engine

- [x] Implement independent game state, masking, case-normalized letter validation, correct and incorrect guesses, and the six-guess limit.
- [x] Implement duplicate rejection, win/loss detection, finished-game protection, and safe state serialization including end-of-game word disclosure.
- [x] Add and run deterministic unit tests for correct, incorrect, repeated and invalid guesses, wins, losses, and hidden-word disclosure.

## Phase 4 — Flask REST API

- [x] Create the Flask app, unique game IDs, and separate in-memory game states; implement the three required endpoints using the decisions above.
- [x] Validate JSON requests and return consistent status codes and JSON errors; serve the browser assets from Flask.
- [x] Add and run API tests for all difficulty levels, independent games, malformed requests, unknown IDs, duplicates, finished games, and answer secrecy while playing; exercise a complete game through HTTP.

## Phase 5 — Browser client

- [x] Build the difficulty selector and new-game flow, and render the server-provided pattern, guessed letters, remaining guesses, and game outcome.
- [x] Add clickable letters and keyboard input, a drawing that changes with incorrect guesses, and a way to start another game without reloading. Disable unavailable input and show request errors clearly.
- [x] Connect all game actions with `fetch()`; keep game rules and the active answer on the server. Verify browser updates after correct and incorrect guesses and test the interface at desktop and mobile sizes.

## Phase 6 — Testing and debugging

- [ ] Run the engine and API test suite and fix any failures; add tests for defects discovered during integration.
- [ ] Play games locally at every difficulty, including a win, a loss, invalid and repeated guesses, and a new game after completion.
- [ ] Inspect a guess request and its JSON response in Chrome Developer Tools; verify the displayed state updates and the active answer is absent from responses.

## Phase 7 — Docs and packaging

- [ ] Write README.md with local setup, run and test commands, browser usage, API examples, the decisions and deviations from Specification.md, and known limitations (including in-memory games and Render's free-tier idle sleep, which can make the first request take a minute or so).
- [ ] Ensure the repository includes the original specification, updated plan, source, word lists, dependencies, tests, and the `prompts/` folder; exclude local environments, secrets, and generated files.
- [ ] Verify the documented setup and play flow from a fresh clone or clean environment.

## Phase 8 — Render deployment

- [ ] Add Gunicorn to dependencies and configure Render to start the Flask app bound to `0.0.0.0:$PORT` with **one worker**, matching the app's module path.
- [ ] Push the verified project to GitHub and deploy it on Render; record the public HTTPS URL in the README.
- [ ] Verify the deployed page and all three API endpoints, play a complete browser game, start another, and confirm it works independently of the local server. Check the first request after free-tier idle sleep and keep the service accessible for grading.

## Phase 9 — Final submission

- [ ] Prepare the 1–2 page PDF report covering the development process, implementation, testing, deployment, a challenge and its resolution, and reflection; include 2–3 representative agent prompts.
- [ ] Record a roughly 2–3 minute demonstration of the deployed page, guesses through a complete win or loss, a new game, and an HTTP request and JSON response in Chrome Developer Tools.
- [ ] Verify the GitHub repository and public deployment URLs, report, recording, original specification, and updated TODO; submit the required materials through HuskyCT.
