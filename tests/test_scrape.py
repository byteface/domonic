"""
test_scrape
~~~~~~~~~~~
Tests for ``domonic.scrape`` -- the front door over ``domonic.webapi.fetch``.
"""

import json
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from domonic import scrape
from domonic.webapi.fetch import Request, Response

HTML = (
    "<html><body><main>"
    "<article class='post'><h1>Release</h1></article>"
    "<ul><li>a</li><li>b</li></ul>"
    "</main></body></html>"
)


def _html_response(method, url, **kwargs):
    return SimpleNamespace(
        url=url,
        status_code=200,
        reason="OK",
        headers={"Content-Type": "text/html"},
        content=HTML.encode("utf-8"),
        history=[],
    )


def _json_response(method, url, **kwargs):
    return SimpleNamespace(
        url=url,
        status_code=200,
        reason="OK",
        headers={"Content-Type": "application/json"},
        content=json.dumps({"url": url}).encode("utf-8"),
        history=[],
    )


class TestScrape(unittest.TestCase):
    def test_single_url_returns_dom(self):
        with patch("requests.request", side_effect=_html_response):
            dom = scrape("https://example.com")
        self.assertEqual(dom.querySelector("h1").textContent, "Release")

    def test_response_flag_returns_pair(self):
        with patch("requests.request", side_effect=_html_response):
            response, dom = scrape("https://example.com", response=True)
        self.assertIsInstance(response, Response)
        self.assertEqual(response.status, 200)
        self.assertTrue(response.ok)
        self.assertEqual(response.url, "https://example.com")
        self.assertEqual(response.headers.get("content-type"), "text/html")
        self.assertEqual(dom.querySelector("h1").textContent, "Release")

    def test_accepts_request_object(self):
        with patch("requests.request", side_effect=_html_response) as mock:
            dom = scrape(Request("https://example.com", init={"method": "GET", "headers": {"X-Tag": "y"}}))
        self.assertEqual(dom.querySelector("h1").textContent, "Release")
        self.assertEqual(mock.call_args.args[0], "GET")
        self.assertEqual(mock.call_args.kwargs["headers"], {"x-tag": "y"})

    def test_accepts_iterable_of_requests(self):
        reqs = [Request("https://example.com/1"), Request("https://example.com/2")]
        with patch("requests.request", side_effect=_html_response):
            doms = scrape(reqs)
        self.assertEqual([d.querySelector("h1").textContent for d in doms], ["Release", "Release"])

    def test_selector_returns_element(self):
        with patch("requests.request", side_effect=_html_response):
            el = scrape("https://example.com", selector="article.post h1")
        self.assertEqual(el.textContent, "Release")

    def test_selector_all_returns_list(self):
        with patch("requests.request", side_effect=_html_response):
            items = scrape("https://example.com", selector="li", all=True)
        self.assertEqual([li.textContent for li in items], ["a", "b"])

    def test_to_projections(self):
        with patch("requests.request", side_effect=_html_response):
            self.assertIn("Release", scrape("https://example.com", to="text"))
            self.assertIn("h1(", scrape("https://example.com", to="pyml"))
            dom = scrape("https://example.com", to="dom")
        self.assertEqual(dom.querySelector("h1").textContent, "Release")

    def test_to_json(self):
        with patch("requests.request", side_effect=_json_response):
            data = scrape("https://example.com/api", to="json")
        self.assertEqual(data, {"url": "https://example.com/api"})

    def test_multiple_urls_preserve_order(self):
        urls = ["https://example.com/1", "https://example.com/2", "https://example.com/3"]
        with patch("requests.request", side_effect=_html_response):
            doms = scrape(urls)
        self.assertEqual([d.querySelector("h1").textContent for d in doms], ["Release"] * 3)

    def test_multiple_urls_with_response(self):
        urls = ["https://example.com/1", "https://example.com/2"]
        with patch("requests.request", side_effect=_html_response):
            pairs = scrape(urls, selector="h1", response=True)
        self.assertEqual([r.url for r, _ in pairs], urls)
        self.assertEqual([el.textContent for _, el in pairs], ["Release", "Release"])

    def test_http_controls_passed_through(self):
        with patch("requests.request", side_effect=_html_response) as mock:
            scrape("https://example.com", headers={"Accept": "text/html"}, params={"q": "x"}, timeout=5)
        self.assertEqual(mock.call_args.kwargs["headers"], {"accept": "text/html"})
        self.assertEqual(mock.call_args.kwargs["params"], {"q": "x"})
        self.assertEqual(mock.call_args.kwargs["timeout"], 5)

    def test_request_field_kwargs_build_the_request(self):
        with patch("requests.request", side_effect=_json_response) as mock:
            scrape("https://example.com/api", to="text", method="POST", json={"q": "x"})
        self.assertEqual(mock.call_args.args[0], "POST")
        self.assertEqual(mock.call_args.kwargs["data"], json.dumps({"q": "x"}))
        self.assertEqual(mock.call_args.kwargs["headers"].get("content-type"), "application/json")

    def test_unknown_kwargs_go_to_requests(self):
        with patch("requests.request", side_effect=_html_response) as mock:
            scrape("https://example.com", verify=False)
        self.assertIs(mock.call_args.kwargs["verify"], False)

    def test_fetch_failure_raises(self):
        with patch("requests.request", side_effect=RuntimeError("boom")):
            with self.assertRaises(RuntimeError):
                scrape("https://example.com")

    def test_validation(self):
        with self.assertRaises(ValueError):
            scrape("https://example.com", to="nope")
        with self.assertRaises(ValueError):
            scrape("https://example.com", to="text", selector="h1")
        with self.assertRaises(ValueError):
            scrape("https://example.com", all=True)


if __name__ == "__main__":
    unittest.main()
