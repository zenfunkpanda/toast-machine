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

import sys

import gtk
import gtk.glade
import pygtk
import gobject
pygtk.require('2.0')

import subprocess

import misc
from toastConfigurator import toastConfigurator
from toastDiskMonitor import toastDiskMonitor

class toastMachineUI(object):
	def __init__(self):
		print 'starting %s' % misc.APP_NAME
		
		self.config = toastConfigurator()
		
		gladeUI = misc.getPath('ui', 'toast-machine.glade')
		self.wTree = gtk.glade.XML(gladeUI,"window1")
		dic = 	{
			"on_btn_exit_clicked": self.btn_exit,
			"on_window1_delete_event": self.delete_event,
			"on_window1_destroy": self.quit,
			"on_btn_burn_clicked": self.btn_burn,
			"on_btn_cp_clicked": self.btn_cp,
			"on_btn_dd_clicked": self.btn_dd,
			#"on_treeview1_cursor_changed": self.selectionChanged,
			"on_btn_about_clicked": self.showAbout,
		}
		self.wTree.signal_autoconnect( dic )
		
		self.window = self.wTree.get_widget("window1")
		
		self.treeview = self.wTree.get_widget("treeview1")
		self.treeview.set_model(self.config.getListForTreeViewTM())
		self.tc = gtk.TreeViewColumn(("Available ISOs"))
		self.treeview.append_column(self.tc)
		self.cr = gtk.CellRendererText()
		self.tc.pack_start(self.cr, True)
		self.tc.add_attribute(self.cr, "markup", 0)
		self.tc.set_expand(True)
		self.td = gtk.TreeViewColumn(("Media"))
		self.treeview.append_column(self.td)
		self.cr = gtk.CellRendererPixbuf()
		self.td.pack_start(self.cr, True)
		self.td.add_attribute(self.cr, 'stock_id', 3)
		self.td.set_expand(False)

		self.status = self.wTree.get_widget("label1")
		self.progressbar = self.wTree.get_widget("progressbar1")
		
		self.toastMonitor = toastDiskMonitor()
		gobject.timeout_add (1000,self.toastMonitor.watch)
		gobject.timeout_add (700,self.idleCheck)
		
		self.ddprocess = 0
				
		return
	
	def idleCheck(self):
		if self.ddprocess != 0:
			print self.ddprocess.pid
		return True
	
	def showAbout(self, widget, data=None):
		aboutDialog = gtk.AboutDialog()
		aboutDialog.set_name("Toast Machine")
		aboutDialog.set_version(misc.APP_VERSION)
		aboutDialog.set_copyright("Copyright © 2010 Giampaolo Bozzali\n" + ("Original Idea by Cremona Linux User Group"))
		aboutDialog.set_comments("«Burnin' Distros»")
		aboutDialog.set_logo(gtk.gdk.pixbuf_new_from_file(misc.get_app_logo()))
		aboutDialog.set_authors(["Giampaolo Bozzali <giampaolo.bozzali@gmail.com>"])
		aboutDialog.set_website("http://toastmachine.trinhackria.org")
		aboutDialog.set_license("GNU GPL - General Public License version 2")
		#aboutDialog.set_translator_credits("http://launchpad.net")
		aboutDialog.run()
		aboutDialog.destroy()

	def btn_burn (self, widget):
		print "TODO: BURN"
	
	def btn_cp (self, widget):
		print "TODO: COPY"
		file = None
		fileType = None
		model, row = self.treeview.get_selection().get_selected()
		if row != None:
			file = model.get_value(row,1)
			fileType = model.get_value(row,2)
			#if fileType == "zip" or fileType == "dmg":
			#	print "cp %s %s/" % (file, self.detectedLastPath)
			#	self.burnprocess = subprocess.Popen(["cp", "-fu", file, self.detectedLastPath])
			#	self.window.set_sensitive(False)
		if file != None:
			print "--> copio %s (%s)" % (file, fileType)	
	
	def btn_dd (self, widget):
		print "ci sto lavorando"
		self.ddprocess = subprocess.Popen(["dd","if=/dev/zero","of=/dev/null"])
	
	def btn_exit (self, widget):
		self.quit()
		
	def delete_event(self, widget, event):
		#if self.validation.check() == "ok":
		#	return False
		print "FIXME: delete_event"
		return True
	
	def run(self):
		gtk.main()
		
	def quit(self):
		sys.exit(0)

if __name__ == "__main__":
	app = toastMachineUI()
	app.run()