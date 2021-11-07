Contributing to domonic
=======================

Welcome! domonic is an open-source project that aims to work for a wide
range of users and codebases. If you're using domonic your experience
is important to the project's success.

It's probably more fun to clone and download domonic than it is to pip install it. 

I'd encourage you to download and play. If you do manage to improve it
in even the smallest way, please feel free to send a pull request.

Small commits are good. You can even fork, edit and submit a pull request
all within github without even downloading the repo. In just 3 or 4 simple steps.

But for a full setup keep reading.

Getting started, building, and testing
--------------------------------------

If you haven't already, take a look at the project's

[README.md file](README.md)

and [domonic documentation](https://readthedocs.org/projects/domonic/),

The readme contains some tips on running tests.

For dev you will need to install the requirements-dev.txt file.

clone the repo an cd into it.

setup a virtual environment

```bash
python3 -m venv venv
. venv/bin/activate
pip install -r requirements-dev.txt
```

and you should be good to go.

The Makefile can be used to run all tests.

```bash
make test
```

or you can run tests just for a single module.

```python
python3 -m unittest tests.test_html
python3 -m unittest tests.test_dom
python3 -m unittest tests.test_style
python3 -m unittest tests.test_javascript
python3 -m unittest tests.test_terminal
python3 -m unittest tests.test_CDN
python3 -m unittest tests.test_JSON
python3 -m unittest tests.test_svg
python3 -m unittest tests.test_collada
python3 -m unittest tests.test_x3d
python3 -m unittest tests.test_dQuery
python3 -m unittest tests.test_geom
python3 -m unittest tests.test_d3
python3 -m unittest tests.test_sitemap
python3 -m unittest tests.test_domonic
python3 -m unittest tests.test_templates
```

Discussion
----------

If you found a bug or think something should behave differently we want to hear from you!

Our forum for discussion is the project's 
[GitHub issue tracker](https://github.com/byteface/domonic/issues) or 
[discussion board](https://github.com/byteface/domonic/discussions)

For less formal discussion send me a message or join the discord server.

Code of Conduct
-----------------------

Everyone contributing to domonic, and in particular in our
issue tracker, pull requests, is expected to treat other people with respect.

First Time Contributors
-----------------------

I appreciates your contribution! If you are interested in helping improve
domonic, there are several ways to get started:

* Docs - learn to publish the sphinx docs and make some small edits.

```bash
cd docs
make html
```

* Unit Test - These are severely lacking and writing them uncovers bugs. Try to start everthing you are doing with tests.

Submitting Changes
------------------

Ideally you can make a fork and submit a pull request and I'll try to review it and add the udpates as soon as possible to a release.

Try to do unit tests if you can and add new ones to the test files if you need to. There is usually a test file for each class or package.

The best thing is to commit little and often. single functions and unit tests. Making sure all existing tests pass (unless they were incorrect).

Preparing Changes
-----------------

Before you begin: if your change will be a significant amount of work
to write, we highly recommend starting by opening an issue laying out
what you want to do.  That lets a conversation happen early in case
other contributors disagree with what you'd like to do or have ideas
that will help you do it.

I'd like to get the conventions as good as possbile but it's a big project with a lot to do.

I'm severly behind on unit tests and documentation.

If you want you can also raise a bug and suggest a fix as a comment. If you have patched something locally and just want to suggest the change but don't feel confident setting everything up just put a message dicussion board.

Issue-tracker conventions
-------------------------

I aim to reply to all issues promptly but I may not be able for somethings or might be busy so please also be patient.

Thanks
-------------------------

domonic has benefitted also from bug fixes and features by other people.

I'd like to thank here...

* William MacMillan - wmacmillan
* Jordan Cottle - Jordan-Cottle
* Alfas Esty - alfasst
* Kristian Thy - kthy

and of course dependabot[bot]
