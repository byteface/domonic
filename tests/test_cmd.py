"""
    test_cmd
    ~~~~~~~~~~~~~~~~
"""

import unittest

from domonic.cmd import dir
from domonic.utils import Utils
# from domonic.decorators import silence


class TestCase(unittest.TestCase):

    def test_cmd_dir(self):
        if not Utils.is_windows():
            return

        files = dir()
        print(files)
        # return
        self.assertIn('domonic', str(dir()))

        try:
            print(dir("..\\"))  # notice requires 2 backslashes
        except Exception:
            # will fail on non windows
            pass

        for line in dir():
            print("line:", line)


if __name__ == '__main__':
    unittest.main()
