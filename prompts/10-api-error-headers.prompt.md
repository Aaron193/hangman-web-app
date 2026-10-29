two small things on server.py:

1. the NotFound import is inside find_game, move it up with the other imports.
2. 405 responses are missing the Allow header. the error handler builds a fresh response, so werkzeug's headers get dropped. keep the exception's headers when you turn it into JSON, add a test that checks the Allow header on a 405, and make sure the body and status of the other errors stay the same.

run the tests. no commits.
