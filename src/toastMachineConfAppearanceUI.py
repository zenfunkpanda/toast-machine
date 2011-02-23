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
			"on_btn_save_clicked": self.btn_save,
			"on_btn_close_clicked": self.btn_cancel,
			"on_btn_wallpaper_clicked" : self.btn_wallpaper,
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
		self.selector.connect ('clicked', self.updateEdgeLabel)
		self.selector._current = [self.config.getPosition()]
		
		self.vbox.add(self.selector)
		self.vbox.reorder_child(self.selector,1)
		self.vbox.show_all()
		
		self.positionLabel = self.wTree.get_widget("label2")
		self.updateEdgeLabel(self, None, None)
		
		a, b = self.config.getSize()
		self.widthSelector = self.wTree.get_widget("spinbutton1")
		self.widthSelector.set_range(640.0, float(gtk.gdk.screen_width()))
		self.widthSelector.set_value(float(a))
		self.heightSelector = self.wTree.get_widget("spinbutton2")
		self.heightSelector.set_range(480.0, float(gtk.gdk.screen_height()))
		self.heightSelector.set_value(float(b))
		
		self.wallpaper = self.config.getWallpaper()
		self.wallPaperName = self.wTree.get_widget("entry1")
		self.wallPaperName.set_text(self.wallpaper.split("/")[-1:][0])

	def updateEdgeLabel(self, widget, position, event):
		position = self.selector._current
		if position == ["Center"]:
			self.positionLabel.set_text(_("Centered"))
		elif position == ["Top"]:
			self.positionLabel.set_text(_("Top"))
		elif position == ["TopRight"]:
			self.positionLabel.set_text(_("Top Right"))
		elif position == ["Right"]:
			self.positionLabel.set_text(_("Right"))
		elif position == ["BottomRight"]:
			self.positionLabel.set_text(_("Bottom Right"))
		elif position == ["Bottom"]:
			self.positionLabel.set_text(_("Bottom"))
		elif position == ["BottomLeft"]:
			self.positionLabel.set_text(_("Bottom Left"))
		elif position == ["Left"]:
			self.positionLabel.set_text(_("Left"))
		elif position == ["TopLeft"]:
			self.positionLabel.set_text(_("Top Left"))

	def selectFile(self):
		dialog = gtk.FileChooserDialog(_("Select Wallpaper"),
                               None,
                               gtk.FILE_CHOOSER_ACTION_OPEN,
                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		dialog.set_default_response(gtk.RESPONSE_OK)
		dialog.set_current_folder(misc.getPath("wallpapers",""))

		filter = gtk.FileFilter()
		filter.set_name("JPG/PNG/GIF")
		filter.add_mime_type("image/jpeg")
		filter.add_mime_type("image/png")
		filter.add_mime_type("image/gif")
		dialog.add_filter(filter)
		
		response = dialog.run()
		
		folder = None
		if response == gtk.RESPONSE_OK:
			folder = dialog.get_filename()
		elif response == gtk.RESPONSE_CANCEL:
			folder = None
		dialog.destroy()
		
		return folder

	def btn_wallpaper(self, widget):
		self.wallpaper = self.selectFile()
		self.wallPaperName.set_text(self.wallpaper.split("/")[-1:][0])
	
	def btn_cancel(self, widget):
		print "TODO: Close"
		if __name__ == "__main__":
			self.quit()
		self.window.hide()
	
	def btn_save(self, widget):
		self.config.setPosition(self.selector._current[0])
		self.config.setSize(self.widthSelector.get_value(), self.heightSelector.get_value())
		self.config.setWallpaper(self.wallpaper)
		self.config.commit()
		print "TODO: Save"
		print self.config.getWallpaper()
	
	def delete_event(self, widget, event):
		print "TODO: Aggiungere conferma di uscita"
		return True
	
	def run(self):
		gtk.main()
	
	def quit(self):
		sys.exit(0)

if __name__ == "__main__":
	app = toastMachineConfAppearanceUI()
	app.run()

