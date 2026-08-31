"""
ODF content example
===================

Generate a tiny OpenDocument ``content.xml`` payload.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import domonic.xml.odf as odf

OUTPUT = Path(__file__).with_suffix(".xml")


def build_content():
    return odf.office_document_content(
        odf.office_body(
            odf.office_text(
                odf.text_h(
                    "domonic XML examples",
                    text_outline_level="1",
                    text_style_name="Heading_20_1",
                ),
                odf.text_p("This paragraph was generated with domonic.xml.odf."),
                odf.table_table(
                    odf.table_table_column(table_number_columns_repeated="2"),
                    odf.table_table_row(
                        odf.table_table_cell(
                            odf.text_p("Feature"),
                            office_value_type="string",
                        ),
                        odf.table_table_cell(
                            odf.text_p("Status"),
                            office_value_type="string",
                        ),
                    ),
                    odf.table_table_row(
                        odf.table_table_cell(
                            odf.text_p("Namespaced constructors"),
                            office_value_type="string",
                        ),
                        odf.table_table_cell(
                            odf.text_p("Ready"),
                            office_value_type="string",
                        ),
                    ),
                    table_name="Release notes",
                ),
            )
        )
    )


def build_manifest():
    return odf.manifest_manifest(
        odf.manifest_file_entry(
            manifest_full_path="/",
            manifest_media_type="application/vnd.oasis.opendocument.text",
        ),
        odf.manifest_file_entry(
            manifest_full_path="content.xml",
            manifest_media_type="text/xml",
        ),
    )


def render_xml(node):
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + str(node)


if __name__ == "__main__":
    OUTPUT.write_text(render_xml(build_content()), encoding="utf-8")
    manifest_path = OUTPUT.with_name("odf_manifest.xml")
    manifest_path.write_text(render_xml(build_manifest()), encoding="utf-8")
    print(f"Wrote {OUTPUT}")
    print(f"Wrote {manifest_path}")
