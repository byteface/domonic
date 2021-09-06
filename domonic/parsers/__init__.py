"""
    domonic.parsers
    ====================================

    A place for parsers and utils for doings so.

    These methods operate strings not on pyml objects. For dom manipulation use the dom.

    WARNING> dont use this class. still in development/idea phase. Teasing util methods out from the in-place parser 

"""

import re


def remove_tags(html_str:str, tags):
    """
    removes a list of tags and their content from the html
    """
    if isinstance(tags, str):
        tags = [tags]

    if isinstance(tags, list):
        for tag in tags:

            if tag == 'js' or tag == 'javascript':
                scripts = re.compile(r'<(script).*?</\1>(?s)')
                html_str = scripts.sub('', html_str)

            if tag == 'css':
                css = re.compile(r'<(style).*?</\1>(?s)')
                html_str = css.sub('', html_str)

            if 'comment' in tag or tag == '#' or tag == '//':
                comments = re.compile(r'<!--(.|\s)*?-->')
                html_str = comments.sub('', html_str)

            # tag = re.compile(r'<(style).*?</\1>(?s)')
            # html = tag.sub('', html)
    return html_str


def remove_extra_whitespace(html: str):
    """
    only allow single spaces and tabs
    """
    html = re.sub(r'\s+', ' ', html)
    html = re.sub(r'\t', ' ', html)
    return html
    # remove abnormal spacing between tag attributes (TODO- maybe 2 spaces is valid somewhere?)
    # page = page.replace('   ', ' ')
    # page = page.replace('  ', ' ')
    # page = page.replace('  ', ' ')


def remove_doctype(html: str):
    """
    remove the doctype from the html
    """
    doctype = re.compile(r'<!DOCTYPE.*?>', re.IGNORECASE)
    html = doctype.sub('', html)
    return html
    # print('parsing parsing parsing!!')

    page = ''.join(page.split('<!DOCTYPE HTML>'))
    page = ''.join(page.split('<!DOCTYPE html>'))
    page = ''.join(page.split('<!doctype html>'))
    page = ''.join(page.split('<!doctype HTML>'))

    page = ''.join(page.split('<?xml version="1.0" encoding="utf-8"?>'))
    page = ''.join(page.split('<?xml version="1.0" encoding="utf-8" ?>'))
    page = ''.join(page.split('<?xml version="1.0" encoding="UTF-8" ?>'))

    page = ''.join(page.split('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'))
    # page = ''.join(page.split('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'))
    # page = ''.join(page.split('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">'))
    # page = ''.join(page.split('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'))
    # page = ''.join(page.split('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'))
    # page = ''.join(page.split('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">'))
    # page = ''.join(page.split('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'))
    # page = ''.join(page.split('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'))
    # page = ''.join(page.split('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">'))
    # page = ''.join(page.split('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'))
    # page = ''.join(page.split('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'))

def remove_xml_header(html:str):
    """
    remove the xml header from the html
    """
    header = re.compile(r'<\?xml.*?\?>', re.IGNORECASE)
    html = header.sub('', html)
    return html

def remove_html_tags(html: str):
    """
    remove all html tags from the html
    """
    # remove all tags
    page = re.compile(r'<.*?>', re.IGNORECASE)
    html = page.sub('', html)
    return html

def remove_html_tag_by_name(html: str, tag: str):
    """
    remove all html tags from the html
    """
    # remove all tags
    page = re.compile(r'<.*?{}.*?>'.format(tag), re.IGNORECASE)
    html = page.sub('', html)
    return html


# def remove_all_tags(html: str):
#     """
#     remove tags
#     """
#     page = re.sub(r'<[^>]*>', '', page)

def remove_content_between_brackets(html: str):
    """
    remove content between brackets
    """
    page = re.sub(r'\[[^\]]*\]', '', page)

def remove_content_between_parenthesis(html: str):
    """
    remove content between parenthesis
    """
    page = re.sub(r'\([^\)]*\)', '', page)

def remove_content_between_braces(html: str):
    """
    remove content between braces
    """
    page = re.sub(r'\{[^\}]*\}', '', page)

# def remove_consecutive_spaces(html: str):
#     """
#     remove consecutive spaces
#     """
#     page = re.sub(r'\s+', ' ', page)


def remove_whitespace(html: str):
    """
    remove whitespace
    """
    html = re.sub(r'\s+', ' ', html)
    return html

def remove_newlines(html: str):
    """
    remove newlines
    """
    html = re.sub(r'\n', '', html)
    return html

def remove_tabs(html: str):
    """
    remove all tabs from the html
    """
    html = re.sub(r'\t', '', html)
    return html


