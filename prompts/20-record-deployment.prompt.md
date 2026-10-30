the render deploy is live: https://hangman-web-app-dwlq.onrender.com (github repo is https://github.com/Aaron193/hangman-web-app). I ran our api checks and a real-browser check against the public url from my machine, with no local server running. 55 api checks passed (29 error cases, 24 full games over https with 12 wins and 12 losses, and no word in any in-progress response) and 39 browser checks passed (a full win and a full loss, new game, keyboard input, a 375px phone viewport, injected network/400/404/500 errors).

please don't curl or open the live url yourself while you do this. I'm in the middle of checking what the first request after idle sleep looks like and any request would wake the service up. everything you need is above.

1. README.md: put the real url in the deployment section where the placeholder is, and add a one-line "Live app: <url>" under the intro paragraph at the top so it's easy to find. keep the note about the free tier sleeping.
2. TODO.md: tick the phase 8 box about pushing, deploying and recording the url in the README. leave the next box (verify the deployed app + the idle check) open, I haven't finished the idle part.
3. submission/report.md, update it for the deployed state:
   - title: drop "(Draft)".
   - development process: the prompt log will have 21 prompts by the time this is all done (this is the 20th, and I'll send one more small one after I've timed the cold start), so say that instead of the "18 earlier turns, plus ... turn 19" wording. keep it plain.
   - testing: take out the sentence saying the DevTools inspection still has to be done. the recording covers that and I don't want the report claiming anything about it yet. add one sentence that the same api and browser checks were also run against the public url (use the numbers above).
   - deployment: the repo is on github and deployed from there to a render free web service, the url, the settings in the repo's render.yaml (python 3.12.3, one gunicorn worker, health check on /), what was checked on the public url (numbers above), and that games are in memory so a restart or redeploy clears them. mention that the free tier sleeps when idle and the first request afterwards is slow, but don't put a number on it yet. don't say how the service was created in the render dashboard (blueprint vs manual), I haven't confirmed which one was used.
   - challenges: fine as is.
   - reflection: keep it short. the last sentence says I still need to verify the deployed service and finish the demo, which isn't true any more, so reword it. put an italic line right under the "Reflection" heading saying it's a draft that gets rewritten in my own words before submitting.
   - nothing else should change, and the three prompt excerpts stay verbatim.
4. submission/demo-script.md: fill in the url, and change the "before recording" note so it says to open the site once a couple of minutes before recording so the free-tier service is awake (it sleeps after about 15 minutes idle and the first load can take around a minute).
5. submission/build-report.sh and report.pdf: the "Representative prompts" heading and its intro line ended up at the bottom of page 1 with the excerpts on page 2. keep that whole block (heading, intro line and the three excerpts) together, so if it doesn't fit on page 1 it all moves to page 2. rebuild the pdf, check it's still 2 pages or fewer, and check with pdftotext that the heading isn't stranded at the bottom of a page.

no commits.
