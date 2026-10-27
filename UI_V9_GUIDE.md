# QA Nexus — UI V9

This is a front-end refresh of the V8 Vercel diagnostic edition. Existing Flask route logic and the manual test management workflow are preserved.

## What changed
- A compact workspace sidebar with active-page highlighting.
- Refined typography, whitespace, cards and dashboard metric accents.
- More readable compact tables and visually distinct status/priority badges.
- Improved test-case editor, execution accordion and bug forms.
- Responsive layouts for mobile/tablet and improved focus indicators.
- Existing `static/style.css` preserved; new overrides in `static/ui-upgrade.css`.

## Install locally
```
python -m pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000.

## Deploy to Vercel
Commit/push updated `templates/index.html` and `static/ui-upgrade.css` (or the full package). Static files need to be deployed together.

## Data warning
This package inherits the V8 diagnostic fix. On Vercel, SQLite may use `/tmp` to allow startup. `/tmp` is not durable storage. Firebase remains one-way backup, not primary persistence. Do not use the Vercel deployment for real data until a persistent database and access controls are implemented.

## Verification
Python syntax compilation, Jinja template parsing and ZIP integrity were checked. End-to-end browser behavior wasn't tested in this environment.
