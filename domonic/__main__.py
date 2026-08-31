"""
domonic CLI
====================================
- some useful cli commands
"""

import argparse
import os
import subprocess  # nosec B404
import sys

from domonic.ext import get_hello_world, get_server_requirements, get_supported_servers

prog = """

function project(){
    PROJECT_NAME=$1
    mkdir $PROJECT_NAME
    cd $PROJECT_NAME

    mkdir static
    mkdir static/js
    mkdir static/css
    mkdir static/img
    mkdir static/data

    mkdir archive
    touch app.py
    echo "from domonic.html import *" >> app.py

    touch Makefile

    touch README.md
    echo "# $PROJECT_NAME" >> README.md
    echo "## Description" >> README.md
    echo "## Installation" >> README.md
    echo "## Usage" >> README.md
    echo "## Tests" >> README.md
    echo "## License" >> README.md

    mkdir app
    touch app/__init__.py
    echo '__version__ = "0.0.1"' >> app/__init__.py

    git init
    touch .gitignore
    echo "*.pyc" >> .gitignore
    echo "*.pyo" >> .gitignore
    echo "*.swp" >> .gitignore
    echo "*.swo" >> .gitignore
    echo "*.DS_Store" >> .gitignore
    echo "__pycache__/" >> .gitignore

    touch static/js/master.js
    touch static/css/styles.css
    touch static/data/data.json

    python3 -m venv venv
    . venv/bin/activate

    pip3 install requests
    pip3 install sanic
    pip3 install domonic
    pip3 freeze >> requirements.txt

    chmod -R 777 static
    open .
}

"""


def _open_directory(path: str = ".") -> None:
    if sys.platform.startswith("darwin"):
        subprocess.run(["open", path], check=False)  # nosec B603 B607
        return

    if sys.platform.startswith("linux"):
        for command in (["xdg-open", path], ["nautilus", path]):
            try:
                subprocess.run(command, check=False)  # nosec B603
                return
            except FileNotFoundError:
                continue
        return

    if os.name == "nt":
        os.startfile(path)  # nosec B606


def _read_source(source: str | None, use_stdin: bool = False) -> str:
    if use_stdin:
        return sys.stdin.read()
    if source is None:
        raise ValueError("A source URL or file path is required")
    if os.path.exists(source):
        with open(source, encoding="utf-8") as handle:
            return handle.read()
    import requests

    response = requests.get(source, timeout=30)
    return response.text


def _emit_results(
    results,
    *,
    text_only: bool = False,
    attr_name: str | None = None,
    count_only: bool = False,
    first_only: bool = False,
):
    items = list(results)
    if first_only:
        items = items[:1]
    if count_only:
        print(len(items))
        return len(items)

    rendered: list[str] = []
    for item in items:
        if attr_name is not None:
            value = getattr(item, attr_name, None)
            if value is None and hasattr(item, "getAttribute"):
                value = item.getAttribute(attr_name)
            if value is not None:
                rendered.append(str(value))
                print(value)
            continue
        if text_only:
            value = getattr(item, "textContent", None)
            if callable(value):
                value = value()
            if value is None:
                value = str(item)
            rendered.append(str(value))
            print(value)
            continue
        rendered.append(str(item))
        print(item)
    return rendered


