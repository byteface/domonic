cmd
=================

.. meta::
   :description: Windows command prompt helpers for Python, including dir, copy, move, erase, type, comp, and portable shell command wrappers.
   :keywords: Python Windows commands, cmd.exe wrapper, dir copy move erase, subprocess helper, cross-platform command wrappers

The ``cmd`` package calls Windows-style commands from Python. On Windows it
delegates to the native command names. On other platforms, common commands such
as ``dir``, ``copy``, ``move``, ``erase``, ``type_``, and ``comp`` are translated
to Unix equivalents so examples and tests remain portable.

List Files
----------

.. code-block :: python

	from domonic.cmd import dir

	for file in dir():
	    print(file)

Portable File Commands
----------------------

The wrappers return command output in a Python-friendly form where possible.

.. code-block :: python

	from domonic.cmd import copy, dir, mkdir

	mkdir("reports")
	copy("README.md", "reports/README.txt")

	print(dir("reports"))
	# README.txt

Windows-Friendly Scripts
------------------------

Use this module when you want examples or teaching scripts to read like Windows
``cmd.exe`` commands while still being testable on Unix-like CI.

.. code-block :: python

	from domonic.cmd import erase, move, rename

	rename("reports/README.txt", "readme-copy.txt")
	move("readme-copy.txt", "reports/readme-copy.txt")
	erase("reports/readme-copy.txt")

Run Arbitrary Commands
----------------------

.. code-block :: python

	from domonic.cmd import Cmdcommand

	print(Cmdcommand.run("echo hi"))
	# hi
	print(Cmdcommand.run_args(["echo", "hi"]))
	# hi

.. automodule:: domonic.cmd
    :members:
    :noindex:
