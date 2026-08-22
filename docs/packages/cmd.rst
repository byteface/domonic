cmd
=================

The ``cmd`` package calls Windows-style commands from Python.

On Windows it delegates to the native command names. On other platforms,
common commands such as ``dir``, ``copy``, ``move``, ``erase``, ``type_``, and
``comp`` are translated to their Unix equivalents so examples and tests remain
portable.

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
	Cmdcommand.run_args(["echo", "hi"])


Take a look at the code in `cmd.py` to see the available command wrappers.


.. automodule:: domonic.cmd
    :members:
    :noindex:
