I followed the README from a clean copy of everything that would be committed: new venv, pip install -r requirements-dev.txt, python -m pytest (88 passed, browser tests included), python server.py on 5000, the curl examples, and the gunicorn command. all of it works, so tick the fresh-clone box in phase 7.

three small things for the README while you're in there:

1. the examples list game_id first, but flask returns the keys in alphabetical order (difficulty, game_id, guessed_letters, ...). add a short note so nobody's surprised.
2. say that you can set the PORT environment variable to change the port for python server.py.
3. the activate command in the quick start is the linux/mac one, so add the windows one (.venv\Scripts\activate).

no commits.
