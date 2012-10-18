#!/usr/bin/env python2
#-*- coding=utf-8 -*-
"""
Copyright (c) 2012, Mark Harviston
All rights reserved.
Redistribution allowed, see LICENSE.txt for details
Uses steam_api.py to generate an HTML file with links to run games
"""
from __future__ import unicode_literals
import os
import codecs
from pprint import pformat
from steam_api import Steam
steam = Steam()

#normally I frown on playing golf with Python, but this is pretty beautiful isn't it?
#No? well the function name clearly describes what it does.
strornonetobool = lambda s: False if s is None else bool(int(s))
	
def gen_output():
	
	with codecs.open('output.html', 'w', encoding='utf-8') as f:
		f.write('<!DOCTYPE html>\n<html lang="en-us">')
		f.write('<meta charset="utf-8"/>\n')
		f.write('<head><title>Test</title></head>')
		f.write('<body>')
		for user in steam.users:
			f.write('<p>Persona: {user.localconfig[friends][PersonaName]}</p>\n'.format(**locals()))
			
			for app in sorted(user.apps, key=lambda x: x.name):
				
				if app.exists and app.visible:
					#header_url = steam.header_url(app.appid, userid)
					bname = os.path.basename(app.installdir)
					f.write('<h2>{app.name}</h2>'.format(**locals()))
					f.write('appid={app.appid} dir={bname}<br/>'.format(**locals()))
					f.write('<a href="{app.launch_url}"><img src="{app.header_url}"/></a><br/>\n'.format(**locals()))
					f.write('<pre>%s</pre><br/>' % pformat(user.appinfo.games_by_id[app.appid],indent=4))
					
		f.write('</body></html>')

gen_output()