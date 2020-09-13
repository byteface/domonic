"""
    domonic CLI
    ====================================
    - some useful cli commands
"""

import argparse


def parse_args():
    parser = argparse.ArgumentParser(add_help=False, prog="domonic", usage="%(prog)s [options]", description="Generate HTML with Python 3")
    parser.add_argument('-a', '--assets', help="generate as assets directory with common files", action='store_true')
    parser.add_argument('-d', '--download', help="Attempts to to generate domonic template from a webpage", type=str)
    # parser.add_argument('-t', '--tree', default=False, help="generate a tree view from a component", type=str)
    parser.add_argument('-h', '--help', action='store_true')  # launch the docs
    parser.add_argument('-v', '--version', action='store_true')  # launch the docs

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


if __name__ == "__main__":
    args = parse_args()
    do_things(args)
