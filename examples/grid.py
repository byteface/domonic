import sys

sys.path.insert(0, "..")

from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from domonic.html import *
from domonic.CDN import CDN_CSS

app = FastAPI()

MARGIN = 1
PADDING = 2
CELL_SIZE = 8
ROWS = 100
COLS = 100

# create a template
cell = lambda x=None: div(
    _class=x if x else "",
    _style=(
        f"display:inline-block;"
        f"width:{CELL_SIZE}px;height:{CELL_SIZE}px;"
        f"margin:{MARGIN}px;padding:{PADDING}px;"
        "box-sizing:border-box;"
    ),
)

row = lambda *x: div(*x, _class="row")

# world grid
_grid = div(
    *[row(*[cell("d") for _ in range(COLS)]) for _ in range(ROWS)],
    _class="container-fluid",
)

_materials = style("""
/* default */
.d{
	background-color: black;
}
.g{
	background-color: green;
}
.r{
	background-color: red;
}
.b{
	background-color: blue;
}
.y{
	background-color: yellow;
}
.p{
	background-color: purple;
}

""")

_scripts = script("""
//alert('yo world!')
""")


class World:
    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.rows = kwargs.get("rows", ROWS)
        self.cols = kwargs.get("cols", COLS)

    def __str__(self):
        grid = _grid
        if self.rows != ROWS or self.cols != COLS:
            grid = div(
                *[
                    row(*[cell("d") for _ in range(self.cols)])
                    for _ in range(self.rows)
                ],
                _class="container-fluid",
            )
        return str(div(_materials, _scripts, grid))


@app.get("/")
@app.get("/world", response_class=HTMLResponse)
async def world(request: Request):
    return Response(
        content=str(
            html(
                head(),
                body(
                    link(_rel="stylesheet", _type="text/css", _href=CDN_CSS.BOOTSTRAP),
                    str(World(request)),
                ),
            )
        )
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
