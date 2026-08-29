## Examples

These examples are not all in the same runtime bucket.

Some are:
- pure render examples that only need `domonic`
- framework examples that need web-server packages
- parser/XPath examples that need parser or scraping extras
- websocket/browser demos that need socket extras and a browser
- local desktop/browser automation examples that need external tooling

### Baseline

For a broad local examples environment:

```bash
. venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pip install -e .
```

### Optional Dependencies

Examples that need extra packages beyond the core install:

- `fastapi`, `uvicorn`, `starlette`
  Used by:
  `games/hangman.py`, `games/rockpaperscissors.py`, `grid.py`, `lifecalendar.py`, `parsing/codemirror.py`

- `websockets`
  Used by:
  `events/events.py`, `sockets/atoms.py`, `sockets/atoms3d.py`, `sockets/diffdom_socket.py`, `sockets/events_test.py`, `sockets/gol.py`

- `requests`
  Used by:
  `parsing/newParser.py`, `parsing/page.py`, `parsing/html5libtest.py`, `parsing/codemirror.py`, `xpathtest.py`

- `html5lib`
  Used by:
  `parsing/html5libtest.py`

- `elementpath`
  Used by:
  `xpathtest.py`

- `selenium`
  Used by:
  `seleniumtest.py`

- `vapory`
  Used by:
  `mixed.py`

Legacy/optional experiments still referenced in comments:

- `flask`
- `geventwebsocket`
- `flask_threaded_sockets`

Those are not required for the main examples set, but some older socket examples mention them as alternate server ideas.

### Current Status

What has been checked recently:

- all Python example files compile on Python `3.13`
- one warning in `games/hangman.py` was cleaned up

What still needs real runtime validation when you step through them:

- websocket examples, because API drift in `websockets` is a common break point
- parser examples that fetch live sites
- selenium/browser automation examples
- anything that spins up a web server and expects manual browser interaction

### Running Examples

Pure examples:

```bash
. venv/bin/activate
cd examples
python alltags.py
python atom_feed.py
python diffdom.py
python mathml.py
python odf_content.py
python rss_feed.py
python scheduler_api.py
python speculation_rules.py
python validity_state.py
python webmcp_form.py
```

Nested examples:

```bash
. venv/bin/activate
cd examples/events
python events.py
```

Server-backed examples are usually better run from the repo root so local imports and assets behave consistently:

```bash
. venv/bin/activate
python examples/games/hangman.py
python examples/sockets/diffdom_socket.py
```
