"""
domonic
====================================

Python DOM, HTML, SVG, XML, Web API, and JavaScript-like runtime toolkit.

"""

__version__ = "1.1.0"
__license__ = "MIT"
__author__ = "@byteface"

VERSION = __version__


import ast
import re
import sys

import domonic.dom as dom

# from domonic.components import Input
try:
    from domonic.html import *
    from domonic.html import html_attributes as attributes
except ImportError:  # pragma: no cover - optional dependency chain
    attributes = []

try:
    from domonic.javascript import *
    _HAS_JAVASCRIPT = True
except ImportError:  # pragma: no cover - optional dependency chain
    _HAS_JAVASCRIPT = False

try:
    # Keep package-root tag conflicts HTML-first; SVG versions are available from domonic.svg.
    from domonic.svg import *
    from domonic.html import a, audio, canvas, iframe, script, style, video
    _HAS_SVG = True
except ImportError:  # pragma: no cover - optional dependency chain
    _HAS_SVG = False

try:
    from domonic.utils import NumberUnit, NumberUtils, Utils
except ImportError:  # pragma: no cover - optional dependency chain
    NumberUnit = None
    NumberUtils = None
    Utils = None


class domonic:

    dom = dom
    DEFAULT_PARSER = "auto"

    JS_MASTER = "assets/js/master.js"
    CSS_STYLE = "assets/css/style.css"

    @staticmethod
    def set_default_parser(parser: str):
        """Set the default parser used by parseString when no parser is passed."""
        parser_name = (parser or "auto").lower()
        valid = {
            "auto",
            "html5_parser",
            "html5-parser",
            "html5lib",
            "lxml_html",
            "lxml-html",
            "expat",
            "selectolax",
            "markupever",
            "justhtml",
        }
        if parser_name not in valid:
            raise ValueError(f"Unknown parser: {parser}")
        if parser_name == "html5-parser":
            parser_name = "html5_parser"
        if parser_name == "lxml-html":
            parser_name = "lxml_html"
        domonic.DEFAULT_PARSER = parser_name

    @staticmethod
    def get_default_parser() -> str:
        """Return the parser name used by parseString by default."""
        return domonic.DEFAULT_PARSER

    @staticmethod
    def get(url: str):
        """downloads html and converts to domonic"""
        import requests

        r = requests.get(url, timeout=30)
        return domonic.parse(r.text)
        # TODO - param to eval

    @staticmethod
    def loads(path: str, *args, **kwargs):
        """[
            given a path to a file will return the .pyml as a python object

            if you have variables in the template they can be pass as kwargs
        ]
        """
        with open(path, "r") as pyml_string:
            content = pyml_string.read()
            # print("++++",content, type(content) )
            prog = domonic.domonify(str(content), *args, **kwargs)
            if type(prog) is tuple:
                prog = prog[0]
            return prog

    @staticmethod
    def load(pyml: str, *args, **kwargs):
        """[
            turns a pyml string into a python object
        ]
        """
        if not isinstance(pyml, str):
            raise ValueError("load requires a string not:", type(pyml))

        page = domonic.parse(pyml)
        prog = domonic.domonify(page, *args, **kwargs)
        if type(prog) is tuple:
            if len(prog) < 2:
                prog = prog[0]
            elif prog[1] == None:
                prog = prog[0]
            else:
                prog = list(prog)
        return prog

    @staticmethod
    def _split_top_level_pyml(pyml: str):
        """Split sibling top-level pyml expressions into standalone chunks."""
        chunks = []
        current = []
        depth = 0
        quote = None
        escaped = False

        for char in pyml:
            if quote is not None:
                current.append(char)
                if escaped:
                    escaped = False
                    continue
                if char == "\\":
                    escaped = True
                    continue
                if char == quote:
                    quote = None
                continue

            if char in ("'", '"'):
                quote = char
                current.append(char)
                continue

            if char == "(":
                depth += 1
            elif char == ")":
                depth = max(0, depth - 1)

            if char == "," and depth == 0:
                chunk = "".join(current).strip().rstrip(",").strip()
                if chunk:
                    chunks.append(chunk)
                current = []
                continue

            current.append(char)

        chunk = "".join(current).strip().rstrip(",").strip()
        if chunk:
            chunks.append(chunk)
        return chunks

    @staticmethod
    def domonify(pyml: str, *args, **kwargs):
        """[
            attempts to fix pyml
        ]

        Args:
            pyml (str): [a string in the form div(_class="123")]

        Returns:
            a python object
            Note:
            returns a potentially edited working program. (not the string)
            if it was ammeneded, render the returned object to get the new string
        """
        # print(pyml)
        if not isinstance(pyml, str):
            raise ValueError("domonify requires a string not:", type(pyml))

        # print("HI>>", pyml)

        s = domonic.evaluate(pyml, *args, **kwargs)

        # NOTE - valid chunks of pyml can still not eval if they are not wrapped
        # i.e. a list not in aa ul or ol. when on single line evaulate will fix
        # but on mulitple lines it will not.
        try:
            p = domonic._safe_eval_pyml(s, kwargs)
        except Exception as e:
            fragments = domonic._split_top_level_pyml(pyml)
            if len(fragments) > 1:
                return tuple(
                    domonic.domonify(fragment, *args, **kwargs)
                    for fragment in fragments
                )
            pyml = "".join(pyml.splitlines()).strip(",")  # try again on a single line
            s = domonic.evaluate(pyml, *args, **kwargs)
            p = domonic._safe_eval_pyml(s, kwargs)

        return p

    LAST_ERR = None  # to stop re-eval

    @staticmethod
    def evaluate(pyml: str, *args, **kwargs):
        """[
            attempts to fix pyml by using eval to make sure we can contruct nodes.
            be careful.
        ]

        Args:
            pyml (str): [a string in the form div(_class="123")]

        Returns:
            a python object
            Note:
            returns a potentially edited working program. (not the string)
            if it was ammeneded, render the returned object to get the new string
        """

        # print(pyml)
        if not isinstance(pyml, str):
            raise ValueError("evaluate requires a string not:", type(pyml))

        try:
            domonic._safe_eval_pyml(pyml, kwargs)
            domonic.LAST_ERR = None
            return pyml  # ????
        except Exception as e:
            # import sys
            # old_log = sys.stdout
            # log_file = open("fail.log","w")
            # sys.stdout = log_file
            # print(e)
            # sys.stdout = old_log

            # if end of file err. add a closed curly
            if "EOF" in str(e):
                # unexpected EOF while parsing (<string>, line 471)
                err = str(e)
                if str(len(pyml.splitlines())) in err:
                    pyml += ")"
                    return domonic.evaluate(pyml, *args, **kwargs)  # try again

            if "positional argument follows keyword argument" in str(e):

                """
                # print(Utils.digits(e))
                if str(e) == domonic.LAST_ERR:  # only allow 1 error per line
                    # raise ValueError("Recursion limit exceeded")
                    domonic.LAST_ERR = None
                    # raise  # Exception("Recursion limit exceeded") # TODO - cant raise as called by self
                    try:
                        return
                    except Exception as e:
                        raise Exception("Recursion limit exceeded")
                else:
                    domonic.LAST_ERR = str(e)
                # return
                """
                num = int(
                    Utils.digits(str(e))
                )  # go backwards from this line. to the one before it opened
                pyml = pyml.splitlines()

                # NOTE - working backwards from the error line. we try to wrap any content.
                # if already wrapped, we don't want to wrap again. so move back 1 line until we can wrap again
                # this is because a node may take several lines.
                countback = 2
                start_line = pyml[num - countback]
                while "_" not in start_line:
                    countback += 1
                    line = pyml[num - countback]
                    if "html" not in line:
                        start_line = line
                pyml[num - countback] = (
                    start_line + ").html("
                )  # need to know when to close tag comma vs wrap

                # pyml[num - 2] = pyml[num - 2] + ").html(" + str(num)   # need to know when to close tag comma vs wrap
                pyml = "\n".join(pyml)
                return domonic.evaluate(pyml, *args, **kwargs)  # try again

            # TODO -  if " does not match opening parenthesis '{' (<string>, line 9)
            # TODO -  keyword argument repeated (<string>, line 617)
            # keyword argument repeated (<string>, line 3)
            # TODO - invalid syntax (<string>, line 615)
            return pyml

    @staticmethod
    def _safe_eval_pyml(pyml: str, extra_context=None):
        """Evaluate PyML after rejecting expressions outside markup construction."""
        context = {**globals(), **(extra_context or {})}
        tree = ast.parse(pyml, mode="eval")
        if not domonic._is_safe_pyml_ast(tree, context):
            raise ValueError("Unsafe PyML expression")
        code = compile(tree, "<domonic-pyml>", "eval")
        return eval(code, {"__builtins__": {}}, context)  # nosec B307

    @staticmethod
    def _is_safe_pyml_ast(tree, context=None):
        """Return True when a parsed PyML expression contains only inert markup calls."""
        context = context or globals()
        allowed_names = {name for name in context}
        allowed_methods = {"html"}

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr not in allowed_methods:
                        return False
                    continue
                if not isinstance(node.func, ast.Name):
                    return False
                if node.func.id.startswith("__"):
                    return False
                target = context.get(node.func.id)
                if target is None or not callable(target):
                    return False
                continue

            if isinstance(node, ast.Attribute):
                if node.attr not in allowed_methods:
                    return False
                continue

            if isinstance(node, ast.Name):
                if node.id.startswith("__") or node.id not in allowed_names:
                    return False
                continue

            if isinstance(
                node,
                (
                    ast.Expression,
                    ast.Load,
                    ast.Constant,
                    ast.Dict,
                    ast.Tuple,
                    ast.List,
                    ast.Starred,
                    ast.keyword,
                    ast.UnaryOp,
                    ast.UAdd,
                    ast.USub,
                ),
            ):
                continue

            return False

        return True

    @staticmethod
    def _is_valid_pyml(line):
        """
        tests a line
        returns True or False with replacement
        """
        try:
            test_line = line.strip("\n").strip()
            if not test_line:
                return False, ""

            if "(" in test_line:
                test_line = test_line + ")"

            if test_line[0] in ['"', "_", "*"]:
                test_line = "div(" + test_line
                if test_line[len(test_line) - 1] != ")":
                    test_line = test_line + ")"

            if test_line == "),":
                return True, line

            tree = ast.parse(test_line, mode="eval")
            if not domonic._is_safe_pyml_ast(tree):
                return False, ""
            return True, line
        except Exception:
            # print(e)
            # rety fix_hyphen_tags
            if ")" in line:  # if there was a bracket return that at least
                return False, ""
            return False, ""
        return False, ""

    @staticmethod
    def dent(pyml, use_tabs=False):
        """[
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

    @staticmethod
    def parse(
        page: str,
        script_tags=False,
        style_tags=False,
        parse_svg=False,
        minify=False,
        # indent=True,
        remove_broken_lines=False,
    ):
        """
        HTML as input and formats to a domonic_string : the pony he comes

        the result will NOT always be valid .pyml . often params will be in wrong order.
        evaluate can be used to try and resolve param order.
        """
        if not isinstance(page, str):
            raise ValueError("Parse requires a string required not:", type(page))

        # print('parsing parsing parsing!!')

        page = "".join(page.split("<!DOCTYPE HTML>"))
        page = "".join(page.split("<!DOCTYPE html>"))
        page = "".join(page.split("<!doctype html>"))
        page = "".join(page.split("<!doctype HTML>"))

        page = "".join(page.split('<?xml version="1.0" encoding="utf-8"?>'))
        page = "".join(page.split('<?xml version="1.0" encoding="utf-8" ?>'))
        page = "".join(page.split('<?xml version="1.0" encoding="UTF-8" ?>'))

        if not page.strip():
            return ""

        def remove_tag_block(content="", tag_name=""):
            if not content or not tag_name:
                return content

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

        def remove_html_comments(content=""):
            if not content:
                return content

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

        # fully strip inline css and js
        if not script_tags:
            page = remove_tag_block(page, "script")

        if not style_tags:
            page = remove_tag_block(page, "style")

        # fully strip svg and code tags
        # svg = re.compile(r'<(svg).*?</\1>(?s)')
        # page = svg.sub('', page)

        page = remove_tag_block(page, "code")

        page = remove_html_comments(page)
        # page = page.strip('\n').strip()

        # remove abnormal spacing between tag attributes (TODO- maybe 2 spaces is valid somewhere?)
        page = page.replace("   ", " ")
        page = page.replace("  ", " ")
        page = page.replace("  ", " ")

        # special quotes
        page = page.replace("“", "&ldquo;")
        page = page.replace("”", "&rdquo;")

        # Replace reserved characters in text nodes only, leaving tag contents intact.
        def replace_outside_tags(content="", replacements=None):
            if not content or not replacements:
                return content

            result = []
            in_tag = False
            for char in content:
                if char == "<":
                    in_tag = True
                    result.append(char)
                    continue
                if char == ">":
                    in_tag = False
                    result.append(char)
                    continue
                if not in_tag and char in replacements:
                    result.append(replacements[char])
                    continue
                result.append(char)
            return "".join(result)

        page = replace_outside_tags(
            page,
            {
                "(": "$LEFTPARENTHESIS$",
                ")": "$RIGHTPARENTHESIS$",
                "_": "$UNDERSCORE$",
                "-": "$HYPHEN$",
                '"': "$QUOTE$",
                "[": "$LEFTSQUARE$",
                "]": "$RIGHTSQUARE$",
                "=": "$EQUALS$",
                "'": "$SINGLEQUOTE$",
            },
        )

        def encode_content(content=""):
            content = content.replace(")", "$RIGHTPARENTHESIS$")
            content = content.replace("(", "$LEFTPARENTHESIS$")
            content = content.replace("_", "$UNDERSCORE$")
            content = content.replace("-", "$HYPHEN$")
            content = content.replace('"', "$QUOTE$")
            content = content.replace("[", "$LEFTSQUARE$")
            content = content.replace("]", "$RIGHTSQUARE$")
            content = content.replace("=", "$EQUALS$")
            content = content.replace("'", "$SINGLEQUOTE$")
            # content = content.replace(" ", "$SPACE$")
            return content

        def encode_attr_content(content=""):
            content = content.replace(")", "$RIGHTPARENTHESIS$")
            content = content.replace("(", "$LEFTPARENTHESIS$")
            content = content.replace("_", "$UNDERSCORE$")
            content = content.replace("-", "$HYPHEN$")
            content = content.replace('"', "$QUOTE$")
            content = content.replace("[", "$LEFTSQUARE$")
            content = content.replace("]", "$RIGHTSQUARE$")
            content = content.replace("=", "$EQUALS$")
            content = content.replace("'", "$SINGLEQUOTE$")

            content = content.replace(",", "$COMMA$")
            content = content.replace(";", "$SEMICOLON$")

            return content

        # LEFT_CURLY_BRACKET = \u007B
        # OR = \u007C
        # RIGHT_CURLY_BRACKET = \u007D
        # TILDE = \u007E
        # SPACE = \u0020

        # [ # \u005B
        # \ # \u005C
        # ] # \u005D
        # ^ # \u005E
        # _ # \u005F
        # ` # \u0060
        # : # U+003A
        # ; # U+003B
        # < # U+003C
        # = # U+003D
        # > # U+003E
        # ? # U+003F
        # @ # U+0040
        # SPACE = \u0020
        # ! # U+0021
        # " # U+0022
        # # # U+0023
        # $ # U+0024
        # % # U+0025
        # & # U+0026
        # ' # U+0027
        # ( # U+0028
        # ) # U+0029
        # * # U+002A
        # + # U+002B
        # , # U+002C
        # - # U+002D
        # . # U+002E
        # / # U+002F

        tags = html_tags + svg_tags
        tags.sort(key=len, reverse=True)
        for tag in tags:
            page = re.sub(f"<{tag}>", f"\n{tag}(\n", page, flags=re.IGNORECASE)
            page = re.sub(f"<{tag} ", f"\n{tag}(\n", page, flags=re.IGNORECASE)
            page = re.sub(f"</{tag}>", "\n),\n", page, flags=re.IGNORECASE)

            reg = "/>"  # NOTE - er?? this is global!
            pattern = re.compile(reg)
            page = re.sub(pattern, "\n),\n", page)  # , flags=re.IGNORECASE )

        # close any tags that aren't properly self closing
        flag = False
        open_count = 0
        increase_index = 0  # by the amount of new chars you add
        last_tag = None
        for index, char in enumerate(page):
            index = (
                index + increase_index
            )  # TODO does this need to go back to zero.? is any of this code still relevant?
            if char == "(":
                open_count += 1
                flag = open_count > 0
                tag = (
                    page[index - 4]
                    + page[index - 3]
                    + page[index - 2]
                    + page[index - 1]
                )
                last_tag = tag
            if char == ")":
                open_count -= 1
                flag = open_count > 0
            if char == ">":  # and flag is True:
                if (
                    "meta" in tag or "link" in tag or "hr" in tag
                ):  # ??... dont think this is catching anymore
                    page = f"{page[:index]}\n),\n{page[index+1:]}"
                    increase_index += 3
                    open_count -= 1
                    flag = open_count > 0
                    continue
                page = f"{page[:index]},\n{page[index+1:]}"
                increase_index += 1

        attribs = list(attributes)
        attribs.extend(["as", "prefix", "role", "decoding", "typography", "content"])

        solo_attributes = [  # ones that can have no value
            "allowfullscreen",
            "allowpaymentrequest",
            "async",
            "autofocus",
            "autoplay",
            "checked",
            "controls",
            "default",
            "disabled",
            "formnovalidate",
            "hidden",
            "ismap",
            "itemscope",
            "loop",
            "multiple",
            "muted",
            "nomodule",
            "novalidate",
            "open",
            "playsinline",
            "readonly",
            "required",
            "reversed",
            "selected",
            "truespeed",
            "typemustmatch",
            "compact",
            "nohref",
            "noresize",
            "noshade",
            "nowrap",
            "scrolling",
            "seamless",
            "sortable",
            "autocomplete",
            "border",
            "challenge",
            "keyparams",
            "keygen",
            "spellcheck",
            "translate",
            "indeterminate",
        ]

        solo_attributes.append("mozdisallowselectionprint")
        solo_attributes.append("moznomarginboxes")
        solo_attributes.append("crossorigin")

        # adds a comma before special attribute types
        extras = ["data-", "aria-", "accept-charset", "http-"]
        for attr in extras:
            reg = f" {attr}"
            pattern = re.compile(reg)
            page = re.sub(pattern, f", {attr}", page)

        # put underscores on all the attr
        for attr in attribs:
            page = re.sub(f' {attr}="', f' _{attr}="', page, flags=re.IGNORECASE)

        # commas between them
        # for attr in attribs:
        # reg = f' _{attr}="'
        # pattern = re.compile(reg)
        # page = re.sub(pattern, f' _{attr}="', page)

        # TODO - diff between loaded and inline
        # TODO - would have to replace all tags in js (same as content ) (or do opposite way round)
        # get the style and script tags
        # // sure this doesnt' work anymore as we do all tags already?
        htmltags = ["style", "script"]
        for tag in htmltags:
            reg = f"<{tag}>"
            pattern = re.compile(reg)
            page = re.sub(pattern, f'{tag}("""', page)  # , flags=re.IGNORECASE )

            # second pass. atrributed
            reg = f"<{tag}"
            pattern = re.compile(reg)
            page = re.sub(pattern, f'{tag}("""', page)  # , flags=re.IGNORECASE )

            reg = f"</{tag}>"
            pattern = re.compile(reg)
            page = re.sub(pattern, '"""),', page)  # , flags=re.IGNORECASE )

            # reg = '/>'
            # pattern = re.compile(reg)
            # page = re.sub(pattern, '"""),', page)  # , flags=re.IGNORECASE )

        page = "\n)\n".join(
            page.split(",)")
        )  # newline this one?. not sure about this one anymore. seems brutal at this stage

        customtags = re.findall(r"<[-a-zA-Z]+", page)
        if len(customtags) > 0:
            for t in customtags:
                # print(t)
                page = page.replace(
                    t, '\ncreate_element(\n"' + t.lstrip("<") + '"'
                )  # < note. changed to not closing tag

        customtags = re.findall(r"<[/][-a-zA-Z]+", page)
        if len(customtags) > 0:
            for t in customtags:
                # print(t)
                page = page.replace(t, "\n),\n")  # < note. changed to not closing tag

        # any stragglers or custom tags
        page = page.replace("/>", "\n),\n")
        page = page.replace(">", "\n(\n")
        page = page.replace("<", "")

        # print(":::",page)
        # page = page.replace('>', '\n,\n')  # < note. changed to not closing tag
        # page = page.replace('<', '\n(\n')

        # < -------- END OF FIRST PASS

        def fix_hyphen_tags(line):
            # NOTE - bad! as will skip some params
            # if line.count('"') % 2 == 1:
            # return line # its an opening multi-line string so continue.

            values = re.findall('"([^"]*)"', line)
            if len(values) > 0:
                for value in values:
                    line = line.replace(value, encode_attr_content(value))

            values = re.findall("'([^']*)'", line)
            if len(values) > 0:
                for value in values:
                    line = line.replace(value, encode_attr_content(value))

            params = line.replace('" _', '", _')
            params = line.strip().strip(",").strip().split(",")

            for count, each in enumerate(params):
                parts = each.split('="')
                if len(parts) < 2:
                    continue
                key = parts[0].strip()
                val = parts[1].strip()

                if "style" in key or "title" in key:
                    for i, att in enumerate(attributes):
                        val = val.replace(att, "$DoMo" + str(i) + "NiC$")

                # checks string lines have quotes both sides
                if val is None or val == "":
                    val = "true"
                if val == " ":
                    val = '" "'
                if val[-1] not in ['"', ",", "*", ")", "$QUOTE$"]:
                    val = val + '"'
                if val[0] not in ['"', ",", "*", "("]:  # note. added opener.
                    val = '"' + val
                if val == None or val == '"':
                    val = '""'

                val = val.replace("-", "$HYPHEN$")

                if (
                    "_" in key
                ):  # or '_' not in key: # skip as its a single attribute with multiple key:values
                    if (
                        "-" not in key
                    ):  # TODO - may still have to do other ones as below?
                        newparam = f"{key}={val}"
                        params[count] = newparam
                        continue

                if "-" in key:
                    key = key.lstrip(
                        "_"
                    )  # if already has an underscore remove it as we add it below
                    END = ""
                    if len(line) - (line.find(val) + len(val)) < 3:
                        # print('last attribute in line')
                        END = ","

                    newparam = f'**\u007b"_{key}":{val}\u007d{END}'
                    params[count] = newparam
                elif (
                    "_" not in key and "-" not in key
                ):  # i dont think much gets to here then anymore?
                    newparam = f", _{key}={val}"
                    params[count] = newparam

            line = ", ".join(params)
            line = line.replace('" _', '", _')

            if line[len(line) - 1] in [
                "'",
                '"',
                ")",
                "$QUOTE$",
                "}",
                "e",
            ]:  # TODO 'e' is the last letter of True. crap check
                line = line + ","

            return line

        # def replace_between(line, match, replacement, start=0, end=0):
        #     front = line[0:start]
        #     mid = line[start:end]
        #     end = line[end:len(line)]
        #     mid = mid.replace(match, replacement)
        #     newline = front + mid + end
        #     return newline

        def scan_attribute_assignments(line):
            attribs = []
            length = len(line)
            cursor = 0

            while cursor < length:
                while cursor < length and line[cursor].isspace():
                    cursor += 1

                key_start = cursor
                while (
                    cursor < length
                    and not line[cursor].isspace()
                    and line[cursor] not in "=>"
                ):
                    cursor += 1

                if cursor == key_start:
                    cursor += 1
                    continue

                key = line[key_start:cursor]
                scan = cursor
                while scan < length and line[scan].isspace():
                    scan += 1

                if scan >= length or line[scan] != "=":
                    cursor = scan if scan > cursor else cursor + 1
                    continue

                scan += 1
                while scan < length and line[scan].isspace():
                    scan += 1

                if scan >= length:
                    attribs.append((key, ""))
                    cursor = scan
                    continue

                quote = line[scan] if line[scan] in ("'", '"') else None
                if quote:
                    scan += 1
                    value = []
                    escaped = False

                    while scan < length:
                        char = line[scan]
                        if escaped:
                            value.append(char)
                            escaped = False
                        elif char == "\\":
                            value.append(char)
                            escaped = True
                        elif char == quote:
                            break
                        else:
                            value.append(char)
                        scan += 1

                    attribs.append((key, "".join(value)))
                    cursor = scan + 1 if scan < length else scan
                    continue

                value_start = scan
                while scan < length:
                    if line[scan].isspace() or line[scan] == ">":
                        break
                    if (
                        line[scan] == "/"
                        and scan + 1 < length
                        and line[scan + 1] == ">"
                    ):
                        break
                    scan += 1

                attribs.append((key, line[value_start:scan]))
                cursor = scan

            return attribs

        def scan_hyphenated_attribute_tokens(line):
            matches = []
            length = len(line)
            cursor = 0

            while cursor < length:
                if line[cursor] != " ":
                    cursor += 1
                    continue

                start = cursor
                cursor += 1
                token_start = cursor

                if cursor >= length or not (
                    line[cursor].isalpha() or line[cursor] == "_"
                ):
                    continue

                saw_hyphen = False
                while cursor < length:
                    char = line[cursor]
                    if char == "-":
                        saw_hyphen = cursor > token_start
                        cursor += 1
                        continue
                    if char.isalnum() or char == "_":
                        cursor += 1
                        continue
                    break

                token = line[token_start:cursor]
                if saw_hyphen and all(part for part in token.split("-")):
                    matches.append(line[start:cursor])

            return matches

        def parse_attributes(line):

            values = re.findall('"([^"]*)"', line)
            if len(values) > 0:
                for value in values:
                    line = line.replace(value, encode_attr_content(value))

            # import re
            # values = re.findall("'([^']*)'", line)
            # if len(values)>0:
            #     for value in values:
            #         line = line.replace(value,encode_attr_content(value))

            # NOTE - bad! as will skip some params
            if line.count('"') % 2 == 1:
                return line  # its an opening multi-line string so continue.
                # continue

            # prevents single attrib with missing quotes from losing content. (or throw unclean html errors?)(start doing that you'll never stop)
            if line.count("=") < 2:  # if only 1 attr
                if line.count('"') < 1 and line.count("'") < 1:
                    line = line.replace(",", "$COMMA$")
                    parts = line.split("=")
                    line = parts[0] + "=" + '"' + parts[1] + '"'
                    # print(line)

            attribs = scan_attribute_assignments(line)

            if attribs:
                for each in attribs:
                    key = each[0].strip()
                    val = each[1].strip()
                    oldval = val

                    is_quote = lambda x: x == '"' or x == "'"
                    try:
                        has_left_quote = is_quote(line[line.find(val) - 1])
                    except Exception as e:
                        has_right_quote = False

                    try:
                        has_right_quote = is_quote(line[line.find(val) + (len(val))])
                    except Exception as e:
                        has_right_quote = False

                    val = val.replace(
                        '"', "&quot;"
                    )  # they don't always get caught by encode
                    val = val.replace(",", "&#44;")
                    # val = val.replace(';',' &#59;')

                    if "style" in key or "title" in key:
                        for i, att in enumerate(attributes):
                            val = val.replace(att, "$DoMo" + str(i) + "NiC$")

                    if "-" in key and key[0] != "_":
                        line = line.replace(key, "_" + key)
                        continue

                    if "font-size" in key:
                        line = line.replace(
                            "font-size", key
                        )  # update to prepended underscore
                        continue  # these keys are transformed later

                    # val = val.replace("\n", "") # remove newlines in atttribute content as causes EOL when parsing

                    if (
                        len(key) > 20 or "//" in key
                    ):  # data-analytics-exit-link << NOTE 15 limit easilty buckles. bad way to check for content in keys
                        continue

                    # if key not in attributes: # THEN IT MUST BE NORMAL TEXT. strict tho
                    # continue
                    if (
                        key.istitle()
                    ):  # very weak check for normal text TODO. normal text with equals gets through.
                        continue

                    if val == None or val == "":
                        val = "true"

                    newval = ""
                    if type(val) != bool:

                        # checks string lines have quotes both sides
                        if val == None:
                            val = '""'
                        if val == " ":
                            val = '" "'
                        if not has_right_quote:
                            val = val + '"'
                        if not has_left_quote:
                            val = '"' + val
                        if val == None or val == '"':
                            val = '""'

                        newval = val.replace("-", "$HYPHEN$")

                    if "_" not in key and "-" not in key:
                        if ":" in key:  # i.e. xml:"lang=en-US"
                            parts = key.split(":")
                            key = parts[0]
                            if len(parts) > 1:
                                if len(parts[1]) > 1:
                                    newval = parts[1] + "=" + newval
                                    line = line.replace(":" + parts[1], "")

                        line = line.replace(key + "=", ", _" + key + "=")
                        line = line.replace(key + " =", ", _" + key + "=")
                        if type(val) != bool and len(val) > 0:
                            line = Utils.replace_between(
                                line,
                                oldval,
                                str(newval),
                                line.find(key),
                                line.find(key) + (len(key) - 1) + (len(val) - 1) + 1,
                            )  # final +1 is the equal sign

            line = line.replace('" _', '", _')
            line = line.replace("' _", "', _")  # single quote version of same thing
            # line = line.strip()
            return line

        # SECOND PASS. split onto lines and fix hyphen tags
        cleaned = []
        lines = page.splitlines()

        if "doctype" in lines[0].lower():
            lines[0] = ""

        lines_iterator = enumerate(lines)
        for count, line in lines_iterator:
            line = line.strip()
            line = line.replace("    ", " ")
            line = line.replace("   ", " ")
            line = line.replace("  ", " ")
            line = line.replace("  ", " ")

            if len(line) < 1:
                continue

            if line == ",":
                if len(lines[count - 1]) > 0:
                    if lines[count - 1][len(lines[count - 1]) - 1] == ",":
                        continue

            if "=" in line:
                line = parse_attributes(
                    line
                )  # < TODO -  normal content with equals in is getting caught here

                # solo attributes

                # TODO - should really be doing these much sooner no?
                # TODO - breaking class in css content when they have attribute names .i.e. hidden. SORTDE> shoudl be fixed now
                # aria-hidden also affected.?. by why it doing with no spaces
                if (
                    "(" not in line and ")" not in line and line[0] != '"'
                ):  # TODO - not if it already has an equals
                    for each in solo_attributes:
                        pos = line.find(each)
                        # if pos < 1: continue

                        # if the previous attribute has a leading quote already don't prepend one
                        # we assume it doesn't to start.
                        has_leading_quote = False
                        PREP = '"'
                        if pos > 5:
                            # check 4 chars back if quote set false.
                            if (
                                '"' in line[pos - 5 : pos]
                            ):  # TODO - or if just the word True
                                has_leading_quote = True
                            if has_leading_quote:
                                PREP = ""

                        # if solo is first in the line
                        reg = f'^{each} (?=(?:[^"]*"[^"]*")*[^"]*$)'  # space in front. nothing behind
                        pattern = re.compile(reg)
                        line = re.sub(pattern, f"_{each}=True,", line)

                        reg = f' {each}(?=(?:[^"]*"[^"]*")*[^"]*$)'  # space in front. nothing behind
                        pattern = re.compile(reg)
                        line = re.sub(pattern, f"{PREP}, _{each}=True,", line)

                        reg = f'{each},(?=(?:[^"]*"[^"]*")*[^"]*$)'  # with a trailing comma
                        pattern = re.compile(reg)
                        line = re.sub(pattern, f"{PREP}, _{each}=True,", line)

                        reg = f' {each} (?=(?:[^"]*"[^"]*")*[^"]*$)'  # with a trailing space
                        pattern = re.compile(reg)
                        line = re.sub(pattern, f"{PREP}, _{each}=True,", line)

                        reg = f',{each} (?=(?:[^"]*"[^"]*")*[^"]*$)'  # leading comma, with a trailing space
                        pattern = re.compile(reg)
                        line = re.sub(pattern, f"{PREP}, _{each}=True,", line)

                # TODO - custom solo attributes

                line = fix_hyphen_tags(line)

                # any leftover solo hyphenataed data-tags
                hyphenated = scan_hyphenated_attribute_tokens(line)
                for each in hyphenated:
                    line = line.replace(each, f'**\u007b"_{each}":{True}\u007d,')

            # TODO - some attribute content could have open curlies. need to replace all normal text chars
            if "(" not in line[0:10]:
                if ")" not in line[0:2]:
                    # normal text could start with underscore. so could also check for =
                    if "_" not in line:
                        if "-" in line and "=" in line:
                            # its probably a line with hypened a data-tags
                            line = fix_hyphen_tags(line)
                        else:
                            # its regular text content
                            line = encode_content(line)
                            line = f'"{line}"'

            is_multiline_string = False
            if (
                line.count('"') % 2 == 1
            ):  # find opening quotes to multilines (odd number)

                if count < len(lines) - 1:
                    next_line = lines[count + 1]
                if count > 0:
                    prev_line = lines[count - 1]

                # if its just a class and not content. bring them up onto the same line
                if "_class" in line:
                    if "(" not in next_line:  # and '"' not in next_line:
                        line = line + lines.pop(
                            count + 1
                        )  # merge the next line to this one
                        line = line.replace("\n", "")
                        line = line.replace("  ", " ")
                        if line.count('"') % 2 == 1:  # if still odd
                            line = line + '"'  # add a quote
                        next(lines_iterator, None)  # skip the iterator along by 1

                else:
                    if not is_multiline_string == False:
                        x = line.rindex('"')
                        if x:
                            line = line[:x] + '"""' + line[x + 1 :]
                            is_multiline_string = True
                    else:
                        x = line.find('"')
                        if x:
                            line = line[:x] + '""",' + line[x + 1 :]
                            is_multiline_string = False

            cleaned.append(line)
        page = "\n".join(cleaned)

        # a final pass to try check for missing commas between lines by checking 1 line ahead
        fixed = []
        lines = page.splitlines()
        for count, line in enumerate(page.splitlines()):
            line = line.strip("\n")
            line = line.strip()
            if line[len(line) - 1] == '"':
                if count < len(lines) - 1:
                    if lines[count + 1][0] != ")":
                        line = line + ","
            if "_" in line:  # normal text can have underscores. this will break
                line = fix_hyphen_tags(line)

            if (
                len(line) < 5 and '"' in line
            ):  # need to stop making these in first place
                if line == '",",':
                    continue

            fixed.append(line)
        page = "\n".join(fixed)

        def clean_junk(page):
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

        page = clean_junk(page)
        # page = clean_junk(page)
        # clean_junk(page)

        # put content text back to normal
        page = page.replace("$RIGHTPARENTHESIS$", ")")
        page = page.replace("$LEFTPARENTHESIS$", "(")
        page = page.replace("$UNDERSCORE$", "_")
        page = page.replace("$HYPHEN$", "-")
        page = page.replace("$QUOTE$", "&quot;")
        page = page.replace("$LEFTSQUARE$", "[")
        page = page.replace("$RIGHTSQUARE$", "]")
        page = page.replace("$EQUALS$", "=")
        page = page.replace("$SINGLEQUOTE$", "'")
        page = page.replace("$COMMA$", ",")
        page = page.replace("$SEMICOLON$", ";")

        for count, att in enumerate(attributes):
            page = page.replace(
                "$DoMo" + str(count) + "NiC$", att
            )  # undo encoding that saves attr content

        if remove_broken_lines:
            print("attempting to remove broken lines")
            fixed = []
            for count, line in enumerate(page.splitlines()):
                line = line.strip("\n")
                is_fixed, newline = domonic._is_valid_pyml(line)
                if is_fixed:
                    fixed.append(newline)
                else:  # break line into bits to keep any working parts
                    # print("BAD:", line)
                    parts = line.split(",")
                    keepers = []
                    for piece in parts:
                        piece = piece.strip()
                        piece = piece.strip("\n")
                        is_working, p = domonic._is_valid_pyml(piece)
                        # print(is_working,p)
                        if is_working:
                            keepers.append(p)
                    line = ",".join(keepers)
                    is_fixed, newline = domonic._is_valid_pyml(line + ",")
                    if is_fixed:
                        fixed.append(newline)
                        # print("FIXED:", line)
            page = "\n".join(fixed)

        # page = ''.join(page.splitlines())
        # page = ''.join(page.splitlines())

        # if not minify and indent:
        #     print('>>',len(page))
        # page = domonic.dent(page)
        #     print('<<',len(page))

        return page

    parseString_prev_error = None

    @staticmethod
    def parseString(string, parser=None):
        """Parse a file into a DOM from a string."""
        parser = (parser or domonic.DEFAULT_PARSER or "auto").lower()

        def _upgrade_custom_elements(page):
            try:
                from domonic.window import window as domonic_window

                domonic_window.customElements.upgrade(page)
            except Exception:
                return page
            return page

        def _looks_like_full_html_document(source: str) -> bool:
            probe = source.lstrip().lower()
            return (
                probe.startswith("<!doctype")
                or probe.startswith("<html")
                or "<html" in probe[:512]
            )

        def _normalize_parsed_page(page, source: str):
            is_full_document = _looks_like_full_html_document(source)

            if isinstance(page, dom.DocumentFragment):
                return page

            html_root = None
            if getattr(page, "tagName", "").lower() == "html":
                html_root = page
            else:
                for child in getattr(page, "childNodes", []) or []:
                    if getattr(child, "tagName", "").lower() == "html":
                        html_root = child
                        break

            if html_root is None:
                return page

            if is_full_document:
                return html_root

            body = (
                html_root.querySelector("body")
                if hasattr(html_root, "querySelector")
                else None
            )
            container = body if body is not None else html_root
            children = list(getattr(container, "childNodes", []) or [])
            if len(children) == 1:
                return children[0]
            if len(children) > 1:
                return dom.Document.createDocumentFragment(*children)
            return dom.Document.createDocumentFragment()

        def _parse_with_html5lib():
            import html5lib  # noqa: F401
            from html5lib import HTMLParser

            from domonic.ext.html5lib_ import getTreeBuilder

            html_parser = HTMLParser(tree=getTreeBuilder())
            if _looks_like_full_html_document(string):
                page = html_parser.parse(string)
            else:
                page = html_parser.parseFragment(string)
            return _upgrade_custom_elements(_normalize_parsed_page(page, string))

        def _parse_with_html5_parser():
            from domonic.ext.html5_parser_ import parse as html5_parser_parse

            page = html5_parser_parse(string, treebuilder="domonic", return_root=False)
            return _upgrade_custom_elements(_normalize_parsed_page(page, string))

        def _parse_with_lxml_html():
            from domonic.ext.lxml_html_ import parse as lxml_html_parse

            page = lxml_html_parse(string, return_root=False)
            return _upgrade_custom_elements(_normalize_parsed_page(page, string))

        def _parse_with_markupever():
            from domonic.ext.markupever_ import parse as markupever_parse

            page = markupever_parse(string, return_root=False)
            return _upgrade_custom_elements(_normalize_parsed_page(page, string))

        def _parse_with_selectolax():
            from domonic.ext.selectolax_ import parse as selectolax_parse

            page = selectolax_parse(string, return_root=False)
            return _upgrade_custom_elements(_normalize_parsed_page(page, string))

        def _parse_with_justhtml():
            from domonic.ext.justhtml_ import parse as justhtml_parse

            page = justhtml_parse(string, return_root=False)
            return _upgrade_custom_elements(_normalize_parsed_page(page, string))

        if parser == "html5lib":
            return _parse_with_html5lib()
        if parser in ("lxml_html", "lxml-html"):
            return _parse_with_lxml_html()
        if parser in ("html5_parser", "html5-parser"):
            return _parse_with_html5_parser()
        if parser == "markupever":
            return _parse_with_markupever()
        if parser == "selectolax":
            return _parse_with_selectolax()
        if parser == "justhtml":
            return _parse_with_justhtml()
        if parser == "expat":
            from domonic.parsers import expatbuilder

            page = expatbuilder.parseString(string)
            return _upgrade_custom_elements(_normalize_parsed_page(page, string))
        if parser != "auto":
            raise ValueError(f"Unknown parser: {parser}")

        # TODO - this needs to be off for debugging
        fallback_parsers = (
            (_parse_with_html5lib, (ImportError,)),
            (_parse_with_lxml_html, (Exception,)),
            (_parse_with_html5_parser, (Exception,)),
            (_parse_with_justhtml, (Exception,)),
            (_parse_with_markupever, (Exception,)),
            (_parse_with_selectolax, (Exception,)),
        )
        for parse_with, handled_errors in fallback_parsers:
            try:
                return parse_with()
            except handled_errors:
                continue

        try:
            from domonic.parsers import expatbuilder

            page = expatbuilder.parseString(string)
            return _upgrade_custom_elements(_normalize_parsed_page(page, string))
        except Exception as e:
            # TODO - problem with this method. is it takes literally forever.
            # as it removes 1 char then reparses entire doc. even on small pages this is a problem.
            dodgycharIndex = int(Utils.digits(str(e).split(",")[1]))
            # string[int(dodgycharIndex)-1] = Utils.escape(string[int(dodgycharIndex)-1])
            dodgyChar = string[int(dodgycharIndex) - 1]
            string = Utils.replace_between(
                string, dodgyChar, "", dodgycharIndex - 2, dodgycharIndex + 2
            )
            if domonic.parseString_prev_error != dodgycharIndex:
                domonic.parseString_prev_error = dodgycharIndex
                return domonic.parseString(string, parser="expat")
            else:
                return None

        # else:
        # from xml.dom import pulldom
        # return _do_pulldom_parse(pulldom.parseString, (string,),
        # {'parser': parser})
