"""
    domonic CLI
    ====================================
    - some useful cli commands
"""

import argparse


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

    if arguments.server is True:
        # import sys
        # sys.argv = ['python', '-m', 'http.server']
        # sys.argv.extend(['--bind', '0.0.0.0', '8000'])
        # sys.call_command('http.server')
        import os   
        os.system('python -m http.server 8000 --bind 0.0.0.0')
        # from http.server import HTTPServer, SimpleHTTPRequestHandler
        # import socketserver
        # PORT = 8000
        # httpd = socketserver.TCPServer(("", PORT), SimpleHTTPRequestHandler)
        # print("serving at port", PORT)
        # httpd.serve_forever()




if __name__ == "__main__":
    args = parse_args()
    do_things(args)
