import sys
sys.path.insert(0, '..')

import os
import datetime

from sanic import Sanic
from sanic import response
from domonic.html import *
from domonic.javascript import *
from domonic.CDN import *
from domonic.dQuery import º

from domonic.components import Modal
# from domonic.constants.color import *
# from domonic.constants.entities import Char

app = Sanic(name='📅 Life Calendar')
app.static('/assets', './assets')

MARGIN = 3
PADDING = 3

DEFAULT_BIRTHDAY = '1970-01-01'
average_lifespan_in_years = 81  # used to build the years in calendar

# create templates
cell = lambda x=None, *args: div(_class=x if x else '', _style=f"display:inline;margin:{MARGIN}px;padding:{PADDING}px;",
                **{"_aria-label": "Click to expand!"}, **{"_data-balloon-pos": "up"},
                **{"_data-ref": "modalref"}).html(
                *args
            )

row = lambda *x: div(*x, _class="row")

_materials = style("""
.body{
    counter-reset: age 0;
}
.row{
    font-size:5px;
    counter-increment: age;
}
.row:before{
    content:counter(age, decimal-leading-zero);
    position:absolute; left:0; text-align:right;
}
.week{
    background-color: white;
    padding:4px; width:14px;
    display:inline-block;
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
""")

_scripts = script("""
//alert('yo world!')
""")


class World(object):
    def __init__(self, request, age, *args, **kwargs):

        weeks = div(_style="margin-left:-14px;")
        for count in range(1, 53):
            weeks += span(str(count).zfill(2), _style="font-size:5px;", _class='week')

        years = []
        for count in range(average_lifespan_in_years):
            year = row()
            for countw in range(52):
                has_passed = ((count * 52) + countw) < Math.floor(self.get_weeks(age))
                year += cell('g open' if has_passed else 'd open')  # , Char.CROSS if has_passed else '')
            years.append(year)

        self.grid = div(
            weeks,
            *years,
            _class="container-fluid"
        )

    def get_weeks(self, BIRTHDAY=DEFAULT_BIRTHDAY):
        currentDate = datetime.datetime.now()
        BIRTHDATE = datetime.datetime.strptime(BIRTHDAY, '%Y-%m-%d')
        AGE = currentDate - BIRTHDATE
        weeks_old = AGE.days / 365 * 52
        return weeks_old

    def __str__(self):
        return str(
            div(
                _materials,
                _scripts,
                self.grid
            )
        )


@app.route('/')
@app.route('/<age>')
async def world(request, age=DEFAULT_BIRTHDAY):
    # check the diffs against our diff map
    return response.html(str(html(
            head(
                script(_src="https://code.jquery.com/jquery-3.5.1.min.js"),
                link(_rel="stylesheet", _type="text/css", _href=CDN_CSS.BALLOON),
                link(_rel="stylesheet", _type="text/css", _href=CDN_CSS.BOOTSTRAP_4),
                link(_rel="stylesheet", _type="text/css", _href=CDN_CSS.MVP),
                style("""
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
                """)
            ),
            body(
                Modal('modalref', div("Here is some content.", br(), button("Add Data"))),
                h1('Life Calendar 📅'.upper(), _style="margin-left:5px;"),
                div(
                    input(_type="date"),
                    div(
                        h5('legend'),
                        div(div(_style="width:10px;height:10px;", _class='g'), "weeks spent"),
                        div(div(_style="width:10px;height:10px;", _class='d'), "weeks left"),
                        hr(),
                        h6("📅 : ", age)
                    ),
                    _style="position:absolute;top:0px;right:0px;"
                ),
                h5("Year of your life".upper(), _class="x-label", _style="top:120px;"),
                h5("Week of the Year".upper(), _class="y-label"),
                div(str(World(request, age)), 
                    _class="container-fluid", _style="top:110px;left:50px;position:absolute;"),
                script("""
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
                """),
            ))))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
