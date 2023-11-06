import sys
sys.path.insert(0, "..")

from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from domonic.html import *
from domonic.CDN import CDN_CSS

app = FastAPI()

MARGIN = 1
PADDING = 2

# create a template
cell = lambda x=None: div(_class=x if x else "", _style=f"display:inline;margin:{MARGIN}px;padding:{PADDING}px;")

row = lambda *x: div(*x, _class="row")

# world grid
_grid = div(
    row(cell("d") / 100) / 100,
    row(cell("d") / 100) / 100,
    _class="container-fluid",
)

_materials = style(
    """
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

"""
)

_scripts = script(
    """
//alert('yo world!')
"""
)


class World:
    def __init__(self, request, *args, **kwargs):
        pass

    def __str__(self):
        return str(div(_materials, _scripts, _grid))


@app.get("/")
@app.get("/world", response_class=HTMLResponse)
async def world(request: Request):
    return Response(
        content=str(
            html(
                head(),
                body(
                    link(rel="stylesheet", type="text/css", href=CDN_CSS.BOOTSTRAP_4),
                    str(World(request)),
                ),
            )
        )
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
