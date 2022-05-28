"""
    test_collada
    ~~~~~~~~~~~~
"""

import unittest

from domonic.xml.collada import *


class TestCase(unittest.TestCase):

    # @silence
    def test_domonic_collada(self):
        col = COLLADA()
        print(col)
        assert col.tag == "COLLADA"


if __name__ == "__main__":
    unittest.main()
