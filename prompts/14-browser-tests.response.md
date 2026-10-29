Added [browser tests](/home/dev/Desktop/college/senior/sem1/cse4095/hangman-web-app/tests/test_browser.py) for the game flow, figure visibility, keyboard input, error messages, and API response secrecy and shape. The tests use the real Flask app with deterministic word lists and system Chrome.

Moved pytest to [requirements-dev.txt](/home/dev/Desktop/college/senior/sem1/cse4095/hangman-web-app/requirements-dev.txt), added Playwright there, and updated the [README](/home/dev/Desktop/college/senior/sem1/cse4095/hangman-web-app/README.md) setup commands. No browser download is required.

The full suite produced **79 passes and 9 browser failures**: Chrome launched, but the sandbox denied its connection to the local server with `net::ERR_ACCESS_DENIED`. All nine cases in `tests/test_browser.py` need to run on your machine:

```sh
.venv/bin/pytest tests/test_browser.py
```

I left the phase 6 TODO boxes unchecked because the browser coverage could not be verified here, including your Chrome DevTools item. No commits were made.