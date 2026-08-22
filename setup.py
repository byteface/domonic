"""Packaging configuration for domonic."""

import os
import re

from setuptools import find_packages, setup

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def read(filename: str) -> str:
    """Returns the contents of a file.

    Args:
        filename (str): The name of the file to read.

    Returns:
        str: content of the file
    """
    with open(os.path.join(BASE_DIR, filename), encoding="utf-8") as file:
        return file.read()


def get_version() -> str:
    """Read the package version without importing domonic during setup."""
    version_file = read(os.path.join("domonic", "__init__.py"))
    match = re.search(r'^__version__\s*=\s*"([^"]+)"', version_file, re.MULTILINE)
    if not match:
        raise RuntimeError("Unable to find package version.")
    return match.group(1)


def get_requirements(filename: str = "requirements.txt"):
    """returns a list of all requirements"""
    requirements = read(filename)
    return list(
        filter(
            None,
            [req.strip() for req in requirements.split() if not req.startswith("#")],
        )
    )

setup(
    name="domonic",
    version=get_version(),
    author="byteface",
    author_email="byteface@gmail.com",
    license="MIT",
    url="https://github.com/byteface/domonic",
    project_urls={
        "Documentation": "https://domonic.readthedocs.io/",
        "Source": "https://github.com/byteface/domonic",
        "Tracker": "https://github.com/byteface/domonic/issues",
        "Examples": "https://github.com/byteface/domonic/tree/master/examples",
        "Releases": "https://github.com/byteface/domonic/releases",
        "Changelog": "https://github.com/byteface/domonic/blob/master/CHANGELOG.md",
        "Contributing": "https://github.com/byteface/domonic/blob/master/CONTRIBUTING.md",
        "Security": "https://github.com/byteface/domonic/blob/master/SECURITY.md",
    },
    description=(
        "Python DOM toolkit for HTML generation, SVG/XML, CSS selectors, XPath, "
        "Web APIs, and JavaScript-like scripting."
    ),
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    keywords=[
        "aframe",
        "browser api",
        "cli",
        "css selectors",
        "cssom",
        "custom elements",
        "dom manipulation",
        "dom",
        "events",
        "feed generator",
        "html builder",
        "html generator",
        "html parser",
        "html tags",
        "html templating",
        "html",
        "html5",
        "javascript runtime",
        "javascript",
        "json",
        "mathml",
        "mutation observer",
        "python dom",
        "python html",
        "rss",
        "scraping",
        "server side rendering",
        "shadow dom",
        "static site",
        "svg",
        "templating",
        "urlpattern",
        "vdom",
        "web api",
        "web components",
        "web",
        "whatwg",
        "xpath",
        "x3d",
        "xml",
    ],
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Other Audience",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Multimedia :: Graphics :: Presentation",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Markup",
        "Topic :: Software Development",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Terminals",
        "Topic :: Utilities",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Text Processing :: Markup :: XML",
    ],
    install_requires=get_requirements(),
    packages=find_packages(exclude=("tests", "tests.*")),
    include_package_data=True,
    license_files=("LICENSE.txt",),
    entry_points={
        "console_scripts": [
            "domonic = domonic.__main__:run",
        ],
    },
)
