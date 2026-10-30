I timed the first request after idle sleep. the service had been untouched for about 18 minutes and the first request (GET /) took 21 seconds to come back with a 200, then requests were fast again, around 0.2 to 0.3 seconds. so it sleeps and wakes up fine, and the wait is about 20 seconds. I also confirmed the render service was created as a blueprint from render.yaml.

same rule as last time: please don't curl or open the live url yourself.

1. README.md: update the free-tier note in the deployment section with this (it sleeps after about 15 minutes idle, the first request after that took about 21 seconds in one test and can take up to a minute, then it's fast again). keep the wording neutral, no "I". also add a short note to the "Live app" line near the top so someone who opens it cold knows the first load can be slow.
2. TODO.md: tick the last phase 8 box. the "keep the service accessible for grading" part can't be verified until grading is over though, so take that phrase out of the phase 8 box and add it to the last phase 9 box instead (that one stays unticked). leave the other phase 9 boxes alone.
3. submission/report.md:
   - testing: remove the sentence you added about the public url checks, the same numbers are in the deployment paragraph.
   - deployment: say the service was created as a Render Blueprint from the repo's render.yaml (python 3.12.3, one gunicorn worker, health check on /). replace the long public-checks sentence with a short one: the same independent api and browser checks (55 api checks and 39 browser checks) were repeated against the public url, all passed, with no local server running. replace the "making the first request afterward slow" part with the timing: it sleeps after about 15 minutes idle, the first request after about 18 idle minutes took about 21 seconds, and later requests took a fraction of a second.
   - nothing else changes. the prompt log count stays at 21 and the reflection stays as it is.
4. submission/demo-script.md: where it says the first load can take around a minute, say it took about 21 seconds when I timed it but to allow up to a minute.
5. rebuild the pdf, still 2 pages or fewer, with the representative prompts block together on page 2.

no commits.
