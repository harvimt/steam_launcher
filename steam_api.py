#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Copyright (c) 2012, Mark Harviston
All rights reserved.
Redistribution allowed, see LICENSE.txt for details

API for Steam information stored in windows registry and config.vdf

"""
import os

#CONSTANTS
extensions = ( 'png','jpg', 'tga',) #more toward front will be prefered
header_url_s = 'http://cdn.steampowered.com/v/gfx/apps/{appid}/header.jpg'
override_location = r'userdata\{userid}\config\grid\{appid}.{ext}'
localconfig_s = r'userdata\{userid}\config\localconfig.vdf'
launch_url_s = 'steam://rungameid/{appid}'
store_url_s = 'http://store.steampowered.com/app/{appid}/'
steam_key = r'Software\Valve\Steam'
appids_key = steam_key + '\\Apps'
userids_key = steam_key + '\\Users'

steam_path_name = "SteamPath"
user_name_name = 'LastGameNameUsed'
installed_name = 'Installed'

import os.path
import itertools
import sys
import vdf, binvdf

from _winreg import HKEY_CURRENT_USER,  KEY_READ, KEY_ENUMERATE_SUB_KEYS
from _winreg import QueryValue, OpenKey, EnumValue, QueryValueEx, EnumKey

READ_AND_ENUM = KEY_READ | KEY_ENUMERATE_SUB_KEYS

def enum_keys(key):
	#enumerate through sub-keys of key
	#yields the sub-key name
	try:
		for i in itertools.count():
			name = EnumKey(key, i)
			yield name
	except WindowsError as e:
		if e.winerror != 259:
			#errno 259 is "No More Data Available"
			raise


EMPTY = object()
def memoize(fn):
	
	def r(self):
		if r.cache is EMPTY:
			r.cache = fn(self)
		return r.cache
	r.cache = EMPTY
	return r
	
def memoize_gen(fn):
	def gen_cache(gen, cache):
		cache = []
		for i in gen:
			yield i
			cache.append(i)
			
	def r(self):
		if r.cache is EMPTY:
			return gen_cache(fn(self), r.cache)
		else:
			return r.cache
	r.cache = EMPTY
	return r

		
class Steam(object):
	def __init__(self):
		with OpenKey(HKEY_CURRENT_USER, steam_key) as key:
			steam_path, type = QueryValueEx(key, steam_path_name)
			#steam path stored with / as seperator, change to use \ and normalize (should already be normalized, but just to make sure
			steam_path = os.path.normpath(steam_path.replace('/','\\'))
			
			user_name, type = QueryValueEx(key, user_name_name)
	
		self.steam_path = steam_path #
		self.user_name = user_name #last known display user name
		assert(os.path.isdir(steam_path))
		self.config = vdf.VDF(os.path.join(steam_path, 'config\\config.vdf'))
		self.appinfo = None
		
	
	@property
	#@memoize_gen
	def appids(self):
		"generator, yield a 2-tuple of appid as int, installed bool pairs"
		with OpenKey(HKEY_CURRENT_USER, appids_key, 0, READ_AND_ENUM) as key:
			for name in enum_keys(key):
				with OpenKey(key, name) as subkey:
					try:
						installed, type = QueryValueEx(subkey, installed_name)
					except WindowsError as e:
						if e.winerror != 2:
							raise #error 2 is "Not Found"
						continue
						installed = 0
				yield int(name), bool(installed)
	
	@property
	#@memoize_gen
	def apps(self):
		for appid, installed in self.appids:
			app = App(self, appid, installed)
			yield app

	@property
	#@memoize_gen
	def userids(self):
		"yield integer user ids"
		with OpenKey(HKEY_CURRENT_USER, userids_key, 0, READ_AND_ENUM) as key:
			for name in enum_keys(key):		
				yield int(name)
	
	@property
	#@memoize_gen
	def users(self):
		for userid in self.userids:
			yield User(self, userid)
	
	def header_url(self, appid, userid):
		#returns url for header image
		for ext in extensions:
			header_file = os.path.join(self.steam_path, override_location.format(**locals()))
			if os.path.exists(header_file):
				return 'file://' + pathname2url(header_url)
		
		return header_url_s.format(**locals())
	
	def launch_url(self, appid):
		return launch_url_s.format(**locals())
		
	def appinfo(self, appid):
		pass
	
	def store_url(self, appid):
		return store_url_s.format(**locals())

class User(object):
	"""
	Convenience Object for Users
	No interesting data about users are stored in windows registry
	lots of stuff in localconfig
	"""
	def __init__(self, steam, userid):
		self.userid = userid
		self.steam = steam
		self._localconfig = vdf.VDF(os.path.join(steam.steam_path, localconfig_s.format(**locals())))
		
		#loading all of the appcache is too slow only load what is installed
		self.appinfo = binvdf.BinVDF(os.path.join(steam.steam_path, 'appcache\\appinfo.vdf'), searching_for=set(self.appids))
	
	@property
	#@memoize
	def localconfig(self):
		return self._localconfig.d['UserLocalConfigStore']
	
	@property
	@memoize_gen
	def appids(self):
		return itertools.imap(int, self.localconfig['apptickets'].keys())
			
	@property
	#@memoize_gen
	def apps(self):
		for appid in self.appids:
			yield App(self.steam, appid, user=self)

class App(object):
	"""
	Convenience Opbject
	app.foo becomes either
		app.foo
		-or-
		steam.config.d['InstallConfigStore']['Software']['Valve']['Steam']['apps'][self.appid][foo]
		-or-
		steam.appinfo.games_by_id[self.appid][foo]
		-or-
		steam.foo(appid)
		
	(whichever comes first)
	"""
	def __init__(self, steam, appid, installed=None, user=None):
		self.steam = steam
		self.appid = appid
		self._installed = installed
		self.user = user
	
	@property
	def installed(self):
		if self._installed is None:
			key_name = appids_key + '\\' + str(self.appid)
			#print key_name
			
			try:
				with OpenKey(HKEY_CURRENT_USER, key_name) as key:
					self._installed, type = QueryValueEx(key, installed_name)
			except WindowsError as e:
				if e.winerror != 2: raise
				self._installed = True
		#return True
		return self._installed
	
	@property
	#@memoize
	def header_url(self):
		return self.steam.header_url(self.appid, self.user.userid)
		
	@property
	def appinfo(self):
		return self.user.games_by_id[self.appid]
		
	@property
	def exists(self):
		
		return self.installed and \
			self.installdir is not None and os.path.exists(self.installdir) and \
			self.HasAllLocalContent #and \
			
	
	@property
	def visible(self):
		"returns False if not a game or demo"
		
		if self.type.lower() not in ('game', 'demo'):
			return False
		elif self.parentAppID is not None: # and self.parentAppId in self.user.appids:
			return False
		else:
			return True
			
	def __getattr__(self, name):
		appid_s = str(self.appid)
		apps_d = self.steam.config.d['InstallConfigStore']['Software']['Valve']['Steam']['apps']
		if appid_s in apps_d and name in apps_d[appid_s]:
			return apps_d[appid_s][name]
		elif self.user is not None and self.appid in self.user.appinfo.games_by_id and \
			name in self.user.appinfo.games_by_id[self.appid]:
			return self.user.appinfo.games_by_id[self.appid][name]
		elif hasattr(self.steam, name):
			method = getattr(self.steam, name)
			if method is None:
				#print name
				return None
			return method(self.appid)
		else:
			return None