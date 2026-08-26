"""
WebMCP declarative form example
===============================

Generate an HTML form annotated as a WebMCP tool.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from domonic.html import *


OUTPUT = Path(__file__).with_suffix(".html")


def build_page():
    return html(
        head(
            meta(_charset="utf-8"),
            meta(_name="viewport", _content="width=device-width, initial-scale=1"),
            title("domonic WebMCP form"),
            style(
                """
                body {
                    font-family: system-ui, sans-serif;
                    margin: 2rem;
                    line-height: 1.5;
                    color: #202124;
                }
                form {
                    display: grid;
                    gap: .75rem;
                    max-width: 32rem;
                }
                input,
                select,
                button {
                    font: inherit;
                    padding: .55rem .65rem;
                }
                """
            ),
        ),
        body(
            main(
                h1("Support request"),
                form(
                    label("First name", _for="firstName"),
                    input(_type="text", _name="firstName", _id="firstName"),
                    label("Last name", _for="lastName"),
                    input(_type="text", _name="lastName", _id="lastName"),
                    label("Request type", _for="requestType"),
                    select(
                        option("Return my purchase.", _value="Customer happiness team"),
                        option("Check where my package is.", _value="Distribution team"),
                        option("Get help on the website.", _value="Website support team"),
                        _name="requestType",
                        _id="requestType",
                        _required="",
                        _toolparamdescription="Determines what team this request is routed to.",
                    ),
                    button("Submit", _type="submit"),
                    _action="/support",
                    _method="post",
                    _toolname="supportRequestTool",
                    _tooldescription="Submit a request for customer support.",
                    _toolautosubmit="",
                ),
            )
        ),
    )


if __name__ == "__main__":
    render(build_page(), str(OUTPUT))
    print(f"Wrote {OUTPUT}")
