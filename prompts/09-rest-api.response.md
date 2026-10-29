Phase 4 is complete. The Flask API uses an app factory with isolated in-memory games, validates requests and returns JSON errors, and serves the static assets. The module-level app and local entry point are also in place.

Added [API tests](/home/dev/Desktop/college/senior/sem1/cse4095/hangman-web-app/tests/test_api.py) covering the requested cases, including complete wins and losses and raw-response answer secrecy. All **79 tests passed** with `.venv/bin/pytest -q`, and the verified Phase 4 items are checked in [TODO.md](/home/dev/Desktop/college/senior/sem1/cse4095/hangman-web-app/TODO.md).

No commits were made.