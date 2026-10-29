Fixed the SVG rendering in [app.js](/home/dev/Desktop/college/senior/sem1/cse4095/hangman-web-app/static/app.js) by toggling the `hidden` attribute.

A headless Chrome check with mocked fetch responses verified each part’s computed display after every wrong guess, in the requested order, and verified that all parts disappear on a new game. All 79 existing tests pass. No commits were made.