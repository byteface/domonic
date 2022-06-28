import sys

sys.path.insert(0, "../..")

import os
import random
from dataclasses import asdict, dataclass, field
from json import load

from sanic import Sanic, response
from sanic_session import InMemorySessionInterface, Session

from domonic.CDN import *
from domonic.html import *

#  TO run this :
#  pip3 install sanic
#  pip3 install sanic-session

app = Sanic(name="Hangman")
app.static("/assets", "./assets")

session = Session(app, interface=InMemorySessionInterface())

# create a template
page_wrapper = lambda content: html(
    head(
        script(_src="https://code.jquery.com/jquery-3.5.1.min.js"),
        link(_rel="stylesheet", _type="text/css", _href=CDN_CSS.MVP),
        script(_type="text/javascript").html(
            """
                document.addEventListener('keydown', send_keypress);
                function send_keypress(event) {
                    $.get('/move?letter='+event.key, function(response){
                        $("#game").html(response);
                    });
                };
                """
        ),
    ),
    body(str(content)),
)


def get_word():
    wordArray = "Adult Aeroplane Air Aircraft Carrier Airforce Airport Album Alphabet Apple Arm Army Baby Baby Backpack Balloon Banana Bank Barbecue Bathroom Bathtub Bed Bed Bee Bible Bible Bird Bomb Book Boss Bottle Bowl Box Boy Brain Bridge Butterfly Button Cappuccino Car Carpet Carrot Cave Chair Chess Board Chief Child Chisel Chocolates Church Church Circle Circus Circus Clock Clown Coffee Comet Compact Disc Compass Computer Crystal Cup Cycle Data Base Desk Diamond Dress Drill Drink Drum Dung Ears Earth Egg Electricity Elephant Eraser Explosive Eyes Family Fan Feather Festival Film Finger Fire Floodlight Flower Foot Fork Freeway Fruit Fungus Game Garden Gas Gate Gemstone Girl Gloves God Grapes Guitar Hammer Hat Hieroglyph Highway Horoscope Horse Hose Ice Insect Jet fighter Junk Kaleidoscope Kitchen Knife Leather jacket Leg Library Liquid Magnet Man Map Maze Meat Meteor Microscope Milk Milkshake Mist Money $$$$ Monster Mosquito Mouth Nail Navy Necklace Needle Onion PaintBrush Pants Parachute Passport Pebble Pendulum Pepper Perfume Pillow Plane Planet Pocket Potato Printer Prison Pyramid Radar Rainbow Record Restaurant Rifle Ring Robot Rock Rocket Roof Room Rope Saddle Salt Sandpaper Sandwich Satellite School Sex Ship Shoes Shop Shower Signature Skeleton Slave Snail Software Solid Space Shuttle Spectrum Sphere Spice Spiral Spoon Spot Light Square Staircase Star Stomach Sun Sunglasses Surveyor Swimming Pool Sword Table Tapestry Teeth Telescope Television Tennis racquet Thermometer Tiger Toilet Tongue Torch Torpedo Train Treadmill Triangle Tunnel Typewriter Umbrella Vacuum Vampire Videotape Vulture Water Weapon Web Wheelchair Window Woman Worm".lower().split()
    word = random.choice(wordArray)
    return word


def display_hangman(tries):
    stages = [
        "  +---+\n  |   |\n  O   |\n /|\  |\n / \  |\n      |\n=========",
        "  +---+\n  |   |\n  O   |\n /|\  |\n /    |\n      |\n=========",
        "  +---+\n  |   |\n  O   |\n /|\  |\n      |\n      |\n=========",
        "  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========",
        "  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========",
        "  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========",
        "  +---+\n  |   |\n      |\n      |\n      |\n      |\n=========",
    ]
    return stages[tries]


@dataclass
class GameData:
    word: str = None
    guessed: bool = False
    guessed_letters: list = field(default_factory=list)
    guessed_words: list = field(default_factory=list)
    tries: int = 6


class Game:
    """Hangman. The data is stored on a session"""

    def __init__(self, request=None):
        self.state = GameData()
        if request is not None:
            if not request.ctx.session.get("game"):
                request.ctx.session["game"] = asdict(self.state)
            else:
                data = request.ctx.session.get("game")
                self.state.word = data["word"]
                self.state.guessed = data["guessed"]
                self.state.guessed_letters = data["guessed_letters"]
                self.state.guessed_words = data["guessed_words"]
                self.state.tries = data["tries"]


@app.route("/move")
async def move(request):
    game = Game(request)  # recover the game from the session
    guess = request.args["letter"][0]
    word_completion = "_" * len(game.state.word)

    board = div()
    if not game.state.guessed and game.state.tries > 0:
        if guess in game.state.guessed_letters:
            board.appendChild(div("You already guessed the letter ", guess))

        elif guess not in game.state.word:
            board.appendChild(div(b(guess), " is not in the word."))
            game.state.tries -= 1
            game.state.guessed_letters.append(guess)

        else:
            board.appendChild(div(f"You guessed the letter '{guess}' correctly!"))
            game.state.guessed_letters.append(guess)

            word_completion = list("_" * len(game.state.word))
            for i, w in enumerate(game.state.word):
                if w in game.state.guessed_letters:
                    word_completion[i] = w

            if "_" not in word_completion:
                game.state.guessed = True

    if game.state.guessed == True:
        board.appendChild(div("Nice one!, you guessed it. You win."))
    elif game.state.tries < 1:
        board.appendChild(div(f"Out of tries. The word was {game.state.word}. Maybe next time!"))

    page = div(
        div(f"Length of the word: {len(game.state.word)}"),
        div(f"Tries Left: {game.state.tries}"),
        pre(display_hangman(game.state.tries)),
    )

    word_completion = list("_" * len(game.state.word))
    for i, w in enumerate(game.state.word):
        if w in game.state.guessed_letters:
            word_completion[i] = w

    # TODO - div('To Play Again Type (Y/N)')
    page.appendChild(" ".join(word_completion))
    page.appendChild(board)
    request.ctx.session["game"] = asdict(game.state)  # update the session
    return response.html(str(main(str(page), _id="game")))


@app.route("/")
@app.route("/play")
async def play(request):

    # create a new game based on this session
    request.ctx.session["game"] = None
    game = Game(request)
    game.state.word = get_word()  # get a random word to start playing with
    request.ctx.session["game"] = asdict(game.state)

    intro = header(
        h1("HANGMAN!"), div("Can you guess the word? type a letter using the keyboard to guess."), main(_id="game")
    )
    return response.html(str(page_wrapper(intro)))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
