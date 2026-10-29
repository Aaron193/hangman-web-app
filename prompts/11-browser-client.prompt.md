phase 5, the browser client in static/ (index.html, style.css, app.js). plain html/css/js, no frameworks, no build step, no CDN stuff. all the game logic stays on the server: the page only sends requests with fetch() and draws whatever state comes back.

what I want to see:

- a title, a difficulty picker (easy / medium / hard, medium by default) and a New game button. start a game automatically on page load with the selected difficulty so there's something to play right away. changing the picker only matters the next time New game is pressed.
- the pattern big and monospaced, the remaining guesses, the letters guessed so far with the wrong ones called out (not just by colour), and a hangman drawn in inline SVG: gallows plus six parts (head, body, two arms, two legs) that show up as wrong guesses pile up. work out how many parts to show from the state the server sends instead of hard-coding anything about the word.
- an on-screen A-Z keyboard made of real buttons that get disabled once guessed (and marked right or wrong). the physical keyboard a-z does the same thing; ignore ctrl/alt/meta combos, and ignore keys while a request is pending or the game is over.
- a status area (aria-live) that says won or lost, shows the word only when the server sends it back at the end, and shows errors. cover the failure cases: the message from the server's {"error": ...} body, network failures, and a 404 on a game (server restarted or went to sleep), where it should say the game is gone and offer a new one. show some kind of "working..." state while a request is pending and don't allow double submits.
- once a game ends the keyboard is disabled and New game starts another one without reloading the page.
- usable on a phone (375px wide) as well as desktop: viewport meta tag, keyboard buttons that wrap nicely, tap targets big enough. decent contrast and visible focus styles. render server data with textContent, not innerHTML, and avoid a favicon request that 404s (an inline data: icon is fine).

if you can, open it in headless chrome (google-chrome is installed) and take screenshots at a desktop and a phone width to check the layout, but don't add any browser-testing packages to requirements.txt. keep the existing tests passing, tick the TODO boxes you actually verified, no commits.
