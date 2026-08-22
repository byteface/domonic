"""
test_collada
~~~~~~~~~~~~
"""

import unittest

from domonic.xml.collada import *


def _debug_print(*args, **kwargs):
    return None


class TestCase(unittest.TestCase):

    # @silence
    def test_domonic_collada(self):
        col = COLLADA()
        _debug_print(col)
        assert col.tag == "COLLADA"


if __name__ == "__main__":
    unittest.main()