def project(name, server_choice: str | None = None):
    """
    this will replace the older bash script
    """
    from domonic.utils import Utils

    server_opt = get_supported_servers()

    if (
        server_choice is not None
        and server_choice not in server_opt
        and server_choice != "none"
    ):
        raise ValueError(
            f"Unsupported server '{server_choice}'. Supported servers: {', '.join(server_opt)}"
        )

    def write_requirements(server: str) -> list[str]:
        requirements = ["domonic", "requests", *get_server_requirements(server)]
        with open("requirements.txt", "w") as requirements_file:
            requirements_file.write("\n".join(requirements) + "\n")
        return requirements

    def write_activation_script(server: str) -> None:
        requirements = write_requirements(server)
        install_commands = [
            "python3 -m pip install --upgrade pip",
            "python3 -m pip install -r requirements.txt",
        ]

        if Utils.is_windows():
            with open("activate.bat", "w") as script:
                script.write("@echo off\n")
                script.write('call "venv\\Scripts\\activate"\n')
                for command in install_commands:
                    script.write(f"{command}\n")
            os.system("activate.bat")  # nosec B605 B607
            os.remove("activate.bat")
        else:
            with open("activate.sh", "w") as script:
                script.write("#!/bin/bash\n")
                script.write("source venv/bin/activate\n")
                for command in install_commands:
                    script.write(f"{command}\n")
            os.system("bash activate.sh")  # nosec B605 B607
            os.remove("activate.sh")

    PROJECT_NAME = name
    os.mkdir(PROJECT_NAME)
    os.chdir(PROJECT_NAME)

    # create a Makefile
    # os.system("touch Makefile")
    with open("Makefile", "w") as f:
        # start venv and run app
        # f.write(". venv/bin/activate\n")
        # f.write("python3 app.py\n")
        # TOD as a run command
        f.write("""
run:
\t(. venv/bin/activate; python3 app.py;)
""")

    # create a README.md
    with open("README.md", "w") as f:
        f.write("# " + PROJECT_NAME + "\n")
        f.write("## Description\n")
        f.write("## Installation\n")
        f.write("## Usage\n")
        f.write("## Tests\n")
        f.write("## License")

    # create app
    os.mkdir("app")
    with open("app/__init__.py", "w") as f:
        f.write('__version__ = "0.0.1"')

    # create a git repo
    os.system("git init")  # nosec B605 B607
    with open(".gitignore", "w") as f:
        f.write("*.pyc\n")
        f.write("*.pyo\n")
        f.write("*.swp\n")
        f.write("*.swo\n")
        f.write("*.DS_Store\n")
        f.write("__pycache__/\n")

    # create a venv
    # os.system("python3 -m venv venv")
    # if os.name == "nt":
    #     os.system("venv\Scripts\activate")
    # else:
    #     os.system("source venv/bin/activate")
    # # install requirements
    # os.system("python3 -m pip install requests")
    # os.system("python3 -m pip install sanic")
    # os.system("python3 -m pip install domonic")
    # os.system("python3 -m pip freeze > requirements.txt")

    # ask the user which server they want to use
    if server_choice is None:
        print("You want a server?")
        for i, server in enumerate(server_opt):
            print(str(i) + ": " + server)
        server_choice = input("Enter a number: ")
        try:
            server_choice = server_opt[int(server_choice)]
        except (IndexError, ValueError):
            if server_choice in server_opt:
                server_choice = server_choice
            else:
                server_choice = "none"
    # with python not touch
    with open("app.py", "w") as f:
        # write the hello world for the given server
        code = get_hello_world(server_choice)
        if code is not None:
            f.write(code)
        else:
            f.write("from domonic.html import *")

    os.system("python3 -m venv venv")  # nosec B605 B607
    write_activation_script(server_choice)

    # license_opt = ["none", "mit", "gpl", "apache", "bsd", "mpl"]
    # for i, license in enumerate(license_opt):
    # license_choice = input("Enter a number: ")
    # license_choice = license_opt[int(license_choice)]
    # dl the license

    # create static
    os.mkdir("static")
    os.mkdir("static/js")
    os.mkdir("static/css")
    os.mkdir("static/img")
    os.mkdir("static/data")

    # create files
    with open("static/js/master.js", "w") as f:
        f.write("")
    with open("static/css/styles.css", "w") as f:
        f.write("")
    with open("static/data/data.json", "w") as f:
        f.write("")

    # chmod
    if os.name == "posix":
        os.system("chmod -R 777 static")  # nosec B605 B607

    _open_directory(".")


# def webpage(content):
#     from domonic.components import webpage_tmpl
#     with open("index.html", "w") as f:
#         f.write(webpage_tmpl(content))


