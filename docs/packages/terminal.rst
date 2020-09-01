Domonic: terminal
=================

There is a command line package that can call bash/unix/posix and other apps on the command line.

This package only works on nix systems as it effectively just passes stuff off to subprocess.

.. code-block :: python

	from domonic.terminal import *

	print(ls())
	print(ls("-al"))
	print(ls("../"))

	print(pwd())

	print(mkdir('somedir'))
	print(touch('somefile'))
	print(git('status'))

	for file in ls( "-al" ):
	    print("Line : ", file)

	for f in ls():
	    try:
	        print(f)
	        print(cat(f))
	    except Exception as e:
	        pass

	for i, l in enumerate(cat('LICENSE.txt')):
	    print(i,l)

	print(man("ls"))
	print(echo('test'))
	print(df())
	print(du())

	for thing in du():
	    print(thing)

	print(find('.'))
	# print(ping('eventual.technology'))# < TODO - need to strean output
	print(cowsay('moo'))
	print(wget('eventual.technology'))
	print(date())
	print(cal())


run arbitrary commands...
--------------------------------

.. code-block :: python

	from domonic.terminal import command
	command.run("echo hi")


Take a look at the code in 'terminal.py' to see all the commands as there's loads. (Disclaimer: not all tested.)
