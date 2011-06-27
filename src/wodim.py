#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (C) 2011 by Giampaolo Bozzali <giampaolo.bozzali@gmail.com>
#  This file is part of Toast Machine.
#  http://pandafunk.blogspot.com/p/toast-machine_10.html
#
#  Toast Machine is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the
#  Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

import sys, os, fcntl, select
import subprocess

# calcola la percentuale
def spacchio(tmp):
	a = tmp.split()
	if a[0] == "Track" and a[3] == "of":
		print "%.0f" % (100 * float(a[2])/float(a[4]))

class burner:
	def __init__(self):
		self.process = subprocess.Popen(["echo"])
		self.outfile = None
		self.outfd = None
		self.file_flags = None
		
		self.iso_file = None
	
	def burna(self, isofile):
		self.process = subprocess.Popen(["wodim", "-dummy", "-v", isofile], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
		self.outfile = self.process.stdout
		self.outfd = self.outfile.fileno()
		self.file_flags = fcntl.fcntl(self.outfd, fcntl.F_GETFL)
		fcntl.fcntl(self.outfd, fcntl.F_SETFL, self.file_flags | os.O_NOFOLLOW)
	
	def test(self):
		if self.process.poll() == 0:
			print "non sta facendo niente"
		elif self.process.poll() == None:
			ready = select.select([self.outfd],[],[],.1)
			print ready
			if len(ready[0]) == 0:
				print "aspetto!"
			else:
				stringa = ''
				tmp = self.outfile.read(1).replace("\r","\n")
				while tmp != '\n':
					stringa += tmp
					tmp = self.outfile.read(1).replace("\r","\n")
				spacchio(stringa)

spacchio("Track 01:    6 of  188 MB written (fifo 100%) [buf  71%]   1.4x.")
