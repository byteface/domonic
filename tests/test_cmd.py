"""
test_cmd
~~~~~~~~~~~~~~~~
"""

import unittest
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from domonic.cmd import CmdException, Cmdcommand
from domonic.cmd import copy, del_, dir, erase, md, move, rd, rename, type_


class TestCase(unittest.TestCase):
    def test_cmd_dir_is_iterable_and_supports_cwd(self):
        with TemporaryDirectory(prefix="domonic cmd ") as tmp:
            sample = Path(tmp, "sample.txt")
            sample.write_text("hello", encoding="utf-8")

            files = dir(cwd=tmp)

            self.assertIn("sample.txt", str(files))
            self.assertIn("sample.txt", list(files))
            self.assertGreaterEqual(len(files), 1)

    def test_cmd_file_wrappers_work_cross_platform(self):
        with TemporaryDirectory(prefix="domonic cmd ") as tmp:
            source = Path(tmp, "source.txt")
            copied = Path(tmp, "copied.txt")
            moved = Path(tmp, "moved.txt")
            renamed = Path(tmp, "renamed.txt")
            folder = Path(tmp, "folder")
            source.write_text("hello\n", encoding="utf-8")

            copy(source, copied)
            self.assertEqual(copied.read_text(encoding="utf-8"), "hello\n")
            self.assertEqual(type_(copied).strip(), "hello")

            move(copied, moved)
            self.assertFalse(copied.exists())
            self.assertTrue(moved.exists())

            rename(moved.name, renamed.name, cwd=tmp)
            self.assertFalse(moved.exists())
            self.assertTrue(renamed.exists())

            erase(renamed)
            self.assertFalse(renamed.exists())

            md(folder)
            self.assertTrue(folder.is_dir())
            rd(folder)
            self.assertFalse(folder.exists())

            del_(source)
            self.assertFalse(source.exists())

    def test_cmd_run_helpers_and_decoded_errors(self):
        self.assertEqual(Cmdcommand.run("echo hello").strip(), "hello")
        self.assertEqual(
            Cmdcommand.run_args([sys.executable, "-c", "print('hello')"]).strip(),
            "hello",
        )

        with self.assertRaises(CmdException) as exc:
            Cmdcommand.run_args(
                [sys.executable, "-c", "import sys; print('bad'); sys.exit(7)"]
            )

        self.assertEqual(exc.exception.returncode, 7)
        self.assertIn("bad", exc.exception.output)


if __name__ == "__main__":
    unittest.main()