def parse_args():
    parser = argparse.ArgumentParser(
        add_help=False,
        prog="domonic",
        usage="%(prog)s [options]",
        description="Generate HTML with Python 3",
    )
    parser.add_argument(
        "-h",
        "--help",
        help="Opens the online docs in your default browser",
        action="store_true",
    )
    parser.add_argument("-v", "--version", action="store_true")
    parser.add_argument("-p", "--project", help="Create a new project", type=str)
    parser.add_argument(
        "--server",
        help="Choose the project server non-interactively",
        type=str,
        default=None,
    )
    parser.add_argument(
        "-e",
        "--eval",
        help="Evaluates a domonic pyml string and returns html",
        type=str,
    )  # default=sys.stdin, nargs='*')

    parser.add_argument(
        "-a",
        "--assets",
        help="Generate an assets directory with common files",
        action="store_true",
    )
    parser.add_argument(
        "-d",
        "--download",
        help="Attempts to to generate domonic template from a webpage",
        type=str,
    )
    parser.add_argument(
        "-x",
        "--xpath",
        help="pass a url and an xpath",
        type=str,
        nargs="*",
        default=None,
    )
    parser.add_argument(
        "-q",
        "--query",
        help="pass a url and a css query",
        type=str,
        nargs="*",
        default=None,
    )
    parser.add_argument(
        "--xpath-file",
        help="pass a local HTML file and an xpath",
        type=str,
        nargs=2,
        default=None,
    )
    parser.add_argument(
        "--query-file",
        help="pass a local HTML file and a css query",
        type=str,
        nargs=2,
        default=None,
    )
    parser.add_argument(
        "--xpath-stdin",
        help="read HTML from stdin and apply an xpath",
        type=str,
        default=None,
    )
    parser.add_argument(
        "--query-stdin",
        help="read HTML from stdin and apply a css query",
        type=str,
        default=None,
    )
    parser.add_argument(
        "--text", help="print text content instead of node markup", action="store_true"
    )
    parser.add_argument(
        "--attr",
        help="print a specific attribute from each result",
        type=str,
        default=None,
    )
    parser.add_argument(
        "--count", help="print only the number of matches", action="store_true"
    )
    parser.add_argument(
        "--first", help="print only the first match", action="store_true"
    )
    parser.add_argument(
        "--parser",
        help="parser backend for CLI HTML input, e.g. selectolax, turbohtml, lxml_html, html.parser",
        type=str,
        default=None,
    )
    parser.add_argument(
        "-h2p",
        "--html2pyml",
        help="Convert HTML to PyML",
        type=str,
        nargs="?",
        default=None,
    )

    # parser.add_argument('-u', '--ui', help="launches a UI")
    # parser.add_argument('-p', '--pyml2html', help="converts a .pyml template file to html", type=str)

    # parser.add_argument('-w', '--website', action='store_true')  # launch the docs
    # parser.add_argument('-s', '--server', help="runs python -m http.server", type=str)
    # parser.add_argument('-u', '--url', help="url to launch the server", type=str)

    # parser.add_argument('-j', '--csv2json', help="converts a csv file to a json file", type=str)
    # parser.add_argument('-c', '--json2csv', help="converts a json file to a csv file", type=str)
    # parser.add_argument('-m', '--merge', help="merges two csv files", type=str)
    # parser.add_argument('-d', '--diff', help="compares two csv files", type=str)
    # parser.add_argument('-t', '--table', help="creates a table from a csv file", type=str)
    # parser.add_argument('-r', '--replace', help="replaces a value in a csv file", type=str)

    # parser.add_argument('-c', '--json2ini', help="converts a json file to an ini file", type=str)
    # parser.add_argument('-i', '--ini2json', help="converts an ini file to a json file", type=str)
    # parser.add_argument('-m', '--merge', help="merges two ini files", type=str)

    # -- ideas
    # -- change all file extensions. from, to
    # -- generate assets/app/license/readme/sitemap.

    args = parser.parse_args()
    return args


