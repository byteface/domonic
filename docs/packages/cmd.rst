cmd
=================

The ``cmd`` package calls Windows commands from Python.

This package only works on Windows systems because it delegates to ``subprocess``.

.. code-block :: python

	from domonic.cmd import *

	print(dir())

	print(mkdir('somedir'))
	print(touch('somefile'))

	for file in dir():
	    print("Line : ", file)


Run Arbitrary Commands
--------------------------------

.. code-block :: python

	from domonic.cmd import Cmdcommand
	Cmdcommand.run("echo hi")


Take a look at the code in `cmd.py` to see the available command wrappers.


.. automodule:: domonic.cmd
    :members:
    :noindex:
