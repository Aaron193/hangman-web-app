Phase 8’s deployment configuration is ready for review.

- Added [render.yaml](/home/dev/Desktop/college/senior/sem1/cse4095/hangman-web-app/render.yaml) with the free Python service, Python 3.12.3, one Gunicorn worker, and a `/` health check. The fields were checked against [Render’s Blueprint reference](https://render.com/docs/blueprint-spec) and [Python version documentation](https://render.com/docs/python-version).
- Updated the [README](/home/dev/Desktop/college/senior/sem1/cse4095/hangman-web-app/README.md) with Blueprint and manual deployment steps, retaining the URL placeholder.
- Confirmed `requirements.txt` contains Flask and Gunicorn only. A clean environment installed it successfully.
- Ran the exact start command: `/` returned 200 and game creation returned 201 without exposing the active word. The server was stopped and its port is closed. Gunicorn logged a control-server read-only filesystem error in the local sandbox, although both requests succeeded.
- Checked only the verified configuration item in [TODO.md](/home/dev/Desktop/college/senior/sem1/cse4095/hangman-web-app/TODO.md). Push and deployment remain unchecked.

No commit or push was made.