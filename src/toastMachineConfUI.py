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
pygtk.require('2.0')

from gettext import gettext as _

import misc
from toastConfigurator import toastConfigurator

### --- The Configuration GUI.
class toastMachineConfUI:
	def __init__( self):
		
		self.config = toastConfigurator()
		
		self.gladefile = misc.getPath('ui', 'toast-machine-conf.glade')
		self.wTree = gtk.glade.XML(self.gladefile,"window1")
		dic = 	{
			"on_entryDesc_changed": self.entryDesc_change,
			"on_btn_save_clicked": self.btn_save,
			"on_btn_cancel_clicked": self.btn_cancel,
			"on_btn_add_clicked" : self.btn_add,
			"on_btn_del_clicked" : self.btn_del,
			"on_btn_appereance_clicked" : self.btn_appereance,
			"on_treeISO_cursor_changed": self.treeISO_select,
			"on_window1_delete_event": self.delete_event,
			"on_toastConfig_destroy": self.quit,
			}
		self.wTree.signal_autoconnect( dic )
		
		self.window = self.wTree.get_widget("window1")
		self.window.set_icon_from_file(misc.getPath('icons', 'toast-machine.png'))

		self.dirtree = self.wTree.get_widget("treeview1")
		self.dirtree.set_model(self.config.getDirListForTreeView())
		self.tc = gtk.TreeViewColumn(_("Search paths"))
		self.dirtree.append_column(self.tc)
		self.cr = gtk.CellRendererText()
		self.tc.pack_start(self.cr, True)
		self.tc.add_attribute(self.cr, "markup", 0)

		self.filetree = self.wTree.get_widget("treeview2")
		self.filetree.set_model(self.config.getListForTreeView())
		self.tc = gtk.TreeViewColumn(_("Available resources"))
		self.filetree.append_column(self.tc)
		self.cr = gtk.CellRendererText()
		self.tc.pack_start(self.cr, True)
		self.tc.add_attribute(self.cr, "markup", 0)
		
		self.entryDesc = self.wTree.get_widget("entryDesc")
		
	def selectDir(self):
		dialog = gtk.FileChooserDialog(_("Select path"),
                               None,
                               gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		dialog.set_default_response(gtk.RESPONSE_OK)
		
		response = dialog.run()
		
		folder = None
		if response == gtk.RESPONSE_OK:
			folder = dialog.get_filename()
		elif response == gtk.RESPONSE_CANCEL:
			folder = None
		dialog.destroy()
		
		return folder
		
	def entryDesc_change(self, widget):
		model, row = self.filetree.get_selection().get_selected()
		if row != None:
			idn = model.get_value(row,1).split("/")[-1]
			#desc = model.get_value(row,0)
		self.config.changeDesc(idn, self.entryDesc.get_text())

	def treeISO_select(self, widget):
		model, row = self.filetree.get_selection().get_selected()
		if row != None:
			idn = model.get_value(row,1)			
			#desc = model.get_value(row,0)
		self.entryDesc.set_text(self.config.getDesc(idn))
	
	def btn_add(self, widget):
		paths = self.config.getPaths()
		tmp = self.selectDir()
		if tmp != None:
			if tmp == "/":
				paths.append(tmp)
			else:
				paths.append(tmp+"/")
				print paths
		self.config.setPaths(paths)
		self.dirtree.set_model(self.config.getDirListForTreeView())
		self.filetree.set_model(self.config.getListForTreeView())		
	
	def btn_del(self, widget):
		model, row = self.dirtree.get_selection().get_selected()
		if row != None:
			path = model.get_value(row,0)
			paths = self.config.getPaths()
			paths.remove(path)
			self.config.setPaths(paths)
			self.dirtree.set_model(self.config.getDirListForTreeView())
			self.filetree.set_model(self.config.getListForTreeView())
	
	def btn_appereance(self, widget):
		print "TODO: show appereance window"			

	def btn_save(self, widget):
		self.config.commit()
		self.quit(self)

	def btn_cancel(self, widget):
		sys.exit(255)
		self.quit(self)
	
	def delete_event(self, widget, event):
		print "TODO: Aggiungere conferma di uscita"
		return True
	
	def run(self):
		gtk.main()
	
	def quit(self, widget):
		sys.exit(0)

if __name__ == "__main__":
	app = toastMachineConfUI()
	app.run()

