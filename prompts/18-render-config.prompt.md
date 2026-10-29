phase 8, render deployment config. the actual deploy comes after this, I'll push to github first.

- add a render.yaml blueprint for a python web service on the free plan: build command pip install -r requirements.txt, start command gunicorn --workers 1 --bind 0.0.0.0:$PORT server:app (one worker, since games live in memory), a health check on /, and pin the python version to the one we developed with. render wants a full x.y.z version for that, so 3.12.3. if you can't check render's docs from here, stick to the standard blueprint fields and tell me anything you weren't sure about.
- make sure requirements.txt has everything the build needs and nothing it doesn't (no pytest or playwright in there).
- run the exact start command locally with PORT set and check that / and one API call respond, then stop the server. please don't leave anything running afterwards.
- update the deployment section of the README with the steps (render dashboard: new blueprint instance from the github repo, or set the build and start commands by hand), keeping the URL placeholder for now.
- only tick what you verified in phase 8. the push and deploy boxes aren't done yet.

no commits.
