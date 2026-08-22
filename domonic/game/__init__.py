"""
domonic.game
====================================

"""

import random

_random = random.SystemRandom()


class Game:
    @staticmethod
    def roll_dice(sides=6) -> int:
        """Roll a die with the requested number of sides.

        Args:
            sides: Number of sides on the die. Defaults to ``6``.

        Returns:
            A random integer between ``1`` and ``sides``.
        """
        return _random.randint(1, sides)

    @staticmethod
    def pick_a_card() -> str:
        """Select a random card label from a standard deck.

        Returns:
            A card string such as ``"A♠"``.
        """
        suits = ["♠", "♥", "♦", "♣"]
        cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        return _random.choice(cards) + _random.choice(suits)

    @staticmethod
    def deal_cards(n: int = 1) -> list:
        """Deal a list of random card labels.

        Args:
            n: Number of cards to deal. Defaults to ``1``.

        Returns:
            A list of card strings.
        """
        return [
            Game.pick_a_card() for _ in range(n)
        ]  # TODO - this could have duplicates

    @staticmethod
    def random_bool() -> bool:
        #  (https://6b.eleuther.ai/) TODO - test
        return bool(_random.getrandbits(1))

    @staticmethod
    def random_char() -> str:
        return chr(_random.choice(range(ord("A"), ord("Z") + 1)))

    # @staticmethod
    # def bingo():
    # calls=["Kelly's Eye","One Little Duck","Cup of Tea","Knock at the Door","Man Alive","Half a Dozen","Lucky Seven","Garden Gate","Doctor's Order","Prime Minister's Den","Legs Eleven","One Dozen","Unlucky for Some","Valentine's Day","Young and Keen","Sweet Sixteen and Never Been Kissed","Dancing Queen","Coming of Age","Goodbye Teens","One Score","Key of the Door","Two Little Ducks","Thee and Me","Two Dozen","Duck and Dive","Pick and Mix","Gateway to Heaven","In a State","Rise and Shine","Dirty Gertie","Get up and Run","Buckle my Shoe","Fish, Chips and Peas","Ask for More","Jump and Jive","Three Dozen","More than Eleven","Christmas Cake","39 Steps","Life Begins","Time for Fun","Winnie-the-Pooh","Down on your Knees","Droopy Drawers","Halfway There","Up to Tricks","Four and Seven","Four Dozen","PC","Half a Centry","Tweak of the Thumb","Danny La Rue","Stuck in a Tree","Clean the Floor","Snakes Alive","Shotts Bus","Heinz Varieties","Make them Wait","Brighton Line","Five Dozen","Baker's Bun","Tickety-Boo","Tickle Me Sixty Three","Red Raw","Old Age Pension","Clickety Click","Stairway to Heaven","Saving Grace","Favourite of Mine","Three Score and Ten","Bang on the Drum","Six Dozen","Queen Bee","Hit the Floor","Strive and Strive","Trombones","Sunset Strip","39 More Steps","One More Time","Eight and Blank","Stop and Run","Straight on Through","Time for Tea","Seven Dozen","Staying Alive","Between the Sticks","Torquay in Devon","Two Fat Ladies","Nearly There","Top of the Shop"]
    # index = Math.random()*len(calls)
    # return calls[index], index+1

    # @staticmethod
    # def random_name():

    # @staticmethod
    # def random_address():
