"""
Speculation Rules example
=========================

Generate a page with browser navigation hints and measurable hero markup.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from domonic.html import *


OUTPUT = Path(__file__).with_suffix(".html")


def build_page():
    rules = {
        "prefetch": [
            {
                "source": "list",
                "urls": ["/docs/", "/examples/"],
                "eagerness": "moderate",
            }
        ],
        "prerender": [
            {
                "source": "document",
                "where": {"href_matches": "/checkout/*"},
                "eagerness": "conservative",
            }
        ],
    }

    return html(
        head(
            meta(_charset="utf-8"),
            meta(_name="viewport", _content="width=device-width, initial-scale=1"),
            title("domonic speculation rules"),
            importmap(
                {
                    "imports": {
                        "app/": "/static/app/",
                        "lit": "https://cdn.jsdelivr.net/npm/lit/+esm",
                    }
                },
                indent=2,
            ),
            speculationrules(rules, indent=2),
            script(
                _src="/campaign.js",
                _attributionsrc="https://example.com/register-source",
            ),
            style(
                """
                body {
                    font-family: system-ui, sans-serif;
                    margin: 2rem;
                    line-height: 1.5;
                    color: #17202a;
                }
                main {
                    max-width: 44rem;
                }
                nav {
                    display: flex;
                    flex-wrap: wrap;
                    gap: .75rem;
                    margin-top: 1.5rem;
                }
                a {
                    border: 1px solid #9aa8b8;
                    color: #17202a;
                    padding: .6rem .75rem;
                    text-decoration: none;
                }
                """
            ),
        ),
        body(
            main(
                h1("Modern navigation hints", _elementtiming="hero-heading"),
                p(
                    "This page renders a speculation rules block plus attribution-capable assets with domonic."
                ),
                nav(
                    a("Docs", _href="/docs/"),
                    a("Examples", _href="/examples/"),
                    a("Campaign link", _href="/checkout/demo", _attributionsrc=""),
                ),
                script("import { boot } from 'app/boot.js'; boot();", _type="module"),
            )
        ),
    )


if __name__ == "__main__":
    render(build_page(), str(OUTPUT))
    print(f"Wrote {OUTPUT}")
