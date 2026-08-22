"""
    test_odf
    ~~~~~~~~
"""

import unittest

import domonic.xml.odf as odf
from domonic.xml.odf import *


class TestCase(unittest.TestCase):
    def test_odf_text_document(self):
        doc = office_document_content(
            office_body(
                office_text(
                    text_h("Heading", **{"text:outline-level": "1"}),
                    text_p("Hello ODF"),
                )
            )
        )

        rendered = str(doc)
        self.assertIn("<office:document-content", rendered)
        self.assertIn('xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"', rendered)
        self.assertIn('office:version="1.2"', rendered)
        self.assertIn('<text:h text:outline-level="1">Heading</text:h>', rendered)
        self.assertIn("<text:p>Hello ODF</text:p>", rendered)

    def test_odf_namespaced_globals_and_factory(self):
        self.assertEqual(str(odf.__dict__["table:table"]()), "<table:table></table:table>")
        self.assertEqual(str(create_odf_element("draw:image", **{"xlink:href": "Pictures/one.png"})), '<draw:image xlink:href="Pictures/one.png"></draw:image>')

    def test_odf_generated_constructor_pattern(self):
        self.assertIn("office:document-content", odf_tags)
        self.assertIn("text:outline-level", odf_attributes)
        self.assertEqual(odf_tag_aliases["office_document_content"], "office:document-content")
        self.assertTrue(issubclass(office_document_content, ODFElement))
        self.assertIs(odf.__dict__["office:document-content"], office_document_content)

        heading = text_h("Heading", text_outline_level=2, text_style_name="Heading_20_2")
        self.assertEqual(
            str(heading),
            '<text:h text:outline-level="2" text:style-name="Heading_20_2">Heading</text:h>',
        )

        image = create_element("draw_image", xlink_href="Pictures/one.png", svg_width="4cm", svg_height="3cm")
        self.assertEqual(image.namespaceURI, DRAW)
        self.assertEqual(
            str(image),
            '<draw:image xlink:href="Pictures/one.png" svg:width="4cm" svg:height="3cm"></draw:image>',
        )

        manifest_doc = manifest_manifest(manifest_file_entry(manifest_full_path="/", manifest_media_type="text/xml"))
        self.assertIn('manifest:version="1.2"', str(manifest_doc))
        self.assertIn('manifest:full-path="/"', str(manifest_doc))

    def test_odf_content_example(self):
        from examples.odf_content import build_content, build_manifest, render_xml

        rendered = render_xml(build_content())
        manifest = render_xml(build_manifest())

        self.assertIn('<?xml version="1.0" encoding="UTF-8"?>', rendered)
        self.assertIn("<office:document-content", rendered)
        self.assertIn('office:version="1.2"', rendered)
        self.assertIn('<table:table table:name="Release notes">', rendered)
        self.assertIn("<text:p>Namespaced constructors</text:p>", rendered)
        self.assertIn("<manifest:manifest", manifest)
        self.assertIn('manifest:full-path="content.xml"', manifest)


if __name__ == "__main__":
    unittest.main()
