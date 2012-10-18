#!/usr/bin/env python2
#-*- coding=utf-8 -*-
"""
Copyright (c) 2012, Mark Harviston
All rights reserved.
Redistribution allowed, see LICENSE.txt for details
Binary VDF (Valve Data Format) Parser

Probably only applies to appcache/appinfo.vdf

Format seems to be of the form:

new record: {STX}{NUL}appid{NULL}
key/value pair: {SOH}key{NUL}value{NUL}

"""

from pprint import pprint
import chardet
from fix_bad_unicode import text_badness, fix_bad_unicode
import codecs
import tkMessageBox

NUL = '\x00' # NULL character (\0)
SOH = '\x01' # Start of Heading (Smiley)
STX = '\x02' # Start of Text
ETX = '\x03' # End of Text
EOT = '\x04' # End of Transmission
ENQ = '\x05' # Enquiry
ACK = '\x06' # Acknowledge
BEL = '\x07' # Ring the Bell
SMI = '\x09' # Smiley



def fix_ze_unicode(txt):
	"doing my best to fix ze unicode"
	
	if txt == b'':
		return u''
	
	try:
		txt = txt.decode('utf-8')
	except UnicodeDecodeError:
		enc = chardet.detect(txt)['encoding']
		txt = txt.decode(enc)
	
	txt = fix_bad_unicode(txt)
	return txt
	
class Universe(object):
	def __contains__(self, other):
		return True

new_game1 = object()
new_game2 = object()
key_state = object()
val_state = object()
def_state = object()

class BinVDF(object):
	def __init__(self, file, searching_for = None):
		if searching_for is None:
			self.searching_for = Universe()
		else:
			self.searching_for = searching_for
			
		with open(file, 'rb', buffering=10 * (2**10) ) as f:
			self.open(f)
	
	def open(self, file):
		state = def_state
		game_id = val = key = ''
		games = []
		game = {}
		kv = []
		self.games_by_id = {}
	
		while True:
			c = file.read(1)
			if not c: break
		
			if c == STX:
				state = new_game1
				continue
			elif c == SOH:
				state = key_state
				key = val = ''
				continue
				
			if state is new_game1:
				if c == NUL:
					state = new_game2
					game_id = ''
			elif state is new_game2:
				if c == NUL:
					state = None
					try:
						game_id = int(game_id)
					except:
						game_id = ''
				else:
					game_id += c
					
			elif state is val_state:
				if c == NUL:
					
					#if 'Eberron' in val:
						#tkMessageBox.showinfo('title', fix_ze_unicode(val))
						#print '%r' % 
						
					if game_id != '' and game_id in self.searching_for:
						key = fix_ze_unicode(key)
						val = fix_ze_unicode(val)
						if game_id not in self.games_by_id:
							self.games_by_id[game_id] = {}
					
						if key not in self.games_by_id[game_id]:
							self.games_by_id[game_id][key] = val
					
					key = val = ''
					
					state = def_state
				else:
					val += c

			elif state is key_state:
				if c == NUL:
					state = val_state
				else:
					key += c
					
		with open('output.txt', 'w') as f:
			pprint(self.games_by_id, stream=f,indent=4)
#binvdf = BinVDF(r'C:\Program Files (x86)\Steam\appcache\appinfo.vdf')