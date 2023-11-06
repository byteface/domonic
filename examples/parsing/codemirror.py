# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "../..")

import requests

from domonic.utils import Utils
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from domonic import domonic
from domonic.html import *

app = FastAPI()

page = lambda content: html(_lang="en", _class="no-js", _dir="auto").html(
    head(
        title("HTML 2 PYML CONVERTER"),
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
                    var input = inp.getValue();
                    fetch("/convert", {
                        method: "POST",
                        body: JSON.stringify({ data: input }),
                        headers: {"Content-Type": "application/json"}
                    })
                    .then(response => response.json())
                    .then(data => outp.setValue(data.output))
                    .catch(error => alert("ERROR!! " + error));
                }

                $('#convert').on("click", function() {
                    convert();
                });
            });
            """,
            _type="module",
        ),
    ),
    body(content),
)

content = str(
    article(
        h1("HTML 2 PYML Converter!"),
        p("You can use this tool to convert HTML into PYML"),
        div(h5("HTML input:"), div(_id="input")),
        div(h5("PYML output:"), div(_id="output")),
        button("convert", _id="convert"),
    )
)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    outp = render(page(str(content)))
    return HTMLResponse(content=outp)

@app.post("/convert", response_class=JSONResponse)
async def convert(data: dict):
    code = data.get("data").strip('"').lstrip('"')
    output = domonic.parse(code)
    return {"output": output}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
