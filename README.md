# Hangman web app

Set up the project and install development dependencies:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
```

Run the tests:

```sh
.venv/bin/pytest
# Alternatively: .venv/bin/python -m pytest
```

Browser tests use the installed Google Chrome; no Playwright browser download is needed. Set `CHROME_PATH` to the Chrome executable if it is not available as `google-chrome` on your PATH. Browser tests are skipped if Playwright or Chrome is unavailable. Production dependencies are listed separately in `requirements.txt`.
