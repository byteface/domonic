"""
    test_terminal
    ~~~~~~~~~~~~~~~~
"""

import unittest

from domonic.terminal import *
from domonic.decorators import silence


class domonicTestCase(unittest.TestCase):

    def test_bash_ls(self):
        files = ls()
        print(files)
        # return
        self.assertTrue('domonic' in ls())
        print(ls("-al"))
        print(ls("../"))
        for line in ls():
            print("line:", line)
        # for f in ls():
        #     try:
        #         print(f)
        #         print(cat(f))
        #     except Exception as e:
        #         pass

    def test_bash_pwd(self):
        thedir = pwd()
        print("OYI::", thedir)
        self.assertTrue('domonic' in thedir)

    def test_bash_cd(self):
        print(cd('../'))  # < CD does not run on terminal
        thedir_aftercd = pwd()
        print(thedir_aftercd)
        self.assertTrue('domonic' not in thedir_aftercd)
        print(cd('domonic'))
        thedir_aftercd = pwd()
        print(thedir_aftercd)
        self.assertTrue('domonic' in thedir_aftercd)

    def test_bash_mkdir(self):
        try:
            mkdir('somedir')
            self.assertTrue('somedir' in ls())
        except Exception as e:
            print(e)
        finally:
            # rm('-r somedir')
            rmdir('somedir')
            self.assertTrue('somedir' not in ls())

    def test_bash_touch(self):
        try:
            touch('somefile')
            self.assertTrue('somefile' in ls())
        except Exception as e:
            print(e)
        finally:
            rm('somefile')
            self.assertTrue('somefile' not in ls())

    @silence
    def test_bash_git(self):
        print(git('status'))
        self.assertTrue('master' in git('status'))

    def test_bash_general(self):
        print(man("ls"))
        print(echo('test'))
        print(df())
        print(du())
        print(ps())
        # print(cowsay('moo'))
        print(date())
        print(cal())
        for i, l in enumerate(cat('LICENSE.txt')):
            print(i, l)

    def test_bash_history(self):
        print(history())
        for i, thing in enumerate(history(), 1):
            print(i, thing)

    @silence
    def test_bash(self):
        print("ran")
        print(ping('http://eventual.technology'))  # < TODO - need to strean output
        # print(wget('eventual.technology'))


if __name__ == '__main__':
    unittest.main()
