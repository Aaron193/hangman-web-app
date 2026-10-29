# Hangman web app

A browser-based Hangman game backed by a Flask REST API. The server chooses the word and keeps the game rules and state; the browser displays the results of each guess.

Features:
- Three difficulty levels and six incorrect guesses per game.
- On-screen letter buttons and keyboard input, with a drawing that grows after wrong guesses.
- Independent games with win/loss feedback and a new-game button.

## Quick start

```sh
git clone <repository-url>
cd hangman-web-app
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python server.py
```

On Windows, activate the environment with `.venv\Scripts\activate` instead. Open http://127.0.0.1:5000. Set the `PORT` environment variable before running `python server.py` to use a different port. In another terminal with the environment activated, run:

```sh
python -m pytest
```

Browser tests require Playwright and Google Chrome. Playwright is included in the development requirements; install Chrome separately. The tests look for `google-chrome` on `PATH`, or use `CHROME_PATH` for its executable. They skip themselves if Playwright or Chrome is unavailable or Chrome cannot launch. A Playwright browser download is not needed.

## How to play

A medium game starts when the page loads. Choose easy, medium, or hard in the difficulty picker and select **New game** to start with that level. Click a letter or type it on the keyboard. Correct guesses reveal matching letters; wrong guesses reduce the remaining count and add to the drawing. Reveal the whole word to win, or make six wrong guesses to lose. The word is shown when the game ends; select **New game** to play again.

## Project layout

- `server.py` — Flask app, API routes, and static-file entry point.
- `game.py` — Flask-independent game rules and state.
- `word_manager.py` — word-list loading, validation, and selection.
- `words/` — difficulty-specific word lists.
- `static/` — browser HTML, CSS, and JavaScript.
- `tests/` — engine, word manager, API, smoke, and browser tests.
- `requirements.txt` — production dependencies.
- `requirements-dev.txt` — production and test dependencies.
- `pytest.ini` — pytest configuration.
- `Specification.md` — original project specification.
- `TODO.md` — phased implementation plan.
- `AGENTS.md` — working rules for coding agents.
- `prompts/` — coding-agent prompt and run records.
- `.gitignore` — local and generated files excluded from Git.
- `README.md` — setup, usage, API, and deployment guide.

Every prompt sent to the coding agent is logged in `prompts/`.

## REST API

POST requests require a JSON content type and exactly the specified string field; unexpected fields are rejected. All successful endpoints return the same state object. `pattern` is space-separated, `guessed_letters` contains accepted guesses in order, and `incorrect_letters` contains wrong guesses in order. `status` is `playing`, `won`, or `lost`. The `word` field is present only after a win or loss.

Flask returns JSON keys in alphabetical order; the examples put `game_id` first for readability. JSON key order does not affect the response.

These example responses describe one possible game with the randomly selected word `cat`; actual IDs, word lengths, and results vary. Replace `GAME_ID` in the commands with the ID returned by creation.

### Create a game

`POST /api/games` — request JSON: `{"difficulty":"easy"}` (also `medium` or `hard`).

```sh
curl -X POST http://127.0.0.1:5000/api/games \
  -H 'Content-Type: application/json' -d '{"difficulty":"easy"}'
```

Response `201 Created`:

```json
{"game_id":"0123456789abcdef0123456789abcdef","difficulty":"easy","pattern":"_ _ _","guessed_letters":[],"incorrect_letters":[],"remaining_guesses":6,"status":"playing"}
```

### Retrieve a game

`GET /api/games/<game_id>` — no request body.

```sh
curl http://127.0.0.1:5000/api/games/GAME_ID
```

Response `200 OK`, before any guesses in the example game:

```json
{"game_id":"0123456789abcdef0123456789abcdef","difficulty":"easy","pattern":"_ _ _","guessed_letters":[],"incorrect_letters":[],"remaining_guesses":6,"status":"playing"}
```

### Guess a letter

`POST /api/games/<game_id>/guess` — request JSON: `{"letter":"c"}`. A guess must be one ASCII letter; uppercase is accepted and normalized to lowercase.

```sh
curl -X POST http://127.0.0.1:5000/api/games/GAME_ID/guess \
  -H 'Content-Type: application/json' -d '{"letter":"c"}'
```

Response `200 OK`, after guessing `c` in the example game:

```json
{"game_id":"0123456789abcdef0123456789abcdef","difficulty":"easy","pattern":"c _ _","guessed_letters":["c"],"incorrect_letters":[],"remaining_guesses":6,"status":"playing"}
```

After the remaining letters `a` and `t` are guessed, the state includes `"status":"won"` and `"word":"cat"`. A lost game also includes `word`.

### Errors and status codes

Errors are JSON objects such as `{"error":"Letter has already been guessed"}`. The message depends on the error.

- `400 Bad Request` — malformed JSON, missing, invalid, or unexpected fields, invalid difficulty or letter, or a repeated guess.
- `404 Not Found` — unknown game ID or route.
- `409 Conflict` — a valid letter was guessed after the game ended.
- `415 Unsupported Media Type` — a POST without a JSON content type.
- `405 Method Not Allowed` — the route does not accept the HTTP method.
- `500 Internal Server Error` — an unexpected server error.

## Browser and server

When you click a letter, the page sends a `fetch` POST to `/api/games/<id>/guess` with the letter as JSON. Flask validates the request and updates the game; the response contains the new state as JSON, and the page redraws from it. The answer is absent from responses while the game is in progress.

To inspect this in Chrome, open Developer Tools, select **Network**, and click a letter. Select the `guess` request to inspect its **Payload** and **Response** tabs, and compare the response with the updated page.

## Design decisions and scope

The word lists use 3–5 letters for easy, 6–8 for medium, and 9 or more for hard; every level allows six wrong guesses. Repeated guesses are rejected with `400` without consuming a chance, and unexpected request fields are rejected. The state JSON is a superset of the examples in `Specification.md`, adding fields needed by the browser. These decisions adapt the specification to the web assignment. Terminal clients, bots, evaluation, leaderboards, and logging/replay are out of scope.

## Deployment and limitations

Games live in server memory and are lost on restart or redeploy. Use one Gunicorn worker so all requests reach the same game store:

```sh
gunicorn --workers 1 --bind 0.0.0.0:$PORT server:app
```

Render URL: **[to be added after deployment]**. Render's free tier sleeps when idle, so the first request afterward can take a minute or so.
