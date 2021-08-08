"""
    domonic
    ====================================

    API for creating and loading .pyml

"""

__version__ = "0.4.4"
__license__ = 'MIT'
__author__ = "@byteface"

'''
__uri__ = "https://github.com/byteface/domonic"
# https://domonic.readthedocs.io/
__title__ = 'domonic'
__description__ = 'Generate HTML with python 3'

__all__ = (
    '__version__',
    '__license__',
    '__uri__',
    '__title__',
    '__description__'
)
'''
# TITLE = __title__
VERSION = __version__
# LICENSE = __license__

import requests
import re

from domonic.svg import *
from domonic.html import *
from domonic.html import html_attributes as attributes
from domonic.javascript import *

from domonic.utils import Utils
from domonic.components import Input

class domonic:

    JS_MASTER = "assets/js/master.js"
    CSS_STYLE = "assets/css/style.css"


    @staticmethod
    def get(url: str):
        """ downloads html and converts to domonic """
        r = requests.get(url)
        return domonic.parse(r.content.decode("utf-8"))
        # TODO - param to eval

    @staticmethod
    def loads(path: str, *args, **kwargs):
        """ [
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
        """ [
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
        return prog

    @staticmethod  # load replaces this.
    def domonify(pyml: str, *args, **kwargs):
        """ [
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

        print("HI>>", pyml)

        s = domonic.evaluate(pyml, *args, **kwargs)

        # NOTE - valid chunks of pyml can still not eval if they are not wrapped
        # i.e. a list not in aa ul or ol. when on single line evaulate will fix
        # but on mulitple lines it will not.
        try:
            p = eval(s, {**kwargs, **globals()})
        except Exception as e:
            print("Failed to evaluate as mulitline trying again:", e)
            pyml = ''.join(pyml.splitlines())  # try again on a single line 
            s = domonic.evaluate(pyml, *args, **kwargs)
            p = eval(s, {**kwargs, **globals()})

        return p

    @staticmethod
    def evaluate(pyml: str, *args, **kwargs):
        """ [
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
            # TODO - strip any potentially bad/dangerous code before eval.
            p = eval(pyml, {**kwargs, **globals()})
            return pyml  # ????
        except Exception as e:
            # import sys
            # old_log = sys.stdout
            # log_file = open("fail.log","w")
            # sys.stdout = log_file
            print(e)
            # sys.stdout = old_log

            # if end of file err. add a closed curly
            if "EOF" in str(e):
                # unexpected EOF while parsing (<string>, line 471)
                err = str(e)
                if str(len(pyml.splitlines())) in err:
                    pyml += ")"
                    return domonic.evaluate(pyml)  # try again

            if "positional argument follows keyword argument" in str(e):
                # print(e)
                num = str(e).split('line')[1]
                if ')' in num:
                    num = num.split(')')[0]
                num = num.strip()
                num = int(num)
                pyml = pyml.splitlines()
                pyml[num - 2] = pyml[num - 2] + ").html("  # need to know when to close tag comma vs wrap
                pyml = '\n'.join(pyml)
                # print(pyml)
                return domonic.evaluate(pyml) # try again
                # pass
                # pyml += ").html("
                # domonic.domonify(pyml) # try again  s and load   

            # TODO -  if " does not match opening parenthesis '{' (<string>, line 9)
            # TODO -  keyword argument repeated (<string>, line 617)
            # keyword argument repeated (<string>, line 3)
            # TODO - invalid syntax (<string>, line 615)
            print('Eval failed! you will have to modify the output manually')
            return pyml

    @staticmethod
    def _is_valid_pyml(line):
        """
        tests a line. 
        returns True or False with replacement
        """
        try:
            test_line = line.strip('\n').strip()

            if '(' in line:
                test_line = line + ')'

            if line[0] in ['"', "_", "*"]:
                test_line = "div(" + line
                if test_line[len(test_line)-1] != ')':
                    test_line = test_line + ')'

            if line == "),":
                return True, line

            # print(test_line)
            l = eval(test_line)
            # print('PASS:', line)
            return True, line
        except Exception as e:
            print(test_line)
            print('FAIL:', line, e)
            # print(e)
            # rety fix_hyphen_tags
            if ')' in line: # if there was a bracket return that at least
                return False, ""
            return False, ""
        return False, ""


    @staticmethod
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
            if lastchar == "\n": # TODO - if file doesn't have newlines already
                char = tabs_or_spaces * dentage + char
            lastchar = char
            dented += char
            if dentage < 0:
                dentage = 0
        return dented


    @staticmethod
    def parse(  page: str,
                script_tags=False,
                style_tags=False,
                parse_svg=False,
                minify=False,
                # indent=True,
                remove_broken_lines=False):
        """
        HTML as input and formats to a domonic_string : the pony he comes

        the result will NOT always be valid .pyml . often params will be in wrong order.
        evaluate can be used to try and resolve param order.
        """
        if not isinstance(page, str):
            raise ValueError("Parse requires a string required not:", type(page))

        # print('parsing parsing parsing!!')

        page = ''.join(page.split('<!DOCTYPE HTML>'))
        page = ''.join(page.split('<!DOCTYPE html>'))
        page = ''.join(page.split('<!doctype html>'))
        page = ''.join(page.split('<!doctype HTML>'))

        page = ''.join(page.split('<?xml version="1.0" encoding="utf-8"?>'))
        page = ''.join(page.split('<?xml version="1.0" encoding="utf-8" ?>'))
        page = ''.join(page.split('<?xml version="1.0" encoding="UTF-8" ?>'))

        # fully strip inline css and js
        if not script_tags:
            scripts = re.compile(r'<(script).*?</\1>(?s)')
            page = scripts.sub('', page)

        if not style_tags:
            css = re.compile(r'<(style).*?</\1>(?s)')
            page = css.sub('', page)

        # fully strip svg and code tags
        # svg = re.compile(r'<(svg).*?</\1>(?s)')
        # page = svg.sub('', page)

        code = re.compile(r'<(code).*?</\1>(?s)')
        page = code.sub('', page)

        comments = re.compile(r'<!--(.|\s)*?-->')
        page = comments.sub('', page)
        # page = page.strip('\n').strip()


        # remove abnormal spacing between tag attributes (TODO- maybe 2 spaces is valid somewhere?)
        page = page.replace('   ', ' ')
        page = page.replace('  ', ' ')
        page = page.replace('  ', ' ')

        # special quotes
        page = page.replace('“', '&ldquo;')
        page = page.replace('”', '&rdquo;')

        # REPLACE ANY STRINGS WE MATCH ON (NOT CONTAINED IN TAGS.
        REGY = re.compile(r'(\u0028)(?![^<>]*>)')
        page = REGY.sub('$LEFTPARENTHESIS$', page)

        REGY = re.compile(r'(\u0029)(?![^<>]*>)')
        page = REGY.sub('$RIGHTPARENTHESIS$', page)

        REGY = re.compile(r'(\u005F)(?![^<>]*>)')
        page = REGY.sub('$UNDERSCORE$', page)

        REGY = re.compile(r'(U+002D)(?![^<>]*>)')
        page = REGY.sub('$HYPHEN$', page)

        REGY = re.compile(r'(U+002D)(?![^<>]*>)')
        page = REGY.sub('$QUOTE$', page)

        REGY = re.compile(r'(U+u005B)(?![^<>]*>)')
        page = REGY.sub('$LEFTSQUARE$', page)

        REGY = re.compile(r'(U+u005D)(?![^<>]*>)')
        page = REGY.sub('$RIGHTSQUARE$', page)

        REGY = re.compile(r'(U+u003D)(?![^<>]*>)')
        page = REGY.sub('$EQUALS$', page)

        REGY = re.compile(r'(U+0027)(?![^<>]*>)')
        page = REGY.sub('$SINGLEQUOTE$', page)

        def encode_content(content=""):
            content = content.replace(")", "$RIGHTPARENTHESIS$")
            content = content.replace("(", "$LEFTPARENTHESIS$")
            content = content.replace("_", "$UNDERSCORE$")
            content = content.replace("-", "$HYPHEN$")
            content = content.replace('"', "$QUOTE$")
            content = content.replace('[', "$LEFTSQUARE$")
            content = content.replace(']', "$RIGHTSQUARE$")
            content = content.replace('=', "$EQUALS$")
            content = content.replace("'", "$SINGLEQUOTE$")
            # content = content.replace(" ", "$SPACE$")
            return content

        def encode_attr_content(content=""):
            content = content.replace(")", "$RIGHTPARENTHESIS$")
            content = content.replace("(", "$LEFTPARENTHESIS$")
            content = content.replace("_", "$UNDERSCORE$")
            content = content.replace("-", "$HYPHEN$")
            content = content.replace('"', "$QUOTE$")
            content = content.replace('[', "$LEFTSQUARE$")
            content = content.replace(']', "$RIGHTSQUARE$")
            content = content.replace('=', "$EQUALS$")
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
            page = re.sub(f"<{tag}>", f'\n{tag}(\n', page, flags=re.IGNORECASE)
            page = re.sub(f"<{tag} ", f'\n{tag}(\n', page, flags=re.IGNORECASE)
            page = re.sub(f"</{tag}>", '\n),\n', page, flags=re.IGNORECASE)

            reg = '/>' # NOTE - er?? this is global!
            pattern = re.compile(reg)
            page = re.sub(pattern, '\n),\n', page)  # , flags=re.IGNORECASE )

        # close any tags that aren't properly self closing
        flag = False
        open_count = 0
        increase_index = 0  # by the amount of new chars you add
        last_tag = None
        for index, char in enumerate(page):
            index = index + increase_index # TODO does this need to go back to zero.? is any of this code still relevant?
            if char == "(":
                open_count +=1
                flag = (open_count>0)
                tag = page[index - 4] + page[index - 3] + page[index - 2] + page[index - 1]
                last_tag = tag
            if char == ")":
                open_count -=1
                flag = (open_count>0)
            if char == ">":# and flag is True:
                if 'meta' in tag or 'link' in tag or 'hr' in tag: #??... dont think this is catching anymore
                    page = f"{page[:index]}\n),\n{page[index+1:]}"
                    increase_index += 3
                    open_count -=1
                    flag = (open_count>0)
                    continue
                page = f'{page[:index]},\n{page[index+1:]}'
                increase_index += 1

        attribs = attributes
        attribs.append('as')
        attribs.append('prefix')
        attribs.append('role')
        attribs.append('decoding')
        attribs.append('typography')
        attribs.append('content')

        solo_attributes = [  # ones that can have no value
            "allowfullscreen", "allowpaymentrequest", "async", "autofocus", "autoplay", "checked", "controls", "default",
            "disabled", "formnovalidate", "hidden", "ismap", "itemscope", "loop", "multiple", "muted", "nomodule", "novalidate",
            "open", "playsinline", "readonly", "required", "reversed", "selected", "truespeed", "typemustmatch", "compact",
            "nohref", "noresize", "noshade", "nowrap", "scrolling", "seamless", "sortable", "autocomplete", "border", "challenge",
            "keyparams", "keygen", "spellcheck", "translate", "indeterminate"]

        solo_attributes.append('mozdisallowselectionprint')
        solo_attributes.append('moznomarginboxes')
        solo_attributes.append('crossorigin')

        # adds a comma before special attribute types
        extras = ['data-', 'aria-', 'accept-charset', "http-"]
        for attr in extras:
            reg = f' {attr}'
            pattern = re.compile(reg)
            page = re.sub(pattern, f', {attr}', page)

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
        #// sure this doesnt' work anymore as we do all tags already?
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

        page = '\n)\n'.join(page.split(',)')) # newline this one?. not sure about this one anymore. seems brutal at this stage

        customtags = re.findall(r'<[-a-zA-Z]+', page)
        if len(customtags) > 0:
            for t in customtags:
                # print(t)
                page = page.replace(t, '\ncreate_element(\n"' + t.lstrip('<') + '"')  # < note. changed to not closing tag

        customtags = re.findall(r'<[/][-a-zA-Z]+', page)
        if len(customtags) > 0:
            for t in customtags:
                # print(t)
                page = page.replace(t, '\n),\n')  # < note. changed to not closing tag

        # any stragglers or custom tags
        page = page.replace('/>', '\n),\n')
        page = page.replace('>', '\n(\n')
        page = page.replace('<', '')


        # print(":::",page)

        # page = page.replace('>', '\n,\n')  # < note. changed to not closing tag
        # page = page.replace('<', '\n(\n')

        # < -------- END OF FIRST PASS

        def fix_hyphen_tags(line):
            # NOTE - bad! as will skip some params
            # if line.count('"') % 2 == 1:
                # return line # its an opening multi-line string so continue.

            values = re.findall('"([^"]*)"', line)
            if len(values)>0:
                for value in values:
                    line = line.replace(value,encode_attr_content(value))

            values = re.findall("'([^']*)'", line)
            if len(values)>0:
                for value in values:
                    line = line.replace(value,encode_attr_content(value))

            params = line.replace('" _','", _')
            params = line.strip().strip(',').strip().split(',')

            for count, each in enumerate(params):
                parts = each.split('="')
                if len(parts) < 2:
                    continue
                key = parts[0].strip()
                val = parts[1].strip()

                if 'style' in key or 'title' in key:
                    for i, att in enumerate(attributes):
                        val = val.replace(att, '$DoMo'+str(i)+'NiC$')

                # checks string lines have quotes both sides
                if val is None or val == "":
                    val = 'true'
                if val == ' ':
                    val = '" "'
                if val[-1] not in ['"',",","*",")","$QUOTE$"]:
                    val = val+'"'
                if val[0] not in ['"',",","*","("]: # note. added opener.
                    val = '"'+val
                if val == None or val == '"':
                    val = '""'

                val = val.replace("-", "$HYPHEN$")

                if '_' in key:  # or '_' not in key: # skip as its a single attribute with multiple key:values
                    if '-' not in key: # TODO - may still have to do other ones as below?
                        newparam = f'{key}={val}'
                        params[count] = newparam
                        continue

                if '-' in key:
                    key = key.lstrip('_')  # if already has an underscore remove it as we add it below
                    END = ""
                    if len(line) - (line.find(val)+len(val)) < 3:
                        # print('last attribute in line')
                        END = ","

                    newparam = f'**\u007b"_{key}":{val}\u007d{END}'
                    params[count] = newparam
                elif '_' not in key and '-' not in key:  # i dont think much gets to here then anymore?
                    newparam = f', _{key}={val}'
                    params[count] = newparam

            line = ', '.join(params)
            line = line.replace('" _', '", _')

            if( line[len(line)-1] in ["'",'"',")","$QUOTE$","}","e"]): # TODO 'e' is the last letter of True. crap check
                line = line + ","

            return line

        # def replace_between(line, match, replacement, start=0, end=0):
        #     front = line[0:start]
        #     mid = line[start:end]
        #     end = line[end:len(line)]
        #     mid = mid.replace(match, replacement)
        #     newline = front + mid + end
        #     return newline

        def parse_attributes(line):

            values = re.findall('"([^"]*)"', line)
            if len(values)>0:
                for value in values:
                    line = line.replace(value,encode_attr_content(value))

            # import re
            # values = re.findall("'([^']*)'", line)
            # if len(values)>0:
            #     for value in values:
            #         line = line.replace(value,encode_attr_content(value))

            # NOTE - bad! as will skip some params
            if line.count('"') % 2 == 1:
                return line # its an opening multi-line string so continue.
                #continue

            # prevents single attrib with missing quotes from losing content. (or throw unclean html errors?)(start doing that you'll never stop)
            if line.count('=')<2: # if only 1 attr
                if line.count('"')<1 and line.count("'")<1:
                    line = line.replace( ',', '$COMMA$')
                    parts = line.split('=')
                    line = parts[0] + "=" + '"'+parts[1]+'"'
                    # print(line)

            attribs = re.findall(r"((?:(?!\s|=).)*)\s*?=\s*?[\"']?((?:(?<=\")(?:(?<=\\)\"|[^\"])*|(?<=')(?:(?<=\\)'|[^'])*)|(?:(?!\"|')(?:(?!\/>|>|\s).)+))", line)

            if attribs:
                for each in attribs:
                    key = each[0].strip()
                    val = each[1].strip()
                    oldval = val

                    is_quote = lambda x : x == '"' or x == "'"
                    try:
                        has_left_quote = is_quote(line[line.find(val)-1])
                    except Exception as e:
                        has_right_quote = False

                    try:
                        has_right_quote = is_quote(line[line.find(val)+(len(val))])
                    except Exception as e:
                        has_right_quote = False

                    val = val.replace('"','&quot;') # they don't always get caught by encode
                    val = val.replace(',','&#44;')
                    # val = val.replace(';',' &#59;')

                    if 'style' in key or 'title' in key:
                        for i, att in enumerate(attributes):
                            val = val.replace( att, '$DoMo'+str(i)+'NiC$')

                    if '-' in key and key[0] != '_':
                        line = line.replace(key,'_'+key)
                        continue

                    if 'font-size' in key:
                        line = line.replace('font-size', key)# update to prepended underscore
                        continue # these keys are transformed later

                    # val = val.replace("\n", "") # remove newlines in atttribute content as causes EOL when parsing

                    if len(key)>20 or '//' in key: # data-analytics-exit-link << NOTE 15 limit easilty buckles. bad way to check for content in keys
                        continue

                    # if key not in attributes: # THEN IT MUST BE NORMAL TEXT. strict tho
                       # continue
                    if key.istitle(): # very weak check for normal text TODO. normal text with equals gets through.
                        continue

                    if val==None or val=="":
                        val = 'true'

                    newval=""
                    if type(val) != bool:

                        # checks string lines have quotes both sides
                        if val == None:
                            val = '""'
                        if val == ' ':
                            val = '" "'
                        if not has_right_quote:
                            val = val+'"'
                        if not has_left_quote:
                            val = '"'+val
                        if val == None or val == '"':
                            val = '""'

                        newval = val.replace("-", "$HYPHEN$")

                    if '_' not in key and '-' not in key:
                        if ':' in key: # i.e. xml:"lang=en-US"
                            parts = key.split(':')
                            key = parts[0]
                            if len(parts)>1:
                                if len(parts[1])>1:
                                    newval = parts[1] + "=" + newval
                                    line = line.replace(":"+parts[1],"")

                        line = line.replace(key+"=",', _'+key+"=")
                        line = line.replace(key+" =",', _'+key+"=")
                        if type(val) != bool and len(val)>0:
                            line = Utils.replace_between( line, oldval, str(newval), line.find(key), line.find(key)+(len(key)-1)+(len(val)-1)+1 )# final +1 is the equal sign

            line = line.replace('" _', '", _')
            line = line.replace("' _", "', _") # single quote version of same thing
            # line = line.strip()
            return line


        # SECOND PASS. split onto lines and fix hyphen tags
        cleaned = []
        lines = page.splitlines()

        if 'doctype' in lines[0].lower():
            lines[0] = ""

        lines_iterator = enumerate(lines)
        for count, line in lines_iterator:
            line = line.strip()
            line = line.replace('    ', ' ')
            line = line.replace('   ', ' ')
            line = line.replace('  ', ' ')
            line = line.replace('  ', ' ')

            if len(line) < 1:
                continue

            if line == ",":
                if len(lines[count-1])>0:
                    if lines[count-1][len(lines[count-1])-1] == ',':
                        continue

            if '=' in line:
                line = parse_attributes(line) # < TODO -  normal content with equals in is getting caught here

                # solo attributes

                # TODO - should really be doing these much sooner no?
                # TODO - breaking class in css content when they have attribute names .i.e. hidden. SORTDE> shoudl be fixed now
                # aria-hidden also affected.?. by why it doing with no spaces
                if '(' not in line and ')' not in line and line[0] != '"': # TODO - not if it already has an equals
                    for each in solo_attributes:
                        pos=line.find(each)
                        # if pos < 1: continue

                        # if the previous attribute has a leading quote already don't prepend one
                        # we assume it doesn't to start.
                        has_leading_quote = False
                        PREP = '"'
                        if pos>5:
                            # check 4 chars back if quote set false.
                            if '"' in line[pos-5:pos]: # TODO - or if just the word True
                                has_leading_quote = True
                            if has_leading_quote:
                                PREP = ''

                        # if solo is first in the line
                        reg = f'^{each} (?=(?:[^"]*"[^"]*")*[^"]*$)'  # space in front. nothing behind
                        pattern = re.compile(reg)
                        line = re.sub(pattern, f'_{each}=True,', line)

                        reg = f' {each}(?=(?:[^"]*"[^"]*")*[^"]*$)'  # space in front. nothing behind
                        pattern = re.compile(reg)
                        line = re.sub(pattern, f'{PREP}, _{each}=True,', line)

                        reg = f'{each},(?=(?:[^"]*"[^"]*")*[^"]*$)'  # with a trailing comma
                        pattern = re.compile(reg)
                        line = re.sub(pattern, f'{PREP}, _{each}=True,', line)

                        reg = f' {each} (?=(?:[^"]*"[^"]*")*[^"]*$)'  # with a trailing space
                        pattern = re.compile(reg)
                        line = re.sub(pattern, f'{PREP}, _{each}=True,', line)

                        reg = f',{each} (?=(?:[^"]*"[^"]*")*[^"]*$)'  # leading comma, with a trailing space
                        pattern = re.compile(reg)
                        line = re.sub(pattern, f'{PREP}, _{each}=True,', line)

                # TODO - custom solo attributes

                line = fix_hyphen_tags(line)

                # any leftover solo hyphenataed data-tags
                hyphenated = re.findall(r' [-A-Za-z]+\w+(?:-\w+)+',line)
                for each in hyphenated:
                    line = line.replace(each, f'**\u007b"_{each}":{True}\u007d,')

            # TODO - some attribute content could have open curlies. need to replace all normal text chars
            if '(' not in line[0:10]:
                if ')' not in line[0:2]:
                    # normal text could start with underscore. so could also check for =
                    if '_' not in line:
                        if '-' in line and '=' in line:
                            # its probably a line with hypened a data-tags
                            # line = fix_hyphen_tags(line)
                            pass
                        else:
                            # its regular text content
                            line = encode_content(line)
                            line = f'"{line}"'

            is_multiline_string = False
            if line.count('"') % 2 == 1: # find opening quotes to multilines (odd number)

                if count < len(lines)-1:
                    next_line = lines[count+1]
                if count > 0:
                    prev_line = lines[count-1]

                # if its just a class and not content. bring them up onto the same line
                if '_class' in line:
                    if '(' not in next_line: # and '"' not in next_line:
                        line = line + lines.pop(count+1) # merge the next line to this one
                        line = line.replace('\n', "")
                        line = line.replace("  ", " ")
                        if line.count('"') % 2 == 1: # if still odd
                            line = line + '"' # add a quote
                        next(lines_iterator, None) # skip the iterator along by 1

                else:
                    if is_multiline_string == False:
                        x = line.rindex('"')
                        if x:
                            line = line[:x] + '"""' + line[x + 1:]
                            is_multiline_string = True
                    else:
                        x = line.find('"')
                        if x:
                            line = line[:x] + '""",' + line[x + 1:]
                            is_multiline_string = False

            cleaned.append(line)
        page = '\n'.join(cleaned)

        # a final pass to try check for missing commas between lines by checking 1 line ahead
        fixed = []
        lines = page.splitlines()
        for count, line in enumerate(page.splitlines()):
            line = line.strip('\n')
            line = line.strip()
            if line[len(line)-1] == '"':
                if count < len(lines)-1:
                    if lines[count+1][0] != ')':
                        line = line + ','
            if "_" in line:  # normal text can have underscores. this will break
                line = fix_hyphen_tags(line)

            if len(line)<5 and '"' in line: # need to stop making these in first place
                if line == '",",':
                    continue

            fixed.append(line)
        page = '\n'.join(fixed)


        def clean_junk(page):        
            page = page.replace('",","', '","')
            page = page.replace('",",', '",')
            page = page.replace('", ",', '",')
            page = page.replace('", \n",', '",')
            page = page.replace('",\n ",', '",')
            page = page.replace('","\n)', '"\n)')
            page = page.replace('", \n, _', '",\n_')
            page = page.replace(', "\n)', '\n)')

            # page = page.replace(',",', ',') < VALID
            page = page.replace(',  ,', ',') # < new bug. due to single attributes having big space in front for some reason
            page = page.replace(', ",', ',')
            page = page.replace(',,', ',')
            page = page.replace(', ,', ',')
            page = page.replace(',"",', ',') # careul. new and covers up somethings else. solo attributes still not done well

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

            page = page.replace('"_, _', '"_') # when solo hyphenated custom attribute is first on a line.

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
        page = page.replace("$QUOTE$", '&quot;')
        page = page.replace("$LEFTSQUARE$", '[')
        page = page.replace("$RIGHTSQUARE$", ']')
        page = page.replace("$EQUALS$", '=')
        page = page.replace("$SINGLEQUOTE$", "'")
        page = page.replace("$COMMA$", ",")
        page = page.replace("$SEMICOLON$", ";")

        for count, att in enumerate(attributes):
            page = page.replace('$DoMo'+str(count)+'NiC$', att) # undo encoding that saves attr content

        if remove_broken_lines:
            print('attempting to remove broken lines')
            fixed=[]
            for count, line in enumerate(page.splitlines()):
                line = line.strip('\n')
                is_fixed, newline = domonic._is_valid_pyml(line)
                if is_fixed:
                    fixed.append(newline)
                else: # break line into bits to keep any working parts
                    # print("BAD:", line)
                    parts = line.split(',')
                    keepers = []
                    for piece in parts:
                        piece = piece.strip()
                        piece = piece.strip('\n')
                        is_working, p = domonic._is_valid_pyml(piece)
                        # print(is_working,p)
                        if is_working:
                            keepers.append(p)
                    line = ','.join(keepers)
                    is_fixed, newline = domonic._is_valid_pyml(line+",")
                    if is_fixed:
                        fixed.append(newline)
                        # print("FIXED:", line)
            page = '\n'.join(fixed)

        # page = ''.join(page.splitlines())
        # page = ''.join(page.splitlines())

        # if not minify and indent:
        #     print('>>',len(page))
        # page = domonic.dent(page)
        #     print('<<',len(page))

        return page
