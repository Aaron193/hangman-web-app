ok so I need to build and deploy a web-based hangman game for my agentic programming class (flask backend, html/css/js frontend, hosted on render). the full assignment is in assignment.md, and the original project spec and plan are Specification.md and TODO.md. please don't open cursor_transcript.md, that's the instructor's transcript and I'm not supposed to copy from it.

the spec covers a much bigger system than I need. for this assignment it's just the hangman server and the browser client. the terminal client, bots, evaluation, scoring and leaderboard are all out of scope, and logging/replay isn't one of the required endpoints so I'd drop that too.

can you rewrite TODO.md as a phased plan for only what's needed? right now it's the instructor's finished version, so every box is checked, and it points at a spec file called Hangman_Project_Specification.md that doesn't exist (it's Specification.md). I'd like phases for:

- project setup (git repo, venv, requirements, folder layout)
- game engine and word management
- flask server and REST API
- browser client
- testing and debugging
- docs and packaging
- cloud deployment on render (gunicorn, one worker)
- final submission stuff (report, screen recording, etc.)

everything should start unchecked, and boxes only get ticked after something is actually verified. phases should be small enough that I can hand them to you one at a time. please write tests as we go instead of saving them for the end.

also write down the stuff the spec leaves open so we stay consistent later: how easy/medium/hard differ, how repeated guesses are handled, which status codes the API returns, and what the game JSON looks like. add a short out-of-scope list too. leave Specification.md alone since it's a submission item, any deviations should go in the README instead.

don't write any code yet, just the plan. when you're done, give me a quick summary of what you changed.
