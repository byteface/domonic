"""Run from the repository root: python -m examples.ssr.compiled_views."""

from types import SimpleNamespace
from contextlib import asynccontextmanager
from pathlib import Path
import os

from domonic import compile
from domonic.dom import DOMConfig
from domonic.html import (
    article,
    div,
    h1,
    h2,
    li,
    p,
    ul,
    html,
    head,
    title,
    body,
    a,
    form,
    input,
    button,
    raw,
)


def profile(user):
    return div(h1("Profile"), p(user.name, _class="bio"))


def medium(user, items):
    return article(
        h1("Your dashboard"),
        p(user.name, _class="welcome"),
        ul([li(item, _class="entry") for item in items]),
        _id="dashboard",
    )


def large(groups):
    return div(
        [
            article(h2(title), ul([li(item) for item in items]), _class="group")
            for title, items in groups
        ],
        _class="directory",
    )


# An application-specific, private directory; reused across server restarts.
CACHE_DIR = Path("/tmp") / f"domonic-ssr-example-{os.getuid()}"


def home(name, trusted_notice):
    return html(
        head(title("Compiled domonic SSR")),
        body(
            h1("Compiled before the first request"),
            p("Normal text is escaped: ", name),
            div(raw(trusted_notice)),
            form(
                input(_name="name", _value=name), button("Render again"), _method="get"
            ),
            ul(
                li(a("Profile", _href="/profile?name=Alice%20%26%20Bob")),
                li(a("Dashboard", _href="/dashboard")),
                li(a("Large tree", _href="/large")),
            ),
        ),
    )


def create_app(cache_dir=CACHE_DIR):
    # Optional server dependencies are imported here so the benchmark can still
    # import the view functions without importing a web framework.
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse

    @asynccontextmanager
    async def lifespan(app):
        DOMConfig.GLOBAL_AUTOESCAPE = True
        # Uvicorn waits for lifespan startup to finish before serving ANY route.
        # No view is rendered here and no first request is needed to warm it up.
        app.state.renderers = {
            view.__name__: compile(view, strict=True, cache_dir=cache_dir)
            for view in (home, profile, medium, large)
        }
        for name, renderer in app.state.renderers.items():
            print(
                f'{name}: ready (disk cache {"hit" if renderer.cache_hit else "miss"})'
            )
        yield

    app = FastAPI(title="Compiled domonic SSR", lifespan=lifespan)

    @app.get("/", response_class=HTMLResponse)
    async def index(name: str = "Alice & Bob <visitors>"):
        # raw() is used only for this application-owned markup, never the query.
        trusted_notice = "<strong>This notice is explicitly trusted HTML.</strong>"
        return app.state.renderers["home"](name, trusted_notice)

    @app.get("/profile", response_class=HTMLResponse)
    async def profile_route(name: str = "Alice & Bob"):
        return app.state.renderers["profile"](SimpleNamespace(name=name))

    @app.get("/dashboard", response_class=HTMLResponse)
    async def dashboard_route(name: str = "Alice & Bob"):
        return app.state.renderers["medium"](
            SimpleNamespace(name=name), ["First item", "Second item", "Third item"]
        )

    @app.get("/large", response_class=HTMLResponse)
    async def large_route():
        groups = [(f"Group {i}", [f"Item {j}" for j in range(50)]) for i in range(100)]
        return app.state.renderers["large"](groups)

    return app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(create_app(), host="127.0.0.1", port=8000)
