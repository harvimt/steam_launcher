#!/usr/bin/env python2
#-*- coding=utf-8 -*-
"""
(C) 2012 Mark Harviston All Rights Reserved

Valve Data Format (VDF) plain text version parser

"GROUP_NAME"
{
	"KEY" "VALUE and stuff"
	"KEY"
	"VALUE"
	"NESTED GROUP" {
		"KEY" "VALUE"
	}
}

key/values  will be stored in a nested dictionary on VDF.d
example: v.d['GROUP_NAME']['NESTED GROUP']['KEY']
and in a seperator delimited dict. VDF.sep_d
example: v.sep_d['GROUP_NAME.NESTED GROUP.KEY']
"""

SEP = '.'

import re, shlex
GROUP_BEGIN = re.compile(r'^\s*\{\s*$')
GROUP_END = re.compile(r'^\s*\}\s*$')

import sys

class VDF(object):
	def __init__(self, file):
		if isinstance(file, (str, unicode)):
			with open(file,'r') as f:
				self.open(f)
		else:
			self.open(f)
		
	def open(self, file):
	
		self.d = {}
		self.d_stack = [self.d]
		self.name_stack = []
		
		self.sep_d = {}
		
		found_single = False #found only a single value on the line
		prev = None
		
		for line_no, line in enumerate(file):
			if found_single:
				found_single = False
				
				if GROUP_BEGIN.match(line) is not None:
					self.name_stack.append(prev)
					tmp_d = {}
					self.d[prev] = tmp_d
					self.d_stack.append(self.d)
					self.d = tmp_d
					
				else:
					line_s = shlex.split(line)
					assert(len(line_s) == 1)
					self.proc_pair(prev, line_s[0])
				prev = None
			else:
				if GROUP_END.match(line) is not None:
					self.name_stack.pop()
					self.d = self.d_stack.pop()
			
				else:
					line_s = shlex.split(line)
					
					if len(line_s) == 1:
						found_single = True
						prev = line_s[0]						
					else:
						name, value = line_s
						self.proc_pair(name, value)

		
	def proc_pair(self, name, value):
		"process a pair of values into the dict"
		self.d[name] = value
		sep_name = SEP.join(self.name_stack) + SEP + name
		self.sep_d[sep_name] = value