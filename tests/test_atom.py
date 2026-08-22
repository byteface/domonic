"""
    test_atom
    ~~~~~~~~~
"""

import unittest

from domonic.xml.atom import *


class TestCase(unittest.TestCase):
    def test_atom_feed(self):
        doc = feed(
            title("Example Feed"),
            id("urn:uuid:60a76c80-d399-11d9-b93C-0003939e0af6"),
            updated("2003-12-13T18:30:02Z"),
            link(_href="https://example.com/"),
            entry(
                title("Atom-Powered Robots Run Amok"),
                id("urn:uuid:1225c695-cfb8-4ebb-aaaa-80da344efa6a"),
                updated("2003-12-13T18:30:02Z"),
                summary("Some text."),
            ),
        )

        rendered = str(doc)
        self.assertIn('<feed xmlns="http://www.w3.org/2005/Atom">', rendered)
        self.assertIn('<link href="https://example.com/"></link>', rendered)
        self.assertIn("<entry>", rendered)

    def test_atom_generated_constructor_pattern(self):
        self.assertIn("feed", atom_tags)
        self.assertIn("xml:lang", atom_attributes)
        self.assertTrue(issubclass(feed, AtomElement))
        self.assertEqual(feed.name, "feed")

        entry_el = create_element("entry", title("Generated"), xml_lang="en")
        self.assertIsInstance(entry_el, AtomElement)
        self.assertEqual(entry_el.namespaceURI, XMLNS)
        self.assertEqual(str(entry_el), '<entry xml:lang="en"><title>Generated</title></entry>')

        custom = create_element("app:edited", "now")
        self.assertEqual(str(custom), "<app:edited>now</app:edited>")

    def test_atom_feed_example(self):
        from examples.atom_feed import build_feed, render_xml

        rendered = render_xml(build_feed())

        self.assertIn('<?xml version="1.0" encoding="UTF-8"?>', rendered)
        self.assertIn('<feed xmlns="http://www.w3.org/2005/Atom"', rendered)
        self.assertIn('xmlns:app="http://www.w3.org/2007/app"', rendered)
        self.assertIn('xml:lang="en"', rendered)
        self.assertIn(
            '<link href="https://example.com/domonic/atom.xml" rel="self">',
            rendered,
        )
        self.assertIn("<app:edited>2026-08-22T12:05:00Z</app:edited>", rendered)


if __name__ == "__main__":
    unittest.main()
