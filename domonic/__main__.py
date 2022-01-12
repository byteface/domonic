"""
    domonic CLI
    ====================================
    - some useful cli commands
"""

import argparse
import os
import sys

prog = '''

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

'''
# TODO - nautilus instead of open for linux
# wrewrite as pure python


def project(name):
    """
    this will replace the older bash script
    """
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
    os.system("git init")
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
    server_opt = ["none", "sanic", "flask", "cherrypy", "django", "bottle", "pyramid", "werkzeug", "tornado", "aiohttp", "fastapi", "starlette", "blacksheep", "muffin", "falcon", "baize", "emmett", "quart"]
    print("You want a server?")
    for i, server in enumerate(server_opt):
        print(str(i) + ": " + server)
    server_choice = input("Enter a number: ")
    try:
        server_choice = server_opt[int(server_choice)]
    except ValueError:
        if server_choice in server_opt:
            server_choice = server_choice

    # TODO - any plugins?.. cors etc

    # with python not touch
    with open("app.py", "w") as f:
        # write the hello world for the given server
        from domonic.ext import get_hello_world
        code = get_hello_world(server_choice)
        if code is not None:
            f.write(code)
        else:
            f.write("from domonic.html import *")

    os.system("python3 -m venv venv")
    from domonic.utils import Utils
    if Utils.is_windows():
        # create a bat file to activate the venv an install requirements
        with open("activate.bat", "w") as f:
            f.write("@echo off\n")
            f.write("call \"venv\Scripts\activate\"\n")
            f.write("python3 -m pip install requests\n")
            if server_choice != 'none':
                f.write(f"python3 -m pip install {server_choice}\n")
            f.write("python3 -m pip install domonic\n")
            f.write("python3 -m pip freeze > requirements.txt\n")
        # call the bat file
        os.system("activate.bat")
        # remove the activate.bat file
        os.system("del activate.bat")
    else:
        # create a bash file to activate the venv an install requirements
        with open("activate.sh", "w") as f:
            f.write("#!/bin/bash\n")
            f.write("source venv/bin/activate\n")
            f.write("python3 -m pip install requests\n")
            if server_choice != 'none':
                f.write(f"python3 -m pip install {server_choice}\n")
            f.write("python3 -m pip install domonic\n")
            f.write("python3 -m pip freeze > requirements.txt\n")
        # call the bash file
        os.system("bash activate.sh")
        # remove the activate.sh file
        os.system("rm activate.sh")

    # license_opt = ["none", "mit", "gpl", "apache", "bsd", "mpl"]
    # print("You want a license?")
    # for i, license in enumerate(license_opt):
    #     print(str(i) + ": " + license)
    # license_choice = input("Enter a number: ")
    # license_choice = license_opt[int(license_choice)]
    # dl the license

    # create static
    # TODO - build asset folders based on server choice.
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
    if os.name == 'posix':
        os.system("chmod -R 777 static")

    if Utils.is_mac():
        os.system("open .")
    elif Utils.is_linux():
        os.system("nautilus .")
    elif Utils.is_windows():
        # TODO - check what to do on windows
        os.system("start .")
        # explorer.exe .?
        # os.system("explorer.exe .")

# def webpage(content):
#     from domonic.components import webpage_tmpl
#     with open("index.html", "w") as f:
#         f.write(webpage_tmpl(content))


def parse_args():
    parser = argparse.ArgumentParser(add_help=False,
                                     prog="domonic",
                                     usage="%(prog)s [options]",
                                     description="Generate HTML with Python 3")
    parser.add_argument('-h', '--help', help="Opens the online docs in your default browser", action='store_true')
    parser.add_argument('-v', '--version', action='store_true')
    parser.add_argument('-p', '--project', help="Create a new project", type=str)
    parser.add_argument('-e', '--eval', help="Evaluates a domonic pyml string and returns html", type=str)  # default=sys.stdin, nargs='*')

    parser.add_argument('-a', '--assets', help="Generate an assets directory with common files", action='store_true')
    parser.add_argument('-d', '--download', help="Attempts to to generate domonic template from a webpage", type=str)

    # parser.add_argument('-u', '--ui', help="launches a UI")
    # parser.add_argument('-p', '--pyml2html', help="converts a .pyml template file to html", type=str)
    # parser.add_argument('-g', '--html2pyml', help="converts a .html file to a .pyml template", type=str)

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
    try:
        if arguments.assets is True:
            from domonic.utils import Utils
            Utils.init_assets()
            # --license,readme,sitemap,requirements
    except TerminalException as e:
        print(e)

    # print(arguments.download)
    if arguments.download is not None:
        print('creating domonic template from url:')
        from domonic import domonic
        page = domonic.get(arguments.download)

        from domonic.html import render
        from domonic.utils import Utils
        print("filename:", Utils.url2file(arguments.download))
        render(page, Utils.url2file(arguments.download))

    if arguments.project is not None:
        print('creating a basic project:')
        project(arguments.project)

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

    # if arguments.server is True:
        # port = domonic.get(arguments.server)
        # os.system('python -m http.server ' + port)


def run():
    """[Entry point required by setup.py console_scripts. Saves having to add alias to .bash_profile]
    """
    args = parse_args()
    do_things(args)


if __name__ == "__main__":
    run()
