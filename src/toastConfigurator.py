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
import gtk
import ConfigParser
import misc

from gettext import gettext as _

class toastConfigurator:
	def __init__(self):
		self.configFile = os.getenv("HOME") + "/.toastmachine"
		self.defaultPath = os.getenv("HOME") + "/iso"
		self.config = ConfigParser.RawConfigParser()
		
		### Check if the config not exists and create one filling it with defaults
		if not os.path.exists(self.configFile):
			if not self.config.has_section("toastMachine"):
				self.config.add_section('toastMachine')
				self.config.set('toastMachine','path',self.defaultPath)
				self.config.add_section('descriptions')
				
			tmp = open(self.configFile,'w')
			self.config.write(tmp)
			tmp.close()
			
		self.config.read(self.configFile)
		self.createDesc()

	### --- Commit changes to the config file
	###     Dump the entire self.config object into the config file and reread it
	def commit(self):
		tmp = open(self.configFile,'w')
		self.config.write(tmp)
		tmp.close()
		self.config.read(self.configFile)
	
	### --- Get paths from config string and convert into an array
	def getPaths(self):
		tmp = []
		if not self.config.get("toastMachine","path") == "":
			for item in self.config.get("toastMachine","path").split(":"):
				if not item.endswith("/") and len(item) > 1:
					item = item + "/"
					tmp.append(item)
				else:
					tmp.append(item)
		return tmp

	
	### --- Convert an array of paths into a configuration string and commit it
	def setPaths(self, dirArray):
		tmp = ":".join(dirArray)
		self.config.set("toastMachine","path",tmp)
		self.createDesc()
		self.commit()
	
	### --- Search for ISOs and return a list from the self.getPaths()
	def searchISO(self):
		fileTypes = [".ISO", ".ZIP", ".DMG", ".IMG"]		
		tmp = []
		for directory in self.getPaths():
			if os.path.exists(directory):
				for file in os.listdir(directory):
					if file[:1] != "." and file[-4:].upper() in fileTypes:
						tmp.append(directory + file)
		return tmp

	### --- Create description for each ISO found, create but not delete if file is missing
	def createDesc(self):
		for item in self.searchISO():
			item = item.split("/")[-1]
			if not self.config.has_option("descriptions", item):
				self.config.set("descriptions", item, item)
		self.commit()
	
	### --- Purge descriptions for missing ISO in path
	###     I use lower() because the option in ConfigParser is case-insensitive
	def purgeDesc(self):
		tmp = []
		for item in self.searchISO():
			tmp.append(item.split("/")[-1].lower())

		for item in self.config.options("descriptions"):
			if not item in tmp:
				print _("No longer exists: %s" % item)
				self.config.remove_option("descriptions",item)
		self.commit()

	### --- Return a Valid list for gtkTreeView with description (for config UI)
	def getDirListForTreeView(self):
		tmp = gtk.TreeStore(str)
		for item in self.getPaths():
			tmp.append(None, [item])
		return tmp
	
	### --- Return a Valid list for gtkTreeView with description (for config UI)
	def getListForTreeView(self):
		tmp = gtk.TreeStore(str,str)
		for item in self.searchISO():
			tmp.append(None, [item.split("/")[-1], item.split("/")[-1] ])
		return tmp

	### --- Return a Valid list for gtkTreeView with description and icons (for TM UI)
	def getListForTreeViewTM(self):
		tmp = gtk.ListStore(str,str,str,str)
		for item in self.searchISO():
			desc = "<big><u><b>%s</b></u></big>\n<small>%s (%s)</small>" % \
				(self.getDesc(item.split("/")[-1]), item.split("/")[-1], misc.humanSizeFile(item))
			if item.split("/")[-1][-3:].upper() == "DMG":
				type_id = "dmg"				
				stockIcon = gtk.STOCK_FLOPPY
			elif item.split("/")[-1][-3:].upper() == "ZIP":
				type_id = "zip"				
				stockIcon = gtk.STOCK_DND
			elif item.split("/")[-1][-3:].upper() == "IMG":
				type_id = "img"				
				stockIcon = gtk.STOCK_HARDDISK
			else:
				type_id = "iso"
				stockIcon = gtk.STOCK_CDROM
			tmp.append([desc, item, type_id, stockIcon])
		return tmp

	### --- Change the description of a given option
	def changeDesc(self, idn, value):
		self.config.set("descriptions", idn, value)
	### --- Get the description of a given option
	def getDesc(self, idn):
		return self.config.get("descriptions", idn)
