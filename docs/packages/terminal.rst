terminal
=================

.. meta::
   :description: Python terminal command wrappers for Bash, Unix, POSIX, subprocess workflows, shell scripts, and CLI automation.
   :keywords: Python terminal, shell commands, subprocess wrapper, Bash from Python, Unix commands, CLI automation

The terminal package calls Bash, Unix, POSIX, Git, and other command-line tools
from Python. It is useful for small build scripts, local automation, examples,
and command-line experiments that should stay close to shell syntax.

Basic Commands
--------------

.. code-block :: python

	from domonic.terminal import date, df, du, echo, ls, pwd

	print(pwd())
	print(ls())
	print(ls("-al"))
	print(echo("hello"))
	print(date())
	print(df())
	print(du())

Small Automation Scripts
------------------------

.. code-block :: python

	from domonic.terminal import grep, ls, pwd

	print("cwd:", pwd())
	print("python files:", ls("*.py"))

	print(grep("domonic README.md"))

Git and Build Helpers
---------------------

.. code-block :: python

	from domonic.terminal import git, make

	print(git("status", "--short"))
	print(make("--version"))

Run Arbitrary Commands
----------------------

.. code-block :: python

	from domonic.terminal import command

	print(command.run("echo hi"))

.. automodule:: domonic.terminal
    :members:
    :noindex:
