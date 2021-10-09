"""
    test_cmd
    ~~~~~~~~~~~~~~~~
"""

import unittest

from domonic.cmd import dir
# from domonic.decorators import silence


class TestCase(unittest.TestCase):

    def test_cmd_dir(self):
        files = dir()
        print(files)
        # return
        self.assertTrue('domonic' in str(dir()))

        try:
            print(dir("..\\"))  # notice requires 2 backslashes
        except Exception:
            # will fail on non windows
            pass

        for line in dir():
            print("line:", line)


if __name__ == '__main__':
    unittest.main()