def do_things(arguments):
    from domonic.terminal import TerminalException

    def _resolve_source_and_expression(values, label: str):
        if values is None:
            return None
        if len(values) == 2:
            return values[0], values[1], False
        if len(values) == 1 and not sys.stdin.isatty():
            return None, values[0], True
        raise ValueError(
            f"{label} expects exactly 2 arguments: a URL and an expression. "
            f"If piping HTML in, pass just the expression."
        )

    try:
        if arguments.assets is True:
            from domonic.utils import Utils

            Utils.init_assets()
            # --license,readme,sitemap,requirements
    except TerminalException as e:
        print(e)

    if arguments.download is not None:
        print("creating domonic template from url:")
        from domonic import domonic

        page = domonic.get(arguments.download)

        from domonic.html import render
        from domonic.utils import Utils

        print("filename:", Utils.url2file(arguments.download))
        render(page, Utils.url2file(arguments.download))

    if arguments.html2pyml is not None:
        print("creating domonic code from url:")
        from domonic import domonic

        page = domonic.get(arguments.html2pyml)
        outp = domonic.parseString(page, parser=arguments.parser)

        from domonic.html import render
        from domonic.utils import Utils

        print(render(outp, to="pyml"))

    if arguments.project is not None:
        print("creating a basic project:")
        project(arguments.project, arguments.server)

    if arguments.help is True:
        import webbrowser

        webbrowser.open_new("https://domonic.readthedocs.io/")

    if arguments.version is True:
        from domonic import __version__

        print(__version__)
        return __version__

    if arguments.eval is not None:
        import domonic

        result = f"{domonic.domonic.domonify(arguments.eval)}"
        print(result)
        return result

    if (
        arguments.xpath is not None
        or arguments.xpath_file is not None
        or arguments.xpath_stdin is not None
    ):
        from domonic import domonic
        from domonic.webapi.xpath import XPathEvaluator, XPathResult

        source: str | None = None
        xpath: str
        use_stdin = False
        if arguments.xpath is not None:
            source, xpath, use_stdin = _resolve_source_and_expression(
                arguments.xpath, "xpath"
            )
        elif arguments.xpath_file is not None:
            source, xpath = arguments.xpath_file
        else:
            xpath = arguments.xpath_stdin
            use_stdin = True

        page = domonic.parseString(
            _read_source(source, use_stdin), parser=arguments.parser
        )
        evaluator = XPathEvaluator()
        expression = evaluator.createExpression(xpath)
        result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        return _emit_results(
            result.nodes,
            text_only=arguments.text,
            attr_name=arguments.attr,
            count_only=arguments.count,
            first_only=arguments.first,
        )

    if (
        arguments.query is not None
        or arguments.query_file is not None
        or arguments.query_stdin is not None
    ):
        query: str
        if arguments.query is not None:
            source, query, use_stdin = _resolve_source_and_expression(
                arguments.query, "query"
            )
            from domonic import domonic

            page = domonic.parseString(
                _read_source(source, use_stdin), parser=arguments.parser
            )
            results = page.querySelectorAll(query)
        else:
            from domonic import domonic

            if arguments.query_file is not None:
                source, query = arguments.query_file
                page = domonic.parseString(
                    _read_source(source), parser=arguments.parser
                )
            else:
                query = arguments.query_stdin
                page = domonic.parseString(
                    _read_source(None, True), parser=arguments.parser
                )
            results = page.querySelectorAll(query)

        return _emit_results(
            results,
            text_only=arguments.text,
            attr_name=arguments.attr,
            count_only=arguments.count,
            first_only=arguments.first,
        )

    # if arguments.server is True:
    # port = domonic.get(arguments.server)
    # os.system('python -m http.server ' + port)


def run():
    """[Entry point required by setup.py console_scripts. Saves having to add alias to .bash_profile]"""
    args = parse_args()
    do_things(args)


if __name__ == "__main__":
    run()
