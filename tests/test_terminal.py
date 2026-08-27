"""
test_terminal
~~~~~~~~~~~~~~~~
"""

import os
import unittest
from tempfile import TemporaryDirectory

from domonic.decorators import silence
from domonic.terminal import *


class TestCase(unittest.TestCase):
    def test_bash_ls(self):
        files = ls()
        # print(files)
        assert "domonic" in files
        # return
        self.assertIn("domonic", ls())
        self.assertIn("domonic", ls("-al"))
        self.assertGreater(len(list(ls())), 0)
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
        sleeper = type(
            "sleeper", (command,), {"name": "sleep", "wait": True, "iterable": True}
        )
        result = sleeper("1", timeout=0.01)
        self.assertEqual(str(result), "")

    def test_bash_cd(self):
        old_cwd = os.getcwd()
        with TemporaryDirectory() as tmp:
            try:
                cd(tmp)
                self.assertEqual(os.path.realpath(os.getcwd()), os.path.realpath(tmp))
                self.assertEqual(os.path.realpath(pwd().strip()), os.path.realpath(tmp))
            finally:
                os.chdir(old_cwd)

    def test_bash_mkdir(self):
        with TemporaryDirectory() as tmp:
            mkdir("somedir", cwd=tmp)
            self.assertIn("somedir", ls(cwd=tmp))
            rmdir("somedir", cwd=tmp)
            self.assertTrue("somedir" not in ls(cwd=tmp))

    def test_bash_touch(self):
        with TemporaryDirectory() as tmp:
            touch("somefile", cwd=tmp)
            self.assertTrue("somefile" in ls(cwd=tmp))
            rm("somefile", cwd=tmp)
            self.assertTrue("somefile" not in ls(cwd=tmp))

    def test_bash_mv(self):
        with TemporaryDirectory() as tmp:
            touch("somefile", cwd=tmp)
            mv("somefile temp", cwd=tmp)
            self.assertTrue("somefile" not in ls(cwd=tmp))
            self.assertTrue("temp" in ls(cwd=tmp))
            rm("temp", cwd=tmp)

    def test_bash_cp(self):
        with TemporaryDirectory() as tmp:
            touch("somefile", cwd=tmp)
            cp("somefile temp", cwd=tmp)
            self.assertTrue("temp" in ls(cwd=tmp))
            rm("somefile", cwd=tmp)
            rm("temp", cwd=tmp)

    @silence
    def test_bash_git(self):
        # print(git('status'))
        self.assertIn("master", git("status"))

    def test_bash_general(self):
        self.assertIn("LS", man("ls").upper())
        self.assertEqual(echo("test").strip(), "test")
        self.assertTrue(str(df()).strip())
        self.assertTrue(str(du("-s .")).strip())
        try:
            self.assertTrue(str(ps()).strip())
        except TerminalException as exc:
            if "Operation not permitted" in str(exc):
                self.skipTest("ps is not permitted in this sandbox")
            raise
        # print(cowsay('moo'))
        self.assertTrue(str(date()).strip())
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
        self.assertEqual(command.run_args(["printf", "ran"]), "ran")


if __name__ == "__main__":
    unittest.main()
