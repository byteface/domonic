import unittest
import subprocess
import os


class TestCLI(unittest.TestCase):
    def setUp(self):
        """Set up any required variables or files."""
        self.script_name = "domonic"

    def test_domonic_cli(self):
        """Test the basic CLI functionality."""
        url = "https://google.com"
        xpath_query = "//a"

        try:
            result = subprocess.run(
                [self.script_name, "-x", url, xpath_query],
                capture_output=True,
                text=True,
                check=True,
            )

            self.assertIn("google", result.stdout)
        except subprocess.CalledProcessError as e:
            self.fail(f"Command failed with error: {e.stderr}")

    def test_domonic_with_pipe(self):
        """Test CLI with piping."""
        url = "https://google.com"
        xpath_query = "//a"

        try:
            result = subprocess.run(
                f"{self.script_name} -x {url} {xpath_query} | uniq | sort",
                shell=True,
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertIn("google", result.stdout)
        except subprocess.CalledProcessError as e:
            self.fail(f"Command with pipe failed: {e.stderr}")


if __name__ == "__main__":
    unittest.main()
