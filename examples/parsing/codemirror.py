# -*- coding: utf-8 -*-

import sys

sys.path.insert(0, "../..")

import requests

from domonic import domonic
from domonic.utils import Utils
from domonic.html import *

from sanic import Sanic
from sanic import response
from sanic.response import json


page = lambda content: html(_lang="en", _class="no-js", _dir="auto").html(
    head(
        title("HTML 2 PYML CONVERTER"),
        # link(_rel="stylesheet", _href="/assets/css/styles.css"),
        script(_src="https://code.jquery.com/jquery-3.5.1.min.js"),
        link(_rel="stylesheet", _href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.52.2/codemirror.min.css"),
        script(
            _type="text/javascript", _src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.52.2/codemirror.min.js"
        ),
        script(
            _type="text/javascript",
            _src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.52.2/mode/python/python.min.js",
        ),
        link(_rel="stylesheet", _href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.52.2/theme/monokai.min.css"),
        script(
            """

        window.addEventListener('load', () => {

        var inp = CodeMirror(document.querySelector('#input'), {
            lineNumbers: true,
            tabSize: 4,
            value: '<html></html>'
           });

        var outp = CodeMirror(document.querySelector('#output'), {
                lineNumbers: true,
                tabSize: 4,
                mode: 'python',
                theme: 'monokai',
                value: 'html()'
            });


        function convert() {
            // use jquery to get the textarea content from input and post it to API then puts result in output

            //console.log(document.querySelector('#input').value);
            //console.log(inp.getValue());

            var input = inp.getValue(); //JSON.stringify(inp.getValue());
            var output = document.querySelector('#output');
            var data = input;


            $.ajax({ url: "/convert",
                type: "POST",
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                data: data , // pass that text to the server as a correct JSON String
                success: function (response) {     

                    //console.log(response)
                    //console.log(response.output)

                    //output.innerHTML = response.output;
                    outp.setValue(response.output);

                },
                error: function (type) { alert("ERROR!!" + type.responseText); }

            });
        }

        $('#convert').on( "click", function() {
            convert();
        });





        });



        """,
            _type="module",
        ),
    ),
    body(
        content,
        #   script(_src="/assets/js/script.js", _type="module")
    ),
)
# )

content = str(
    article(
        h1("HTML 2 PYML Converter!"),
        p("You can use this tool to convert html into pyml"),
        div(h5("html input:"), div(_id="input")),
        div(h5("pyml output:"), div(_id="output")),
        button("convert", _id="convert"),
    )
)


# render(page(content), "codemirror.html")

app = Sanic(name="HTML 2 PYML converter")
app.debug = True
# app.static('/assets', './assets')


@app.route("/")
async def index(request):
    outp = render(page(str(content)))
    return response.html(outp)


@app.route("/convert", methods=["GET", "POST"])
async def convert(request):

    data = request.body.decode("utf-8")
    print(data)

    code = data.strip('"').lstrip('"')

    output = domonic.parse(code)

    # output = domonic.evaluate(output)  # eval - should fix up params
    # render(page, 'tmp/'+Utils.url2file(SITE)+'.pyml') # write evaulated
    # outp = domonic.domonify(page)

    # print(output)
    return json({"output": output})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
