"""Run: python -m examples.ssr.decorated_view (no web framework required)."""

from domonic import compiled
from domonic.dom import DOMConfig
from domonic.html import body, h1, html, p

DOMConfig.GLOBAL_AUTOESCAPE = True


@compiled
def home(name="World"):
    return html(body(h1("Hello"), p(name)))

def run(name="World"):
    return html(body(h1("Goodbye"), p(name)))


if __name__ == "__main__":
    print(home())
    print(home("Alice & Bob"))
    h = home()
    print(type(h)) # no longer a dom as not compiled
    test = run()
    print(type(test)) # still a dom as not compiled