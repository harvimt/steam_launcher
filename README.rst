==============
Steam Launcher
==============
A Launcher for Steam Games
--------------------------

Requirements
============

	* Python 2 (tested with 2.7)
	* Python `chardet`_ package
	* Steam

.. _chardet: http://pypi.python.org/pypi/chardet

Running
=======
Run output.py then load output.html in your favorite browser.
Clicking on a game launches it, you may have to confirm that you want links of type steam:// to open in Steam.

How it works 
============
Data is pulled from the windows registry and from vdf (both binary and plain text) files stored in the Steam.
This information is then used to create an HTML web-page containing steam:// links that launch your games.

License
=======
BSD 3-Clause License
fix_bad_unicode (bundled) is MIT Licensed
