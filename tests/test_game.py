"""
test_game
~~~~~~~~~
"""

import unittest

from domonic.game import Game


class TestGame(unittest.TestCase):
    def test_pick_a_card_returns_standard_card(self):
        card = Game.pick_a_card()

        self.assertIn(
            card[:-1],
            {"2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"},
        )
        self.assertIn(card[-1], {"♠", "♥", "♦", "♣"})

    def test_deal_cards_returns_unique_cards(self):
        hand = Game.deal_cards(52)

        self.assertEqual(len(hand), 52)
        self.assertEqual(len(set(hand)), 52)

    def test_deal_cards_rejects_impossible_counts(self):
        with self.assertRaises(ValueError):
            Game.deal_cards(-1)
        with self.assertRaises(ValueError):
            Game.deal_cards(53)

    def test_random_bool_returns_bool(self):
        self.assertIsInstance(Game.random_bool(), bool)


if __name__ == "__main__":
    unittest.main()
