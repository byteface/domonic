import io
import sys
import tempfile
import unittest
from argparse import Namespace
from contextlib import redirect_stdout
from unittest.mock import MagicMock, patch

from domonic.__main__ import do_things, project


class TestCLI(unittest.TestCase):
    def _base_args(self, **overrides):
        args = Namespace(
            help=False,
            version=False,
            project=None,
            eval=None,
            assets=False,
            download=None,
            xpath=None,
            query=None,
            xpath_file=None,
            query_file=None,
            xpath_stdin=None,
            query_stdin=None,
            text=False,
            attr=None,
            count=False,
            first=False,
            parser=None,
            html2pyml=None,
            server=None,
        )
        for key, value in overrides.items():
            setattr(args, key, value)
        return args

    def test_xpath_cli_outputs_nodes(self):
        mocked_nodes = ["<a href='https://example.com'>Example</a>"]
        mocked_result = MagicMock(nodes=mocked_nodes)
        mocked_expression = MagicMock()
        mocked_expression.evaluate.return_value = mocked_result
        mocked_evaluator = MagicMock()
        mocked_evaluator.createExpression.return_value = mocked_expression
        fake_requests = MagicMock()
        fake_requests.get.return_value.text = (
            "<html><body><a href='https://example.com'>Example</a></body></html>"
        )

        with (
            patch.dict(sys.modules, {"requests": fake_requests}),
            patch("domonic.domonic.parseString", return_value=object()) as mock_parse,
            patch("domonic.webapi.xpath.XPathEvaluator", return_value=mocked_evaluator),
            redirect_stdout(io.StringIO()) as stdout,
        ):
            do_things(
                self._base_args(
                    xpath=["https://example.com", "//a"],
                    parser="selectolax",
                )
            )

        fake_requests.get.assert_called_once_with("https://example.com", timeout=30)
        mock_parse.assert_called_once_with(
            "<html><body><a href='https://example.com'>Example</a></body></html>",
            parser="selectolax",
        )
        mocked_evaluator.createExpression.assert_called_once_with("//a")
        self.assertIn("Example", stdout.getvalue())

    def test_query_cli_outputs_matching_nodes(self):
        fake_document = MagicMock()
        fake_document.querySelectorAll.return_value = [
            "<a class='cta'>Call to action</a>"
        ]
        fake_requests = MagicMock()
        fake_requests.get.return_value.text = (
            "<html><body><a class='cta'>Call to action</a></body></html>"
        )

        with (
            patch.dict(sys.modules, {"requests": fake_requests}),
            patch(
                "domonic.domonic.parseString", return_value=fake_document
            ) as mock_parse,
            redirect_stdout(io.StringIO()) as stdout,
        ):
            do_things(
                self._base_args(
                    query=["https://example.com", ".cta"],
                    parser="selectolax",
                )
            )

        fake_requests.get.assert_called_once_with("https://example.com", timeout=30)
        mock_parse.assert_called_once_with(
            "<html><body><a class='cta'>Call to action</a></body></html>",
            parser="selectolax",
        )
        fake_document.querySelectorAll.assert_called_once_with(".cta")
        self.assertIn("Call to action", stdout.getvalue())

    def test_query_file_cli_supports_attr_and_first(self):
        fake_node = MagicMock()
        fake_node.href = "https://example.com/docs"
        fake_page = MagicMock()
        fake_page.querySelectorAll.return_value = [
            fake_node,
            MagicMock(href="https://example.com/ignored"),
        ]

        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as handle:
            handle.write(
                "<html><body><a href='https://example.com/docs'>Docs</a></body></html>"
            )
            file_path = handle.name

        try:
            with (
                patch(
                    "domonic.domonic.parseString", return_value=fake_page
                ) as mock_parse,
                redirect_stdout(io.StringIO()) as stdout,
            ):
                do_things(
                    self._base_args(
                        query_file=[file_path, "a"],
                        attr="href",
                        first=True,
                        parser="selectolax",
                    )
                )
        finally:
            import os

            os.unlink(file_path)

        fake_page.querySelectorAll.assert_called_once_with("a")
        mock_parse.assert_called_once_with(
            "<html><body><a href='https://example.com/docs'>Docs</a></body></html>",
            parser="selectolax",
        )
        self.assertEqual(stdout.getvalue().strip(), "https://example.com/docs")

    def test_xpath_stdin_cli_supports_count(self):
        mocked_result = MagicMock(nodes=["<a>One</a>", "<a>Two</a>"])
        mocked_expression = MagicMock()
        mocked_expression.evaluate.return_value = mocked_result
        mocked_evaluator = MagicMock()
        mocked_evaluator.createExpression.return_value = mocked_expression

        with (
            patch("domonic.domonic.parseString", return_value=object()) as mock_parse,
            patch("domonic.webapi.xpath.XPathEvaluator", return_value=mocked_evaluator),
            patch(
                "sys.stdin",
                io.StringIO("<html><body><a>One</a><a>Two</a></body></html>"),
            ),
            redirect_stdout(io.StringIO()) as stdout,
        ):
            do_things(
                self._base_args(
                    xpath_stdin="//a",
                    count=True,
                    parser="selectolax",
                )
            )

        mock_parse.assert_called_once_with(
            "<html><body><a>One</a><a>Two</a></body></html>",
            parser="selectolax",
        )
        self.assertEqual(stdout.getvalue().strip(), "2")

    def test_xpath_cli_uses_piped_stdin_when_only_expression_is_passed(self):
        mocked_result = MagicMock(nodes=["<title>Example</title>"])
        mocked_expression = MagicMock()
        mocked_expression.evaluate.return_value = mocked_result
        mocked_evaluator = MagicMock()
        mocked_evaluator.createExpression.return_value = mocked_expression

        with (
            patch("domonic.domonic.parseString", return_value=object()) as mock_parse,
            patch("domonic.webapi.xpath.XPathEvaluator", return_value=mocked_evaluator),
            patch(
                "sys.stdin",
                io.StringIO("<html><head><title>Example</title></head></html>"),
            ),
            patch("sys.stdin.isatty", return_value=False),
            redirect_stdout(io.StringIO()) as stdout,
        ):
            do_things(self._base_args(xpath=["//title"]))

        mock_parse.assert_called_once()
        mocked_evaluator.createExpression.assert_called_once_with("//title")
        self.assertIn("Example", stdout.getvalue())

    def test_query_cli_uses_piped_stdin_when_only_selector_is_passed(self):
        fake_page = MagicMock()
        fake_page.querySelectorAll.return_value = ["<a class='cta'>CTA</a>"]

        with (
            patch("domonic.domonic.parseString", return_value=fake_page) as mock_parse,
            patch(
                "sys.stdin",
                io.StringIO("<html><body><a class='cta'>CTA</a></body></html>"),
            ),
            patch("sys.stdin.isatty", return_value=False),
            redirect_stdout(io.StringIO()) as stdout,
        ):
            do_things(self._base_args(query=["a.cta"], parser="selectolax"))

        mock_parse.assert_called_once_with(
            "<html><body><a class='cta'>CTA</a></body></html>",
            parser="selectolax",
        )
        fake_page.querySelectorAll.assert_called_once_with("a.cta")
        self.assertIn("CTA", stdout.getvalue())

    def test_xpath_requires_url_and_expression(self):
        with patch("sys.stdin.isatty", return_value=True):
            with self.assertRaisesRegex(
                ValueError, "xpath expects exactly 2 arguments"
            ):
                do_things(self._base_args(xpath=["https://example.com"]))

    def test_query_requires_url_and_selector(self):
        with patch("sys.stdin.isatty", return_value=True):
            with self.assertRaisesRegex(
                ValueError, "query expects exactly 2 arguments"
            ):
                do_things(self._base_args(query=["https://example.com"]))

    def test_project_rejects_unknown_server_choice(self):
        with self.assertRaisesRegex(ValueError, "Unsupported server"):
            project("tmp-project", server_choice="not-a-real-server")


if __name__ == "__main__":
    unittest.main()
