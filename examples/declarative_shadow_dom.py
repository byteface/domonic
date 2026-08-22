import sys

sys.path.insert(0, "..")

from domonic import render
from domonic.html import *

profile_card = create_element(
    "profile-card",
    template(
        style("""
            :host {
                display: block;
                font-family: system-ui, sans-serif;
                max-width: 28rem;
            }

            .card {
                border: 1px solid #d0d7de;
                border-radius: 8px;
                padding: 1rem;
                background: #fff;
                box-shadow: 0 1px 2px rgba(31, 35, 40, 0.08);
            }

            .name {
                display: block;
                font-size: 1.15rem;
                margin-bottom: 0.25rem;
            }

            ::slotted(img) {
                width: 3rem;
                height: 3rem;
                border-radius: 50%;
                object-fit: cover;
                float: right;
                margin-left: 1rem;
            }
            """),
        article(
            slot(_name="avatar"),
            strong(slot(_name="name"), _class="name"),
            p(slot()),
            _class="card",
        ),
        _shadowrootmode="open",
    ),
    img(
        _slot="avatar",
        _src="https://avatars.githubusercontent.com/u/314543",
        _alt="byteface avatar",
    ),
    span("byteface", _slot="name"),
    "Declarative Shadow DOM lets domonic output a server-rendered web component.",
)

page = html(
    head(
        meta(_charset="utf-8"),
        meta(_name="viewport", _content="width=device-width, initial-scale=1"),
        title("domonic Declarative Shadow DOM"),
        style("""
            body {
                margin: 2rem;
                background: #f6f8fa;
            }
            """),
    ),
    body(profile_card),
)

render(page, "declarative_shadow_dom.html")
print(page)
