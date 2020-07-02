"""
    test_terminal
    ~~~~~~~~~~~~~~~~
"""

import unittest
from domonic.terminal import *


class domonicTestCase(unittest.TestCase):

    def test_bash_ls(self):
        # ls = ls()
        print(ls())
        # print(ls("-al"))
        # print(ls("../"))

        print(pwd())
        print(cd('../'))  # < TODO - will need custom
        # print(cd('archive'))
        # print('---',pwd())

        # print(mkdir('somedir'))
        # print(touch('somefile'))

        # print(git('status'))

        # for file in ls( "-al" ):
        #     print("LINE:",file)

        # for f in ls():
        #     try:
        #         print(f)
        #         print(cat(f))
        #     except Exception as e:
        #         pass

        # for i, l in enumerate(cat('LICENSE.txt')):
        #     print(i,l)

        # for l in history(): # print('ls'.l) # TODO

        # print(history())
        # print(man("ls"))
        # print(echo('test'))
        # print(df())
        # print(du())

        # for thing in du():
        #     print(thing)

        # print(find('.'))
        # print(ping('eventual.technology'))# < TODO - need to strean output
        # print(cowsay('moo'))
        # print(wget('eventual.technology'))
        print(date())
        print(cal())


if __name__ == '__main__':
    unittest.main()
