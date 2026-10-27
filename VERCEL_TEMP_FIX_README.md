# QA Nexus V8 temporary Vercel diagnostic fix

This patch changes only the SQLite database path to /tmp on Vercel and ensures init() runs when Vercel imports app.

**WARNING**: /tmp storage is ephemeral. Never store real test data using this build. Firebase synchronization is still one-way and will not make SQLite persistent.

1. Back up your local qa_manual.db.
2. Replace your app.py using this package; commit and push.
3. After Vercel redeploys, test /health and then /.
4. If error persists, check Vercel latest deployment ID and full runtime traceback.
5. Before production, migrate to a persistent database and implement authentication.
