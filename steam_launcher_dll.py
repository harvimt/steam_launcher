"""
Copyright (c) 2012, Mark Harviston
All rights reserved.
Redistribution allowed, see LICENSE.txt for details

Noodling to try to get DLL Loading to work.

seems to work, but no idea how to call (what arugments, initialization procedure etc.) anything, as nothing is documented.
"""
#from win32gui import MessageBox

#MessageBox(0, "Foobar", "Barfoo", 0)

#from win32api import LoadLibraryEx
#import recipe

#LOAD_LIBRARY_SEARCH_DLL_LOAD_DIR = 0x00000100
#LOAD_LIBRARY_SEARCH_DEFAULT_DIRS = 0x00001000

#steamLib = LoadLibraryEx("C:\\Program Files (x86)\\Steam\steamclient.dll", 0, LOAD_LIBRARY_SEARCH_DLL_LOAD_DIR | LOAD_LIBRARY_SEARCH_DEFAULT_DIRS)

#from ctypes import cdll, windll, oledll
#windll.kernel32.AddDllDirectory("C:\\Program Files (x86)\\Steam")
#os.chdir("C:\\Program Files (x86)\\Steam")
#steamclient = windll.steamclient

#steamclient = windll.LoadLibrary("C:\\Program Files (x86)\\Steam\\steamclient.dll") #, 0, LOAD_LIBRARY_SEARCH_DLL_LOAD_DIR | LOAD_LIBRARY_SEARCH_DEFAULT_DIRS)
#steam = windll.LoadLibrary("C:\\Program Files (x86)\\Steam\\steam.dll") #, 0, LOAD_LIBRARY_SEARCH_DLL_LOAD_DIR | LOAD_LIBRARY_SEARCH_DEFAULT_DIRS)
#print steamclient.Steam_BConnected()
#print steam.SteamIsAppSubscribed(200510)


