"""
domonic.parsers
====================================

A place for parsers and utils for doings so.

These methods operate strings not on pyml objects. For dom manipulation use the dom.

WARNING> dont use this class. still in development/idea phase. Teasing util methods out from the in-place parser

"""

import re

from domonic.html import *
from domonic.xml.sitemap import *


def create_element(name="custom_tag", *args, **kwargs):  # type: ignore[no-redef]
    """
    NOTE - USED BY THE HACKED EXPAT PARSER TO GET VALID DOCUMENT NODES FROM ANY KNOWN SET

    Deliberately shadows the ``create_element`` pulled in by ``from
    domonic.html import *`` -- this variant also knows the sitemap/XML tag sets.
    """
    from domonic.html import create_element as create_html_element
    from domonic.html import html_tags

    if name in html_tags:
        return globals()[name](*args, **kwargs)
    from domonic.xml.sitemap import sitemap_tags

    if name in sitemap_tags:
        return globals()[name](*args, **kwargs)

    return create_html_element(name, *args, **kwargs)


def remove_tags(html_str: str, tags):
    """
    removes a list of tags and their content from the html
    """

    def remove_tag_block(content: str, tag_name: str) -> str:
        opening = f"<{tag_name}"
        closing = f"</{tag_name}>"
        lower_content = content.lower()
        result = []
        cursor = 0

        while True:
            start = lower_content.find(opening, cursor)
            if start == -1:
                result.append(content[cursor:])
                break

            result.append(content[cursor:start])

            open_end = lower_content.find(">", start)
            if open_end == -1:
                result.append(content[start:])
                break

            close_start = lower_content.find(closing, open_end + 1)
            if close_start == -1:
                cursor = open_end + 1
                continue

            cursor = close_start + len(closing)

        return "".join(result)

    def remove_html_comments(content: str) -> str:
        result = []
        cursor = 0

        while True:
            start = content.find("<!--", cursor)
            if start == -1:
                result.append(content[cursor:])
                break

            result.append(content[cursor:start])
            end = content.find("-->", start + 4)
            if end == -1:
                break
            cursor = end + 3

        return "".join(result)

    if isinstance(tags, str):
        tags = [tags]

    if isinstance(tags, list):
        for tag in tags:

            if tag == "js" or tag == "javascript":
                html_str = remove_tag_block(html_str, "script")

            if tag == "css":
                html_str = remove_tag_block(html_str, "style")

            if "comment" in tag or tag == "#" or tag == "//":
                html_str = remove_html_comments(html_str)

            # tag = re.compile(r'<(style).*?</\1>(?s)')
            # html = tag.sub('', html)
    return html_str


def remove_extra_whitespace(html_str: str):
    """
    only allow single spaces and tabs
    """
    html_str = re.sub(r"\s+", " ", html_str)
    html_str = re.sub(r"\t", " ", html_str)
    return html_str


def remove_doctype(html_str: str):
    """
    remove the doctype from the html_str
    """
    doctype = re.compile(r"<!DOCTYPE.*?>", re.IGNORECASE)
    html_str = doctype.sub("", html_str)
    return html_str
    # page = ''.join(page.split('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">'))
    # page = ''.join(page.split('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'))
    # page = ''.join(page.split('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'))


def remove_xml_header(html_str: str):
    """
    remove the xml header from the html_str
    """
    header = re.compile(r"<\?xml.*?\?>", re.IGNORECASE)
    html_str = header.sub("", html_str)
    return html_str


def remove_html_tags(html_str: str):
    """
    remove all html tags from the html_str
    """
    # remove all tags
    page = re.compile(r"<.*?>", re.IGNORECASE)
    html_str = page.sub("", html_str)
    return html_str


def remove_html_tag_by_name(html_str: str, tag: str):
    """
    remove all html tags with the given name from the html_str
    """
    # remove all tags
    page = re.compile(r"<.*?{}.*?>".format(tag), re.IGNORECASE)
    html_str = page.sub("", html_str)
    return html_str


# def remove_all_tags(html: str):
#     """
#     remove tags
#     """
#     page = re.sub(r'<[^>]*>', '', page)


def remove_content_between_brackets(html_str: str):
    """
    remove content between brackets
    """
    page = re.sub(r"\[[^\]]*\]", "", html_str)
    return page


def remove_content_between_parenthesis(html_str: str):
    """
    remove content between parenthesis
    """
    page = re.sub(r"\([^\)]*\)", "", html_str)
    return page


def remove_content_between_braces(html_str: str):
    """
    remove content between braces
    """
    page = re.sub(r"\{[^\}]*\}", "", html_str)
    return page


# def remove_consecutive_spaces(html_str: str):
#     """
#     remove consecutive spaces
#     """
#     page = re.sub(r'\s+', ' ', page)


def remove_whitespace(html_str: str):
    """
    remove whitespace
    """
    html_str = re.sub(r"\s+", " ", html_str)
    return html_str


def remove_newlines(html_str: str):
    """
    remove newlines
    """
    html_str = re.sub(r"\n", "", html_str)
    return html_str


def remove_tabs(html_str: str):
    """
    remove all tabs from the html_str
    """
    html_str = re.sub(r"\t", "", html_str)
    return html_str


def replace_special_quotes(html_str: str):
    """
    replace special quotes with html entities
    """
    # special quotes
    html_str = html_str.replace("“", "&ldquo;")
    html_str = html_str.replace("”", "&rdquo;")
    html_str = html_str.replace("’", "&rsquo;")
    html_str = html_str.replace("‘", "&lsquo;")
    html_str = html_str.replace("„", "&sbquo;")
    html_str = html_str.replace("‚", "&obquo;")
    html_str = html_str.replace("‹", "&usbquo;")
    html_str = html_str.replace("›", "&ensquo;")
    return html_str


