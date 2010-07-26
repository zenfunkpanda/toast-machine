#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of the Toast Machine utility.
#
# Copyright(c) 2010 Giampaolo Bozzali <giampaolo.bozzali@gmail.com>
#
# This file may be licensed under the terms of of the
# GNU General Public License Version 2 (the ``GPL'').
#
# Software distributed under the License is distributed
# on an ``AS IS'' basis, WITHOUT WARRANTY OF ANY KIND, either
# express or implied. See the GPL for the specific language
# governing rights and limitations.
#
# You should have received a copy of the GPL along with this
# program. If not, go to http://www.gnu.org/licenses/gpl.html
# or write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

import os, sys

import gtk
import gtk.glade
import pygtk
import gobject
pygtk.require('2.0')

import misc
from toastConfigurator import toastConfigurator

class toastMachineUI(object):
	def __init__(self):
		print 'starting %s' % misc.APP_NAME
		
		self.config = toastConfigurator()
		
		gladeUI = misc.getPath('ui', 'toast-machine.glade')
		self.wTree = gtk.glade.XML(gladeUI,"window1")
		dic = 	{
			"on_btn_exit_clicked": self.btn_exit,
			"on_window1_delete_event": self.delete_event,
			#"on_window1_destroy": self.quit,
			#"on_btn_burn_clicked": self.burn,
			#"on_btn_copy_clicked": self.makeCopy,
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
		
		return
	
	### Signal handlers
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
		
	
