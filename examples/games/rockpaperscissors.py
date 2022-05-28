# -*- coding: utf-8 -*-
# NOTICE THE ENCODING TO ALLOW THE FUNNY CHARS!

import sys

sys.path.insert(0, "../..")

import random
from sanic import Sanic, response

from domonic.html import *
from domonic.CDN import *
from domonic.utils import *
from domonic.constants.entities import Char

#  To run this first:
#  pip3 install sanic

app = Sanic(name="paper_scissors_rock")
app.static("/assets", "./assets")

# create a template
page_wrapper = lambda content: html(
    head(
        script(_src="https://code.jquery.com/jquery-3.5.1.min.js"),
        link(_rel="stylesheet", _type="text/css", _href=CDN_CSS.MVP),
        script(_type="text/javascript").html(
            """
                document.addEventListener('keydown', send_keypress);
                function send_keypress(event) {
                    var choice = "";
                    if( event.key == 'r' || event.key == 'R' ){
                        choice="✊";
                    }
                    if( event.key == 'p' || event.key == 'P' ){
                        choice="✋";
                    }
                    if( event.key == 's' || event.key == 'S' ){
                        choice="✌";
                    }
                    $.get('/move?choice='+choice, function(response){
                        $("#game").html(response);
                    });
                };
                """
        ),
    ),
    body(str(content)),
)


choices = ["✊", "✋", "✌"]


def get_choice():
    choice = random.choice(choices)
    return choice


@app.route("/move")
async def move(request):
    choice = Utils.escape(request.args["choice"][0])
    computer = get_choice()

    page = div()
    board = div()

    result = lambda u, c, r: board.appendChild(
        div(f"You chose {u} ", Char.NBSP, f" I chose {c} ", h4(f"{r}", _id="result"))
    )

    if choice == "✊":
        if computer == "✊":
            result("✊", "✊", "Draw!")
        elif computer == "✋":
            result("✊", "✋", "I win. You lose!")
        elif computer == "✌":
            result("✊", "✌", "I lose. You win!")

    elif choice == "✋":
        if computer == "✋":
            result("✋", "✋", "Draw!")
        elif computer == "✊":
            result("✋", "✊", "I lose. You win!")
        elif computer == "✌":
            result("✋", "✌", "I win. You lose!")

    elif choice == "✌":
        if computer == "✌":
            result("✌", "✌", "Draw!")
        elif computer == "✊":
            result("✌", "✊", "I win. You lose!")
        elif computer == "✋":
            result("✌", "✋", "I lose. You win!")

    page.appendChild(board)
    return response.html(str(main(str(page), _id="game")))


@app.route("/")
@app.route("/play")
async def play(request):
    intro = header(
        h1("✊✋✌!"),
        h2("Wanna play?"),
        div("type 'r' for Rock ✊", br(), "'p' for Paper ✋", br(), "Or 's' for Scissors ✌"),
        main(_id="game"),
    )
    return response.html(str(page_wrapper(intro)))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
