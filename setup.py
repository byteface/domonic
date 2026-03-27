"""Packaging configuration for domonic."""

import os
import re

from setuptools import find_packages, setup


def read(filename: str) -> str:
    """Returns the contents of a file.

    Args:
        filename (str): The name of the file to read.

    Returns:
        str: content of the file
    """
    with open(filename, encoding="utf-8") as file:
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
    },
    description="A Python DOM far beyond minidom, with HTML, SVG, events, web APIs, and a JavaScript-like runtime.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    keywords=[
        "html",
        "generate",
        "templating",
        "dom",
        "vdom",
        "terminal",
        "json",
        "web",
        "template",
        "javascript",
        "DOM",
        "GUI",
        "render",
        "website",
        "apps",
        "html5",
        "framework",
        "SVG",
        "x3d",
        "events",
        "geom",
        "whatwg",
        "web api",
        "custom elements",
        "shadow dom",
        "css selectors",
        "html parser",
        "animation",
        "dom manipulation",
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
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Multimedia :: Graphics :: Presentation",
        "Topic :: Software Development",
        "Topic :: Software Development :: Code Generators",
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
