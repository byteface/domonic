import sys
sys.path.insert(0, "..")

import datetime

from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from domonic.html import *
from domonic.components import Modal
from domonic.javascript import *
from domonic.CDN import CDN_CSS, CDN_JS

app = FastAPI()

MARGIN = 3
PADDING = 3
CELL_SIZE = 14
YEAR_LABEL_WIDTH = 22

DEFAULT_BIRTHDAY = "1970-01-01"
average_lifespan_in_years = 81  # used to build the years in the calendar

# create templates
cell = lambda x=None, *args: div(
    _class=x if x else "",
    _style=(
        f"display:inline-block;width:{CELL_SIZE}px;height:{CELL_SIZE}px;"
        f"margin:{MARGIN}px;padding:{PADDING}px;box-sizing:border-box;"
    ),
    **{"_aria-label": "Click to expand!"},
    **{"_data-balloon-pos": "up"},
    **{"_data-ref": "modalref"},
).html(*args)

row = lambda *x: div(*x, _class="life-row")

_materials = style(
    """
.body{
    counter-reset: age 0;
}
.life-calendar{
    display:inline-block;
}
.life-weeks{
    display:flex;
    align-items:center;
    gap:0;
    margin-left:0;
    padding-left:0;
}
.life-row{
    display:flex;
    align-items:center;
    gap:0;
    font-size:5px;
    line-height:1;
    counter-increment: age;
    position:relative;
    margin:0;
    padding:0;
    flex-wrap:nowrap;
}
.life-row:before{
    content:counter(age, decimal-leading-zero);
    display:inline-block;
    width:""" + str(YEAR_LABEL_WIDTH) + """px;
    margin-right:6px;
    text-align:right;
    font-size:10px;
    line-height:""" + str(CELL_SIZE + (PADDING * 2)) + """px;
    color:#333;
}
.week{
    background-color: white;
    width:""" + str(CELL_SIZE) + """px;
    min-width:""" + str(CELL_SIZE) + """px;
    margin:""" + str(MARGIN) + """px;
    padding:""" + str(PADDING) + """px;
    box-sizing:border-box;
    display:inline-flex;
    align-items:center;
    justify-content:center;
    font-size:10px;
    line-height:1;
}
.d{
    background-color: white; border: 1px solid black;
}
.d:hover{
    background-color: black; border: 1px solid red;
}
.g{
    background-color: #a90308; border: 1px solid white;
}
.g:hover{
    background-color: black; border: 1px solid red;
}
"""
)

_scripts = script(
    """
//alert('yo world!')
"""
)

class World:
    def __init__(self, request, age, *args, **kwargs):

        weeks = div(_class="life-weeks", _style=f"padding-left:{YEAR_LABEL_WIDTH + 6}px;")
        for count in range(1, 53):
            weeks += span(str(count).zfill(2), _class="week")

        years = []
        for count in range(average_lifespan_in_years):
            year = row()
            for countw in range(52):
                has_passed = ((count * 52) + countw) < Math.floor(self.get_weeks(age))
                year += cell("g open" if has_passed else "d open")  # , Char.CROSS if has_passed else '')
            years.append(year)

        self.grid = div(weeks, *years, _class="life-calendar")

    def get_weeks(self, BIRTHDAY=DEFAULT_BIRTHDAY):
        currentDate = datetime.datetime.now()
        BIRTHDATE = datetime.datetime.strptime(BIRTHDAY, "%Y-%m-%d")
        AGE = currentDate - BIRTHDATE
        weeks_old = AGE.days / 365 * 52
        return weeks_old

    def __str__(self):
        return str(div(_materials, _scripts, self.grid))


@app.get("/", response_class=HTMLResponse)
@app.get("/{age}", response_class=HTMLResponse)
async def world(request: Request, age: str = DEFAULT_BIRTHDAY):
    if request.url.path == '/favicon.ico':
        # Skip date parsing for favicon requests
        return Response(content='')

    def get_weeks(BIRTHDAY=DEFAULT_BIRTHDAY):
        currentDate = datetime.datetime.now()
        BIRTHDATE = datetime.datetime.strptime(BIRTHDAY, "%Y-%m-%d")
        AGE = currentDate - BIRTHDATE
        weeks_old = AGE.days / 365 * 52
        return weeks_old

    return HTMLResponse(
        str(
            html(
                head(
                    script(_src=CDN_JS.JQUERY),
                    link(_rel="stylesheet", _type="text/css", _href=CDN_CSS.BALLOON),
                    link(_rel="stylesheet", _type="text/css", _href=CDN_CSS.BOOTSTRAP),
                    link(_rel="stylesheet", _type="text/css", _href=CDN_CSS.MVP),
                    style(
                        """
                        .x-label{
                            writing-mode: vertical-rl;
                            display: inline-block;
                            position: absolute;
                            left: 10px;
                            margin: 0;
                        }
                        .y-label{
                            display: inline-block;
                            position: absolute;
                            left: 50px;
                        }
                        .calendar-shell{
                            top:110px;
                            left:50px;
                            position:absolute;
                        }
                    """
                    ),
                ),
                body(
                    Modal("modalref", div("Here is some content.", hr(), button("Add Data"))),
                    h1("Life Calendar 📅".upper(), _style="margin-left:5px;"),
                    div(
                        input(type="date"),
                        div(
                            h5("legend"),
                            div(div(_style="width:10px;height:10px;", _class="g"), "weeks spent"),
                            div(div(_style="width:10px;height:10px;", _class="d"), "weeks left"),
                            hr(),
                            h6("📅 : ", age),
                        ),
                        _style="position:absolute;top:0px;right:0px;",
                    ),
                    h5("Year of your life".upper(), _class="x-label", _style="top:120px;"),
                    h5("Week of the Year".upper(), _class="y-label"),
                    div(
                        str(World(request, age)),
                        _class="calendar-shell",
                    ),
                    script(
                        """
                        $(document).on( "click", ".close", function() {
                            var _id = $(this).data('ref');
                            $('#'+_id).css("display","none");
                        });
                        $(document).on( "click", ".open", function() {
                            var _id = $(this).data('ref');
                            $('#'+_id).css("display","block");
                        });
                        $('input[type=date]').change(function () {
                            //console.log(this.value);
                            window.location = '/'+this.value;
                        });
                        """
                    ),
                ),
            )
        )
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