def replace_special_chars(html_str: str):
    """
    replace special characters with html entities
    """
    # special chars
    html_str = html_str.replace("&", "&amp;")
    html_str = html_str.replace("<", "&lt;")
    html_str = html_str.replace(">", "&gt;")
    html_str = html_str.replace('"', "&quot;")
    html_str = html_str.replace("'", "&#39;")
    return html_str


# def remove_bom(html: str):
# page = page.replace('\ufeff', '')


def replace_punctuation(html_str: str):
    """
    replace punctuation with html entities
    """
    # special chars
    html_str = html_str.replace(".", "&#46;")
    html_str = html_str.replace(",", "&#44;")
    html_str = html_str.replace("!", "&#33;")
    html_str = html_str.replace("?", "&#63;")
    html_str = html_str.replace("(", "&#40;")
    html_str = html_str.replace(")", "&#41;")
    html_str = html_str.replace("[", "&#91;")
    html_str = html_str.replace("]", "&#93;")
    html_str = html_str.replace("{", "&#123;")
    html_str = html_str.replace("}", "&#125;")
    html_str = html_str.replace("<", "&lt;")
    html_str = html_str.replace(">", "&gt;")
    html_str = html_str.replace('"', "&quot;")
    html_str = html_str.replace("'", "&#39;")
    return html_str


# def add_newlines(html: str):
# """
# add newlines
# """
# page = page.replace('\n', '<br>')


def replace_newlines(html_str: str):
    """
    remove newlines
    """
    html_str = html_str.replace("<br>", "\n")
    return html_str


# def add_paragraphs(html: str):
#     """
#     add paragraphs
#     """
#     page = page.replace('\n', '<br>\n')

# def remove_paragraphs(html: str):
#     """
#     remove paragraphs
#     """
#     page = page.replace('<br>\n', '\n')


def clean_junk(page):
    """[clears any typically invalid runs of chars that may exist in pyml.
        to be used at the end of all cleaning functions before an evaluation.
        should not apply to content.]

    Args:
        page ([str]): [pyml string]

    Returns:
        [str]: [pyml string with garbled chars removed]
    """
    page = page.replace('",","', '","')
    page = page.replace('",",', '",')
    page = page.replace('", ",', '",')
    page = page.replace('", \n",', '",')
    page = page.replace('",\n ",', '",')
    page = page.replace('","\n)', '"\n)')
    page = page.replace('", \n, _', '",\n_')
    page = page.replace(', "\n)', "\n)")

    # page = page.replace(',",', ',') < VALID
    page = page.replace(
        ",  ,", ","
    )  # < new bug. due to single attributes having big space in front for some reason
    page = page.replace(', ",', ",")
    page = page.replace(",,", ",")
    page = page.replace(", ,", ",")
    page = page.replace(
        ',"",', ","
    )  # careul. new and covers up somethings else. solo attributes still not done well

    page = page.replace("( ,*", "(*")
    page = page.replace("( , *", "(*")
    page = page.replace("(,*", "(*")
    page = page.replace("(, *", "(*")
    page = page.replace("(,  *", "(*")
    page = page.replace('(", *', "(*")
    page = page.replace('(\n",', "(\n")
    page = page.replace("(\n,", "(")

    page = page.replace('),",', "),")
    page = page.replace('),\n"\n),', "),\n),")
    page = page.replace('},\n"\n),', "}\n),")

    page = page.replace(
        '"_, _', '"_'
    )  # when solo hyphenated custom attribute is first on a line.

    # page = page.replace('),\n",\n', '(')  # < break things but is also valid. text sentences can start with a comma
    # 2 issues. this also turns a closer into an opener. when catching a true case
    return page


# @staticmethod
def dent(pyml, use_tabs=False):
    """[
        proper dentage for pyml
    ]
    """
    tabs_or_spaces = "    "
    if use_tabs:
        tabs_or_spaces = "\t"
    dentage = 0
    lastchar = ""
    dented = ""
    if "\n" not in pyml:
        lines = []
        current = ""
        for char in pyml:
            if char == "(":
                lines.append((tabs_or_spaces * dentage) + current + "(")
                dentage += 1
                current = ""
                continue
            if char == ")":
                if current.strip():
                    lines.append((tabs_or_spaces * dentage) + current)
                    current = ""
                dentage = max(0, dentage - 1)
                lines.append((tabs_or_spaces * dentage) + ")")
                continue
            current += char
        if current.strip():
            lines.append((tabs_or_spaces * dentage) + current)
        return "\n".join(lines)
    for count, char in enumerate(pyml):
        if char == "(":
            dentage += 1
        if char == ")":
            dentage -= 1
        if lastchar == "\n":
            char = tabs_or_spaces * dentage + char
        lastchar = char
        dented += char
        if dentage < 0:
            dentage = 0
    return dented


def add_cdata_tags_to_every_node(
    content: str,
):
    """[puts a CDATA tag on every node in the document]"""
    content = content.replace("<", "<![CDATA[")
    content = content.replace(">", "]]>")
    return content


def remove_cdata_tags_from_every_node(content: str):
    """[removes a CDATA tag from every node in the document]"""
    content = content.replace("]]>", ">")
    content = content.replace("<![CDATA[", "<")
    return content


def add_xml_declaration_to_document(content: str):
    """[puts an XML declaration at the top of the document]"""
    content = content.replace("<", '<?xml version="1.0" encoding="UTF-8" ?>\n<')
    return content
