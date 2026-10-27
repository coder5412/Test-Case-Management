# QA Nexus V8 — Manual Test Management + Firebase Mirror

This edition is based on **V7.1**, preserving editable/quick-create projects, Excel import, manual results, test-case revisions, bug tracker, reports, version comparison and version deletion.

## Execution numbering (as requested)
Version numbers increase monotonically **per project**. Create V1, delete V1, create a new run => **V2**. Deleting older runs does not reset counters; deleted numbers are not reused. Existing SQLite counters are preserved if you bring your previous `qa_manual.db`.

## Install (Windows PowerShell)
```powershell
python -m pip install -r requirements.txt
$env:QA_FIREBASE_CREDENTIALS = "C:\secure\vvahid-progress-service-account.json"
python app.py
```
Open http://127.0.0.1:5000/settings and use **Sync to Firebase Now**. The service-account private key is downloaded from Firebase Console → Project settings → Service accounts → Generate new private key. Keep it outside this project; never paste it into chat or public JS.

Firebase project: `vvahid-progress`.
Database: `https://vvahid-progress-default-rtdb.asia-southeast1.firebasedatabase.app`.
Dedicated namespace: **`/qa_nexus_manual_v8`**. Existing unrelated Firebase data is not touched.

## How sync works
Local **SQLite is primary**. Every successful write attempts to mirror the complete app-owned dataset into Firebase; errors are recorded and do not block the local transaction. Manual sync in Settings retries. `GET /api/firebase/status` returns the latest sync attempt. This is a **one-way mirror**, not cloud-based multi-user collaborative editing. No service-account credential is included.

## Preserve data
Stop old Flask, BACK UP `qa_manual.db` and place a copy in the extracted new project next to `app.py`. Do not reuse the V7.2 SQLite file if you want to roll back previous version numbering changes; the monotonic counter is used irrespective of that code. Always preserve a DB backup before changing versions.

## Safety
Bind Flask to localhost only; no authentication or CSRF, unsuitable for a public deployment. Do not change Firebase security rules to public write. The Firebase Admin SDK credentials remain private on your computer.
