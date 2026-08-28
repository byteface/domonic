import unittest
from unittest.mock import patch

from domonic.lerpy.easing import Linear
from domonic.lerpy.tween import Tween


class TestCase(unittest.TestCase):
    def test_tween_pause_offsets_elapsed_time(self):
        target = {"x": 0}
        tween = Tween(target, {"x": 100}, 10, Linear.easeNone)
        for value in tween._values:
            value.start = target[value.prop]
            value.change = value.target - value.start
        tween._timeStart = 0
        tween._timePaused = 0
        tween._timePrevious = 0
        tween._tweening = True

        self.assertTrue(tween.tweening)

        with patch("domonic.lerpy.tween.get_timer", return_value=4):
            tween._update(None)
        self.assertEqual(target["x"], 40)

        with patch("domonic.lerpy.tween.get_timer", return_value=4.5):
            tween.pause()
        with patch("domonic.lerpy.tween.get_timer", return_value=8.5):
            tween.unpause()
        with patch("domonic.lerpy.tween.get_timer", return_value=9):
            tween._update(None)

        self.assertEqual(target["x"], 50)


if __name__ == "__main__":
    unittest.main()
