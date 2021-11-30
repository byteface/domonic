"""
    domonic.xml
    ====================================

    definitions for generating given types of xml

"""

DECLARATION = """<?xml version="1.0" encoding="UTF-8"?>"""
STYLESHEET = lambda xsl: f"""<?xml-stylesheet type="text/xsl" href="{xsl}"?>"""
# <?xml-stylesheet type="text/xsl" href="i.e/wp-content/plugins/wordpress-seo-premium/css/main-sitemap.xsl"?>

# comment = lambda comment: f"""<!-- {comment} -->"""


def comment(comment: str):  # -> str:
    return "<!-- {} -->".format(comment)


cdata = lambda cdata: f"""<![CDATA[{cdata}]]>"""
CDATA = cdata

# from domonic.html import render
# render = render


def prettify(elem):
    """prettify

    Args:
        elem (Element): Element to be prettified

    Returns:
        str: prettified xml element
    """
    from xml.dom import minidom

    x = minidom.parseString(elem)
    # pretty = '\n'.join(x.toprettyxml().splitlines()[1:])
    return x.toprettyxml()
