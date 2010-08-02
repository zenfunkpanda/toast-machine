#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
#   Project: toast-machine - Self-Service Burning Station  
#    Author: Giampaolo Bozzali <giampaolo.bozzali@gmail.com>
# Copyright: 2010 Giampaolo Bozzali
#   License: GPL-2+
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation; either version 2 of the License, or (at your option)
#  any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
# On Debian GNU/Linux systems, the full text of the GNU General Public License
# can be found in the file /usr/share/common-licenses/GPL-2.
##

import os
import time

class toastDiskMonitor:
	def __init__ (self):
		self.lastList = os.popen("udisks --enumerate").readlines()
		self.lastDevice = None
		self.availableDevice = None
		self.availableMountPoint = None
	
	def isMounted(self):
		tmp = os.popen("udisks --show-info %s" % self.availableDevice).readlines()
		mounted = False
		for line in tmp:
			if line.startswith("  is mounted:") and line.endswith("1\n"):
				mounted = True
			if mounted:
				if line.startswith("  mount paths:"):
					self.availableMountPoint = line.split(":")[1][:-1].lstrip()
					return True
		return False
	
	def isWritable(self):
		tmp = os.popen("udisks --show-info %s" % self.availableDevice).readlines()
		for line in tmp:
			if line.startswith("  is read only:") and line.endswith("0\n"):
				return False
		return True
				
	def mount (self):
		if not self.isMounted() and self.availableDevice != None:
			os.system("udisks --mount %s" % self.availableDevice)
			self.isMounted()
	
	def unmount (self):
		if self.isMounted():
			os.system("udisks --unmount %s" % self.availableDevice)
			self.isMounted()
	
	def watch (self):
		self.newList = os.popen("udisks --enumerate").readlines()
		#removing = (set(self.lastList) - set(self.newList))
		adding = (set(self.newList) - set(self.lastList))
		
		if adding:
			for device in adding:
				if device[-2:-1].isdigit():
					self.lastDevice = device
		#elif removing:
		#	for device in removing:
		#		if device[-2:-1].isdigit():
		#			print device[:-1]
		
		if self.lastDevice != None:
			tmp = "/dev/%s" % self.lastDevice.split("/")[-1:][0][:-1]
			if os.path.exists(tmp):
				self.availableDevice = tmp
			else:
				self.availableDevice = None
				self.availableMountPoint = None
			
		self.lastList = self.newList
		return True
		
		
if __name__ == "__main__":
	# for testing
	app = toastDiskMonitor()
	app.availableDevice = "/dev/sdc1"
	#if app.isMounted():
	#	print app.availableMountPoint
	app.unmount()
	print app.availableMountPoint
	#while 1:
	#	time.sleep(3)
	#	app.watch()
	#	print app.availableDevice