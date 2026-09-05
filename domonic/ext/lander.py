"""
domonic.ext.lander
====================================

The "it worked" landing page a freshly scaffolded domonic server project
serves from ``/`` (see the ``HELLO_*`` scaffolds in ``domonic.ext`` and
``python -m domonic``). Generated projects import it rather than carrying a
copy of the markup:

.. code-block:: python

    from domonic.ext.lander import page

    @app.route("/")
    def index():
        return page()

``page()`` returns the rendered HTML string; ``LANDER`` is the underlying
domonic DOM tree if you want to inspect or tweak it.
"""

from __future__ import annotations

from domonic.html import (
    a,
    body,
    div,
    footer,
    h1,
    head,
    header,
    html,
    main,
    meta,
    p,
    section,
    span,
    strong,
    style,
    title,
)

_CSS = """\
:root {
  --ink: #171717;
  --muted: #686868;
  --paper: #fbfaf6;
  --line: #dedbd1;
  --accent: #ffcf33;
  --accent-soft: #fff0a8;
  --code: #20201f;
}

* { box-sizing: border-box; }

html, body {
  min-height: 100%;
  margin: 0;
}

body {
  min-height: 100vh;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
               "Segoe UI", sans-serif;
  color: var(--ink);
  background:
    radial-gradient(circle at 50% 34%, rgba(255, 218, 74, .20), transparent 22rem),
    linear-gradient(var(--paper), #f6f4ed);
  display: grid;
  place-items: center;
  overflow-x: hidden;
}

a { color: inherit; }

.shell {
  width: min(1120px, calc(100% - 40px));
  min-height: 100vh;
  display: grid;
  grid-template-rows: auto 1fr auto;
  padding: 28px 0 24px;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  width: fit-content;
  font-weight: 760;
  letter-spacing: -.025em;
  text-decoration: none;
  font-size: 17px;
}

.brand-mark {
  font-size: 22px;
  line-height: 1;
  transform: translateY(-1px);
}

main {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(360px, .82fr);
  align-items: center;
  gap: clamp(40px, 8vw, 110px);
  padding: 72px 0 80px;
}

.copy { max-width: 640px; }

.eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
  padding: 7px 11px 7px 9px;
  border: 1px solid var(--line);
  border-radius: 999px;
  background: rgba(255,255,255,.55);
  color: #54534f;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: .02em;
  box-shadow: 0 1px 0 rgba(0,0,0,.03);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #35a854;
  box-shadow: 0 0 0 4px rgba(53,168,84,.12);
}

h1 {
  margin: 0;
  max-width: 720px;
  font-size: clamp(48px, 7vw, 86px);
  line-height: .95;
  letter-spacing: -.062em;
  font-weight: 820;
}

h1 span {
  display: block;
  color: #77736b;
  font-weight: 620;
}

.lede {
  margin: 28px 0 0;
  max-width: 590px;
  color: var(--muted);
  font-size: clamp(18px, 2vw, 21px);
  line-height: 1.55;
  letter-spacing: -.012em;
}

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 11px;
  margin-top: 32px;
}

.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 44px;
  padding: 0 17px;
  border-radius: 10px;
  border: 1px solid var(--ink);
  background: var(--ink);
  color: white;
  text-decoration: none;
  font-size: 14px;
  font-weight: 740;
  transition: transform .16s ease, box-shadow .16s ease, background .16s ease;
}

.button:hover {
  transform: translateY(-1px);
  box-shadow: 0 7px 18px rgba(0,0,0,.11);
}

.button.secondary {
  background: rgba(255,255,255,.65);
  color: var(--ink);
  border-color: var(--line);
}

.visual {
  position: relative;
  aspect-ratio: 1 / 1;
  max-width: 470px;
  width: 100%;
  justify-self: center;
  display: grid;
  place-items: center;
}

.orbit {
  position: absolute;
  inset: 7%;
  border: 1px solid rgba(30,30,30,.10);
  border-radius: 50%;
  animation: spin 24s linear infinite;
}

.orbit::before,
.orbit::after {
  content: "";
  position: absolute;
  border-radius: 50%;
  background: var(--ink);
}

.orbit::before {
  width: 9px;
  height: 9px;
  top: 9%;
  left: 19%;
}

.orbit::after {
  width: 6px;
  height: 6px;
  right: 4%;
  bottom: 35%;
  opacity: .45;
}

.orbit.second {
  inset: 20%;
  animation-direction: reverse;
  animation-duration: 17s;
  border-style: dashed;
}

.orbit.second::before {
  background: var(--accent);
  width: 12px;
  height: 12px;
  top: 48%;
  left: -6px;
}

.orbit.second::after {
  width: 7px;
  height: 7px;
  right: 13%;
  bottom: 8%;
}

.mark-wrap {
  position: relative;
  width: 48%;
  aspect-ratio: 1;
  display: grid;
  place-items: center;
  border-radius: 34%;
  background: linear-gradient(145deg, rgba(255,255,255,.92), rgba(255,255,255,.5));
  border: 1px solid rgba(0,0,0,.08);
  box-shadow: 0 28px 80px rgba(51,45,18,.12), inset 0 1px 0 white;
  transform: rotate(4deg);
}

.mark-wrap::before {
  content: "";
  position: absolute;
  inset: 10%;
  border-radius: 30%;
  background: var(--accent-soft);
  opacity: .68;
  filter: blur(2px);
  transform: rotate(-8deg);
}

.mark {
  position: relative;
  z-index: 2;
  font-family: Georgia, "Times New Roman", serif;
  font-size: clamp(94px, 12vw, 150px);
  line-height: 1;
  transform: translateY(-3%) rotate(-4deg);
  text-shadow: 0 3px 0 rgba(255,255,255,.8);
  animation: breathe 3.8s ease-in-out infinite;
}

.node {
  position: absolute;
  padding: 8px 11px;
  border: 1px solid var(--line);
  border-radius: 9px;
  background: rgba(255,255,255,.84);
  backdrop-filter: blur(6px);
  font: 600 11px/1.2 ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  box-shadow: 0 8px 24px rgba(0,0,0,.05);
  white-space: nowrap;
}

.n1 { top: 10%; right: 1%; transform: rotate(4deg); }
.n2 { bottom: 13%; left: 0; transform: rotate(-5deg); }
.n3 { bottom: 4%; right: 8%; transform: rotate(2deg); }

.code {
  margin-top: 36px;
  width: fit-content;
  max-width: 100%;
  padding: 13px 15px;
  border: 1px solid #2a2a28;
  border-radius: 10px;
  background: var(--code);
  color: #e9e7de;
  font: 500 13px/1.55 ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  box-shadow: 0 12px 30px rgba(0,0,0,.10);
  overflow-x: auto;
}

.code .fn { color: #ffd75b; }
.code .str { color: #b9e986; }

footer {
  display: flex;
  justify-content: space-between;
  gap: 18px;
  color: #87847d;
  font-size: 12px;
  line-height: 1.5;
}

footer strong { color: #5f5c56; }

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes breathe {
  0%, 100% { transform: translateY(-3%) rotate(-4deg) scale(1); }
  50% { transform: translateY(-3%) rotate(-4deg) scale(1.045); }
}

@media (max-width: 820px) {
  .shell { width: min(680px, calc(100% - 32px)); }

  main {
    grid-template-columns: 1fr;
    gap: 42px;
    padding: 66px 0 54px;
  }

  .visual {
    order: -1;
    max-width: 330px;
  }

  .copy {
    text-align: center;
    margin-inline: auto;
  }

  .eyebrow,
  .code {
    margin-inline: auto;
  }

  .actions { justify-content: center; }

  footer {
    flex-direction: column;
    text-align: center;
  }
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: .001ms !important;
    animation-iteration-count: 1 !important;
    scroll-behavior: auto !important;
  }
}
"""

