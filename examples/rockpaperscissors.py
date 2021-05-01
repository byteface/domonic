# -*- coding: utf-8 -*-
# NOTICE THE ENCODING TO ALLOW THE FUNNY CHARS!

import sys
sys.path.insert(0, '..')

import os
import random
from json import load
from dataclasses import dataclass, asdict, field
from sanic import Sanic
from sanic import response

from domonic.html import *
from domonic.CDN import *
from domonic.utils import *

from domonic.constants.color import Color
print(Color.rgb2hex(0,0,0))

from domonic.constants.entities import Char
print(Char.NBSP)

#  To run this first:
#  pip3 install sanic

app = Sanic(name='✊✋✌')
app.static('/assets', './assets')

# create a template
page_wrapper = lambda content : html(
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
                )
            ),
            body(
                str(content)
            ))


choices = ['✊', '✋', '✌']
def get_choice():
    # TODO - put a learning algo in here per user? rather than just random. 
    # try to read their mind or second guess based on previous games.
    choice = random.choice(choices)
    return choice


@app.route('/move')
async def move(request):
    choice = Utils.escape(request.args['choice'][0])
    computer = get_choice()

    page = div()
    board = div()

    result = lambda u, c, r : board.appendChild( div( f'You chose {u} ', Char.NBSP, f' I chose {c} ', h4( f'{r}', _id="result")) )

    # when py3.10 comes out see if this works
    # match choice:
    #     case "✊":
    #         match computer:
    #             case '✊': result('✊','✊','Draw')
    #             case '✋': result('✊','✋','I lose')
    #             case '✌': result('✊','✌','I win') )
    #     case "✋":
    #         match computer:
    #             case '✊': result('✋','✊','I win')
    #             case '✋': result('✋','✋','Draw')
    #             case '✌': result('✋','✌','I lose')
    #     case "✌":
    #         match computer:
    #             case '✊': result('✌','✊','I win')
    #             case '✋': result('✌','✋','I lose')
    #             case '✌': result('✌','✌','Draw')


    print(choice == '✊')

    if choice == "✊":
            if computer=='✊': result('✊','✊','Draw!')
            if computer=='✋': result('✊','✋','I win. You lose!')
            if computer=='✌': result('✊','✌','I lose. You win!')

    if choice == "✋":
            if computer=='✋': result('✋','✋','Draw!')
            if computer=='✊': result('✋','✊','I lose. You win!')
            if computer=='✌': result('✋','✌','I win. You lose!')
        
    if choice == "✌":
            if computer=='✌': result('✌','✌','Draw!')
            if computer=='✊': result('✌','✊','I win. You lose!')
            if computer=='✋': result('✌','✋','I lose. You win!')

    page.appendChild(board)
    return response.html(str(main( str(page), _id="game")))


@app.route('/')
@app.route('/play')
async def play(request):
    intro = header(
        h1("✊✋✌!"),
        h2("Wanna play?"),
        div( "type 'r' for Rock ✊", br(), "'p' for Paper ✋", br(), "Or 's' for Scissors ✌"),
        main(_id="game")
    )
    return response.html(str(page_wrapper(intro)))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
