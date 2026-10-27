"""Secure optional server-side mirror for manual QA database."""
import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

FIREBASE_URL = 'https://vvahid-progress-default-rtdb.asia-southeast1.firebasedatabase.app'
FIREBASE_PROJECT = 'vvahid-progress'
FIREBASE_PATH = 'qa_nexus_manual_v8'
_last_status = {'ok': False, 'message': 'Not synced yet', 'at': None}

def firebase_status():
    credential_path = os.environ.get('QA_FIREBASE_CREDENTIALS', '').strip()
    return {
        **_last_status,
        'configured': bool(credential_path and Path(credential_path).is_file()),
        'project': FIREBASE_PROJECT,
        'database_url': FIREBASE_URL,
        'firebase_path': '/' + FIREBASE_PATH,
        'credentials_path_set': bool(credential_path),
    }

def sync_to_firebase(db_path):
    """Mirror the app-owned namespace only. Never writes to Firebase root."""
    credential_path = os.environ.get('QA_FIREBASE_CREDENTIALS', '').strip()
    if not credential_path:
        result = {'ok': False, 'message': 'Set QA_FIREBASE_CREDENTIALS to the service-account JSON file.'}
        _last_status.update(result)
        return result
    if not Path(credential_path).is_file():
        result = {'ok': False, 'message': 'Firebase credential file not found.'}
        _last_status.update(result)
        return result
    try:
        import firebase_admin
        from firebase_admin import credentials, db as rtdb
        try:
            app = firebase_admin.get_app('qa-nexus-manual-v8')
        except ValueError:
            app = firebase_admin.initialize_app(
                credentials.Certificate(credential_path),
                {'databaseURL': FIREBASE_URL},
                name='qa-nexus-manual-v8',
            )
        tables = ['projects', 'cases', 'case_history', 'counters', 'runs',
                  'run_items', 'bugs', 'bug_comments', 'bug_events']
        local = sqlite3.connect(db_path, timeout=20)
        local.row_factory = sqlite3.Row
        try:
            snapshot = {}
            for table in tables:
                rows = local.execute(f'SELECT * FROM {table}').fetchall()
                # key by stable SQLite ID; RTDB arrays would create fragile indexes
                identifier = 'project_id' if table == 'counters' else 'id'
                snapshot[table] = {str(r[identifier]): dict(r) for r in rows} or None
        finally:
            local.close()
        # Update only an app-specific namespace, isolated from existing project data.
        rtdb.reference('/' + FIREBASE_PATH, app=app).set({
            'metadata': {'synced_at': datetime.now(timezone.utc).isoformat(),
                         'source': 'qa-nexus-manual-v8', 'mode': 'sqlite-mirror'},
            'data': snapshot,
        })
        result = {'ok': True, 'message': 'Synced successfully',
                  'at': datetime.now(timezone.utc).isoformat()}
        _last_status.update(result)
        return result
    except Exception as exc:
        result = {'ok': False, 'message': f'{type(exc).__name__}: {str(exc)[:250]}'}
        _last_status.update(result)
        return result