LANDER = html(
    head(
        meta(_charset="utf-8"),
        meta(_name="viewport", _content="width=device-width, initial-scale=1"),
        title("domonic — it worked"),
        style(_CSS),
    ),
    body(
        div(
            header(
                a(
                    span("𖤐", _class="brand-mark"),
                    span("domonic"),
                    _class="brand",
                    _href="https://domonic.readthedocs.io/",
                ),
            ),
            main(
                section(
                    div(
                        span(_class="status-dot"),
                        "development server running",
                        _class="eyebrow",
                    ),
                    h1(
                        "It worked.",
                        span("Your DOM is alive."),
                    ),
                    p(
                        "You’re seeing this page because domonic is installed "
                        "and your project is running correctly. Now replace this "
                        "route and start building with HTML, DOM and Web APIs "
                        "— in Python.",
                        _class="lede",
                    ),
                    div(
                        a(
                            "Read the docs →",
                            _class="button",
                            _href="https://domonic.readthedocs.io/",
                        ),
                        a(
                            "View on GitHub",
                            _class="button secondary",
                            _href="https://github.com/byteface/domonic",
                        ),
                        _class="actions",
                    ),
                    div(
                        span("html", _class="fn"),
                        "(",
                        span("body", _class="fn"),
                        "(",
                        span("h1", _class="fn"),
                        "(",
                        span('"Hello, world!"', _class="str"),
                        ")))",
                        _class="code",
                    ),
                    _class="copy",
                ),
                section(
                    div(_class="orbit"),
                    div(_class="orbit second"),
                    div(
                        div("𖤐", _class="mark"),
                        _class="mark-wrap",
                    ),
                    div("<html>", _class="node n1"),
                    div("querySelector()", _class="node n2"),
                    div("appendChild()", _class="node n3"),
                    _class="visual",
                ),
            ),
            footer(
                span(
                    strong("domonic"),
                    " · a Python DOM that goes beyond minidom",
                ),
                span("Replace the root route when you’re ready."),
            ),
            _class="shell",
        ),
    ),
    _lang="en",
)


def page() -> str:
    """Return the landing page as an HTML string."""
    return str(LANDER)