def replace_special_quotes(html: str):
    """
    replace special quotes with html entities
    """
    # special quotes
    page = page.replace('“', '&ldquo;')
    page = page.replace('”', '&rdquo;')
    page = page.replace('’', '&rsquo;')
    page = page.replace('‘', '&lsquo;')
    page = page.replace('„', '&sbquo;')
    page = page.replace('‚', '&obquo;')
    page = page.replace('‹', '&usbquo;')
    page = page.replace('›', '&ensquo;')


def replace_special_chars(html: str):
    """
    replace special characters with html entities
    """
    # special chars
    page = page.replace('&', '&amp;')
    page = page.replace('<', '&lt;')
    page = page.replace('>', '&gt;')
    page = page.replace('"', '&quot;')
    page = page.replace("'", '&#39;')


# def remove_bom(html: str):
    # page = page.replace('\ufeff', '')

def replace_punctuation(html: str):
    """
    replace punctuation with html entities
    """
    # special chars
    page = page.replace('.', '&#46;')
    page = page.replace(',', '&#44;')
    page = page.replace('!', '&#33;')
    page = page.replace('?', '&#63;')
    page = page.replace('(', '&#40;')
    page = page.replace(')', '&#41;')
    page = page.replace('[', '&#91;')
    page = page.replace(']', '&#93;')
    page = page.replace('{', '&#123;')
    page = page.replace('}', '&#125;')
    page = page.replace('<', '&lt;')
    page = page.replace('>', '&gt;')
    page = page.replace('"', '&quot;')
    page = page.replace("'", '&#39;')


# def add_newlines(html: str):
    # """
    # add newlines
    # """
    # page = page.replace('\n', '<br>')

def replace_newlines(html: str):
    """
    remove newlines
    """
    page = page.replace('<br>', '\n')

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
    page = page.replace(', "\n)', '\n)')

    # page = page.replace(',",', ',') < VALID
    page = page.replace(',  ,', ',')  # < new bug. due to single attributes having big space in front for some reason
    page = page.replace(', ",', ',')
    page = page.replace(',,', ',')
    page = page.replace(', ,', ',')
    page = page.replace(',"",', ',')  # careul. new and covers up somethings else. solo attributes still not done well

    page = page.replace('( ,*', '(*')
    page = page.replace('( , *', '(*')
    page = page.replace('(,*', '(*')
    page = page.replace('(, *', '(*')
    page = page.replace('(,  *', '(*')
    page = page.replace('(", *', '(*')
    page = page.replace('(\n",', '(\n')
    page = page.replace('(\n,', '(')

    page = page.replace('),",', '),')
    page = page.replace('),\n"\n),', '),\n),')
    page = page.replace('},\n"\n),', '}\n),')

    page = page.replace('"_, _', '"_')  # when solo hyphenated custom attribute is first on a line.

    # page = page.replace('),\n",\n', '(')  # < break things but is also valid. text sentences can start with a comma
    # 2 issues. this also turns a closer into an opener. when catching a true case
    return page


# @staticmethod
def dent(pyml, use_tabs=False):
    """ [
        proper dentage
    ]
    """
    tabs_or_spaces = "    "
    if use_tabs:
        tabs_or_spaces = "\t"
    dentage = 0
    lastchar = ""
    dented = ""
    for count, char in enumerate(pyml):
        if char == "(":
            dentage += 1
        if char == ")":
            dentage -= 1
        if lastchar == "\n":  # TODO - if file doesn't have newlines already
            char = tabs_or_spaces * dentage + char
        lastchar = char
        dented += char
        if dentage < 0:
            dentage = 0
    return dented


def add_cdata_tags_to_every_node(content: str): # TODO - just have a CDATASection class?
    """[puts a CDATA tag on every node in the document] """
    content = content.replace('<', '<![CDATA[')
    content = content.replace('>', ']]>')
    return content

def remove_cdata_tags_from_every_node(content: str):
    """[removes a CDATA tag from every node in the document] """
    content = content.replace(']]>', '>')
    content = content.replace('<![CDATA[', '<')
    return content

def add_xml_declaration_to_document(content: str):
    """[puts an XML declaration at the top of the document] """
    content = content.replace('<', '<?xml version="1.0" encoding="UTF-8" ?>\n<')
    return content




# TODO - other methods I can add to this class
# - add_xml_declaration_to_document
# - add_cdata_tags_to_every_node
# - remove_cdata_tags_from_every_node
# - remove_newlines
# - add_paragraphs
# - indent
# - create_html_from_markdown
# - create_html_from_xml
# - get_xpath_of_node


''' TODO - check earlier version getter/setters for some string methods that may be useful here
@body.setter
def body(self, content):
    """ Sets the document's body (the <body> element) """
    # self.querySelector('body')
    # tag = "body"
    # reg = f"<{tag}.*?>(.+?)</{tag}>"
    # pattern = re.compile(reg)
    # tags = re.findall(pattern,html)
    # return tags[0]
    print("TODO - setter method on body")
    return
'''