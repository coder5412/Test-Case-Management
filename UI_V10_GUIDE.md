# QA Nexus UI V10 — All-page redesign

Updated: Dashboard, Test Case Library, Create/Edit Case, Excel Import, Execution List, Run Details, Bug Tracker, Bug Create/Edit, Reports, Version Comparison, Settings. All original Flask routes/actions preserved.

## Local run
`python -m pip install -r requirements.txt`
`python app.py`

## Deployment caution
Vercel temporary `/tmp` SQLite is not persistent. This UI release does NOT fix production storage or add authentication. Do not use it for live data on Vercel until a persistent database and authentication are implemented.

## Migration
Copy source into existing GitHub repo. Back up local `qa_manual.db` separately. Do not commit any database or service-account JSON. The update focuses on `templates/index.html`, `static/ui-v10.css`, retaining the existing app backend.
