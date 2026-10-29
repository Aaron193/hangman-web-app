phase 4, the flask REST API in server.py. use the decisions section in the TODO for the endpoints, status codes and JSON. a few things on top of that:

- use an app factory, create_app(word_manager=None), and keep a module-level `app = create_app()` so `gunicorn server:app` works. games live in an in-memory dict that belongs to the app, so every test gets a fresh store. game ids should be random and unguessable (uuid4 hex is fine). tests can pass in a WordManager pointed at a tmp words dir with one word per list, which keeps wins and losses deterministic.
- the response for create / get / guess is just game.to_dict() from game.py. map the engine's exceptions the way the TODO says (invalid and duplicate guesses 400, guess after the game ended 409).
- check the game id first (unknown id is 404 no matter what the body looks like), then the body: not a JSON content type 415, malformed JSON 400, a body that isn't an object 400, missing / unexpected / wrong-typed fields 400, bad difficulty 400.
- every error comes back as {"error": "..."} JSON, including flask's own 400, 404, 405 and 415 and an unexpected 500, so use a generic error handler instead of the default html pages.
- GET / serves static/index.html and the other assets come from /static, same origin so no CORS.
- add a `python server.py` entry point for local runs: host 127.0.0.1, port from the PORT env var (default 5000), debug off.

tests/test_api.py with the flask test client: create at all three difficulties, independent games, all the malformed request cases above, unknown game ids for GET and guess, repeated and invalid letters (state unchanged), a guess after the game has finished, wrong method and unknown route returning JSON, the word never appearing in any response while a game is in progress (check the raw body text, not just a "word" key, and use a distinctive test word so a substring match can't be a false positive), the word showing up after a win and after a loss, and one complete win and one complete loss played purely through HTTP. also check GET / and a static file.

run all the tests, tick what you verified in the TODO, no commits.
