Domonic: cmd
=================

There is a cmd package for calling windows commands within python3

This package only works on windows systems as it effectively just passes stuff off to subprocess.

.. code-block :: python

	from domonic.cmd import *

	print(dir())

	print(mkdir('somedir'))
	print(touch('somefile'))

	for file in dir():
	    print("Line : ", file)


run arbitrary commands...
--------------------------------

.. code-block :: python

	from domonic.cmd import Cmdcommand
	command.run("echo hi")


Take a look at the code in 'cmd.py' to see all the commands. (Disclaimer: not tested.)


.. automodule:: domonic.cmd
    :members:
    :noindex:

