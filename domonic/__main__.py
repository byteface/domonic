"""
    domonic CLI
    ====================================
    - some useful cli commands
"""

import argparse
import os


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
    touch README.md
    touch MakeFile

    mkdir app
    touch app/__init__.py

    git init
    touch .gitignore

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


# class domonic_ui(object):
#     """
#         domonic UI - browser interface to create pyml via contextmenu clicks?.
#     """
#     def __init__(self):
#         pass



def parse_args():
    parser = argparse.ArgumentParser(add_help=False, prog="domonic", usage="%(prog)s [options]", description="Generate HTML with Python 3")
    parser.add_argument('-a', '--assets', help="generate as assets directory with common files", action='store_true')
    parser.add_argument('-d', '--download', help="Attempts to to generate domonic template from a webpage", type=str)
    parser.add_argument('-h', '--help', action='store_true')  # launch the docs
    parser.add_argument('-v', '--version', action='store_true')
    # parser.add_argument('-u', '--ui', help="launches a UI")

    parser.add_argument('-i', '--install', action='store_true')  # add 'projects' to the .bashprofile or .bashrc

    # parser.add_argument('-w', '--website', action='store_true')  # launch the docs
    # parser.add_argument('-s', '--server', help="runs python -m http.server", type=str)
    # parser.add_argument('-u', '--url', help="url to launch the server", type=str)
    
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

    if arguments.help is True:
        import webbrowser
        webbrowser.open_new("https://domonic.readthedocs.io/")

    if arguments.version is True:
        from domonic import __version__
        print(__version__)
        return __version__

    # if arguments.server is True:
        # port = domonic.get(arguments.server)
        # os.system('python -m http.server ' + port)

    if arguments.install is True:
        # detect operating system and attempts to append prog to the .bashprofile or .bashrc
        if os.name == 'nt':
            print('Sorry, this install is currently unavaialable for windows')
        else:

            # detect if the user has a bashrc or bashprofile
            if os.path.exists(os.path.expanduser('~/.bashrc')):

                # dont do it if alreay exists
                if 'function project()' not in open(os.path.expanduser('~/.bashrc')).read():
                    print('found .bashrc')
                    with open(os.path.expanduser('~/.bashrc'), 'a') as f:
                        f.write('\n\n# domonic\n')
                        f.write(prog)
                        f.write('alias domonic="python3 -m domonic"\n')
                else:
                    print('already installed. You need to manually remove it from ~/.bashrc')
        
            elif os.path.exists(os.path.expanduser('~/.bash_profile')):

                if 'function project()' not in open(os.path.expanduser('~/.bash_profile')).read():
                    print('found .bash_profile')
                    with open(os.path.expanduser('~/.bash_profile'), 'a') as f:
                        f.write('\n\n# domonic\n')
                        f.write(prog)
                        f.write('alias domonic="python3 -m domonic"\n')
                else:
                    print('already installed. You need to manually remove it from ~/.bash_profile')

            else:
                print('no bashrc or bash_profile found. you need to manually add the following to your .bashrc or .bash_profile')
                print(prog)



if __name__ == "__main__":
    args = parse_args()
    do_things(args)



# def install():