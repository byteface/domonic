"""
    test_terminal
    ~~~~~~~~~~~~~~~~
"""

import unittest

from domonic.decorators import silence
from domonic.terminal import *


class TestCase(unittest.TestCase):
    def test_bash_ls(self):
        files = ls()
        # print(files)
        assert "domonic" in files
        # return
        self.assertIn("domonic", ls())
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
        # print("OYI::", thedir)
        self.assertIn("domonic", thedir)

    def test_command_core_helpers(self):
        self.assertEqual(echo("hello", "world").strip(), "hello world")
        self.assertEqual(command.run_args(["printf", "hello world"]), "hello world")

        files = ls()
        self.assertGreater(len(files), 0)
        self.assertIn("domonic", files)
        self.assertIn("domonic", list(files))

    def test_command_errors_are_decoded(self):
        with self.assertRaises(TerminalException) as exc:
            command.run_args(["ls", "__domonic_missing_file__"])

        self.assertIsInstance(exc.exception.output, str)
        self.assertIn("__domonic_missing_file__", str(exc.exception))

    def test_wait_command_timeout_returns_partial_output(self):
        sleeper = type("sleeper", (command,), {"name": "sleep", "wait": True, "iterable": True})
        result = sleeper("1", timeout=0.01)
        self.assertEqual(str(result), "")

    def test_bash_cd(self):
        pass  # TODO - need to change github action
        # print(cd('../'))  # < CD does not run on terminal
        # thedir_aftercd = pwd()
        # print(thedir_aftercd)
        # self.assertTrue('domonic' not in thedir_aftercd)
        # print(cd('domonic'))
        # thedir_aftercd = pwd()
        # print(thedir_aftercd)
        # self.assertTrue('domonic' in thedir_aftercd)

    def test_bash_mkdir(self):
        try:
            mkdir("somedir")
            self.assertIn("somedir", ls())
        except Exception as e:
            print(e)
        finally:
            # rm('-r somedir')
            rmdir("somedir")
            self.assertTrue("somedir" not in ls())

    def test_bash_touch(self):
        try:
            touch("somefile")
            self.assertTrue("somefile" in ls())
        except Exception as e:
            print(e)
        finally:
            rm("somefile")
            self.assertTrue("somefile" not in ls())

    def test_bash_mv(self):
        try:
            touch("somefile")
            mv("somefile temp")
        except Exception as e:
            print(e)
        finally:
            self.assertTrue("somefile" not in ls())
            self.assertTrue("temp" in ls())
            rm("temp")

    def test_bash_cp(self):
        try:
            touch("somefile")
            cp("somefile temp")
        except Exception as e:
            print(e)
        finally:
            self.assertTrue("temp" in ls())
            rm("somefile")
            rm("temp")

    @silence
    def test_bash_git(self):
        # print(git('status'))
        self.assertIn("master", git("status"))

    def test_bash_general(self):
        print(man("ls"))
        print(echo("test"))
        print(df())
        print(du())
        try:
            print(ps())
        except TerminalException as exc:
            if "Operation not permitted" in str(exc):
                self.skipTest("ps is not permitted in this sandbox")
            raise
        # print(cowsay('moo'))
        print(date())
        # print(cal())
        # failing on github actions
        # for i, l in enumerate(cat('LICENSE.txt')):
        # print(i, l)

    def test_bash_history(self):
        pass  # failing on github actions
        # print(history())
        # for i, thing in enumerate(history(), 1):
        # print(i, thing)

    @silence
    def test_bash(self):
        print("ran")
        print(ping("https://www.google.com"))  # < TODO - need to strean output
        # print(wget('eventual.technology'))


if __name__ == "__main__":
    unittest.main()
