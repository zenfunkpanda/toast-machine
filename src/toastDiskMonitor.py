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
			
		self.lastList = self.newList
		return True
		
		
if __name__ == "__main__":
	app = toastDiskMonitor()
	while 1:
		time.sleep(3)
		app.watch()
		print app.availableDevice