# D1: the same relational idea behind a Worker API

Week 4's `week04/api.py` reads a JSON tide file and returns data through an HTTP
API. It has no D1 binding. Here a small **Python Worker** runs a prepared SQL
query against a `DB` binding and returns related rows as JSON. D1 uses SQLite
SQL semantics; it is Cloudflare's managed relational service, not a vector store
and not a file Peewee opens directly. The new `WorkerEntrypoint` is the minimal
binding interface; Week 4 used FastAPI's ASGI adapter for its routes.

This is a tutor-prepared local demonstration, or an optional paired extension.
It fits inside the relational block; don't install a second platform during
project-support time. Use a prepared partner machine if setup stalls.

From **`week10/d1`**, with Node 22+:

```bash
npm ci
npm run seed
npm run dev
```

On the prepared machine, `python check_d1.py` runs HTTP/validation/restart
checks against a separate disposable local store. See [current validation
limits](../VALIDATION.md); the Python runtime must have its Pyodide bundle
available before class. If unavailable, keep the same relational exercise in
SQLite and observe the tutor’s prepared API demo instead of installing during
the support block.

The first install needs network access. These commands use Wrangler's local D1
emulation, a fictional ID and local state in `.wrangler/state`; no account,
Cloudflare login, remote database, key or payment is required. **Do not deploy
this configuration.** It is a read-only API over fictional public teaching rows,
not an authenticated history service. All clients can read these examples.

In another terminal:

```bash
curl 'http://127.0.0.1:8010/messages?conversation=1'
curl 'http://127.0.0.1:8010/messages?conversation=999'
curl -i 'http://127.0.0.1:8010/messages?conversation=bad'
```

**Predict → run → inspect:** find two messages, both joined to `Handbook`.
The unused conversation gives an empty result, not another user's rows.
Bad input gives HTTP 400. Trace `GET /messages` → Python parameter check →
`DB.prepare(SQL).bind(conversation).all()` → JSON. `?1` binds a value, not SQL
syntax. Read the three table definitions, PK/FK fields and compound index.

**Change → restart → check**, in another terminal from the same folder:

```bash
npx wrangler d1 execute sd5913-week10-local --local --command "UPDATE conversation SET title = 'Saved across restart' WHERE id = 1"
```

Stop the dev server with Ctrl+C, restart `npm run dev`, then repeat the first
curl. Both joined rows should show the changed title. Restarting the Worker
loses live Python objects but preserves the local database. Compare Week 9's
in-memory Scene, which resets on server restart.

**Recover:** reseeding is safe but deliberately does not overwrite your changed
row. Restore it with `UPDATE conversation SET title = 'Handbook' WHERE id = 1`.
Keep `.wrangler/state` to preserve experiments. For a fresh disposable database,
use a new `--persist-to` directory consistently on **both** `wrangler dev` and
`wrangler d1 execute`; don't delete a folder containing work you need. A missing
schema needs `npm run seed`; a port conflict needs a free port and matching curl.
Never substitute `--remote`: local and hosted D1 contain separate data.

A real hosted version needs an actual D1 resource and binding, access control,
operational limits and a separate deployment decision. It isn't part of this
exercise. No SQL relationship automatically authenticates a caller.

Official references checked 11 November 2026:
[Python Worker binding](https://developers.cloudflare.com/d1/examples/query-d1-from-python-workers/),
[prepared queries](https://developers.cloudflare.com/d1/worker-api/prepared-statements/),
[local development](https://developers.cloudflare.com/d1/best-practices/local-development/).
