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
import Widgets
from toastConfigurator import toastConfigurator

### --- The Configuration GUI.
class toastMachineConfAppearanceUI:
	def __init__( self):
		
		self.config = toastConfigurator()
		
		self.gladefile = misc.getPath('ui', 'toast-machine-conf-appearance.glade')
		self.wTree = gtk.glade.XML(self.gladefile,"window1")
		dic = 	{
		#	"on_entryDesc_changed": self.entryDesc_change,
		#	"on_btn_save_clicked": self.btn_save,
			"on_btn_close_clicked": self.btn_cancel,
		#	"on_btn_add_clicked" : self.btn_add,
		#	"on_btn_del_clicked" : self.btn_del,
		#	"on_btn_appereance_clicked" : self.btn_appereance,
		#	"on_treeISO_cursor_changed": self.treeISO_select,
			"on_window1_delete_event": self.delete_event,
		#	"on_toastConfig_destroy": self.quit,
			}
		self.wTree.signal_autoconnect( dic )
		
		self.window = self.wTree.get_widget("window1")
		self.window.set_icon_from_file(misc.getPath('icons', 'toast-machine.png'))
		
		self.vbox = self.wTree.get_widget("vbox2")
		self.selector = Widgets.SingleEdgeSelector("")
		
		self.vbox.add(self.selector)
		self.vbox.reorder_child(self.selector,1)
		self.vbox.show_all()

	def btn_cancel(self, widget):
		print "TODO: Close"
	
	def delete_event(self, widget, event):
		print "TODO: Aggiungere conferma di uscita"
		return False
	
	def run(self):
		gtk.main()
	
	def quit(self, widget):
		sys.exit(0)

if __name__ == "__main__":
	app = toastMachineConfAppearanceUI()
	app.run()

