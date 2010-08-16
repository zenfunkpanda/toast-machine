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

import sys, os, fcntl, select

import gtk
import gtk.glade
import pygtk
import gobject
pygtk.require('2.0')

import subprocess
from threading import Thread

from gettext import gettext as _

import misc
from toastConfigurator import toastConfigurator
from toastDiskMonitor import toastDiskMonitor

class toastMachineUI(object):
	def __init__(self):
		print 'DEBUG: starting %s' % misc.APP_NAME
		
		self.config = toastConfigurator()
		self.secure = misc.passwordChecker()
		
		gladeUI = misc.getPath('ui', 'toast-machine.glade')
		self.wTree = gtk.glade.XML(gladeUI,"window1")
		dic = 	{
			"on_btn_exit_clicked": self.btn_exit,
			"on_window1_delete_event": self.delete_event,
			"on_window1_destroy": self.quit,
			"on_btn_burn_clicked": self.btn_burn,
			"on_btn_cp_clicked": self.btn_cp,
			"on_btn_dd_clicked": self.btn_dd,
			"on_treeview1_cursor_changed": self.selectionChanged,
			"on_btn_about_clicked": self.showAbout,
			"on_window1_window_state_event": self.minimize_event
		}
		self.wTree.signal_autoconnect( dic )
		
		self.window = self.wTree.get_widget("window1")
		self.window.set_icon_from_file(misc.getPath('icons', 'toast-machine.png'))
		
		self.ui_btn_burn = self.wTree.get_widget("btn_burn")
		self.ui_btn_burn.set_sensitive(False)
		self.ui_btn_dd = self.wTree.get_widget("btn_dd")
		self.ui_btn_dd.set_sensitive(False)
		self.ui_btn_cp = self.wTree.get_widget("btn_cp")
		self.ui_btn_cp.set_sensitive(False)
		
		self.ui_buttongroup = self.wTree.get_widget("hbuttonbox1")
		
		self.treeview = self.wTree.get_widget("treeview1")
		self.treeview.set_model(self.config.getListForTreeViewTM())
		self.tc = gtk.TreeViewColumn(_("Available resources"))
		self.treeview.append_column(self.tc)
		self.cr = gtk.CellRendererText()
		self.tc.pack_start(self.cr, True)
		self.tc.add_attribute(self.cr, "markup", 0)
		self.tc.set_expand(True)
		self.td = gtk.TreeViewColumn(_("Type"))
		self.treeview.append_column(self.td)
		self.cr = gtk.CellRendererPixbuf()
		self.td.pack_start(self.cr, True)
		self.td.add_attribute(self.cr, 'stock_id', 3)
		self.td.set_expand(False)

		self.status = self.wTree.get_widget("label1")
		self.status.set_text("")
		self.progressbar = self.wTree.get_widget("progressbar1")
		
		self.toastMonitor = toastDiskMonitor()
		gobject.timeout_add (1000,self.toastMonitor.watch)
		gobject.timeout_add (150,self.idleCheck)
		
		self.dd_process = subprocess.Popen(["echo"])
		self.dd_outfile = None
		self.dd_outfd = None
		self.dd_file_flags = None
		self.dd_file = None
		
		self.cp_process = subprocess.Popen(["echo"])
		self.cp_file = None
		
		self.burn_process = subprocess.Popen(["echo"])
		self.burn_file = None
				
		return

	def selectionChanged(self, widget):
		model, row = self.treeview.get_selection().get_selected()
		if row != None:
			file = model.get_value(row,0)
			fileType = model.get_value(row,2)
			if fileType == "iso":
				self.ui_btn_burn.set_sensitive(True)
				self.ui_btn_dd.set_sensitive(False)
				self.ui_btn_cp.set_sensitive(True)
			elif fileType == "img":
				self.ui_btn_burn.set_sensitive(False)
				self.ui_btn_dd.set_sensitive(True)
				self.ui_btn_cp.set_sensitive(True)
			elif fileType == "zip" or fileType == "dmg":
				self.ui_btn_burn.set_sensitive(False)
				self.ui_btn_dd.set_sensitive(False)
				self.ui_btn_cp.set_sensitive(True)
	
	def idleCheck(self):
		if self.dd_process.poll() == 0 and self.cp_process.poll() == 0 and self.burn_process.poll() == 0:
			if self.toastMonitor.availableDevice == None:
				self.status.set_text(_("Insert a removable media"))
				self.progressbar.set_text("")
			else:
				self.status.set_text(_("Current media: %s" % self.toastMonitor.availableDevice))
		
		if self.dd_process.poll() == None:
			ready = select.select([self.dd_outfd],[],[],.1)
			if len(ready[0]) == 0:
				os.system("kill -USR1 %s" % self.dd_process.pid)
			else:
				tmp = self.dd_outfile.readline()[:-1]
				if len(tmp.split()) > 3:
					self.progressbar.pulse()
					self.progressbar.set_text(tmp)
		
		if self.cp_process.poll() == None:
			tmp = self.cp_file.split("/")[-1:][0]
			ttmmpp = 0
			try:
				ttmmpp = "%s/%s" % (self.toastMonitor.availableMountPoint, tmp)
			except:
				ttmmpp = 0
			self.progressbar.pulse()
			txt = _("%s of %s copied" % (misc.humanSizeFile(ttmmpp),misc.humanSizeFile(self.cp_file)))
			self.progressbar.set_text(txt)
		
		return True
	
	def btn_burn (self, widget):
		self.burn_file = None
		model, row = self.treeview.get_selection().get_selected()
		if row != None:
			self.burn_file = model.get_value(row,1)
			print "DEBUG: passo la palla a brasero"
			self.burn_process = subprocess.Popen(["brasero", "-i", self.burn_file ])
			self.window.set_visible(False)
			Thread(target=self.burnWait).start()

	def burnWait (self):
		self.burn_process.wait()
		print "DEBUG: brasero si è chiuso"
		self.window.set_visible(True)
	
	def btn_cp (self, widget):
		self.cp_file = None
		model, row = self.treeview.get_selection().get_selected()
		if row != None:
			self.cp_file = model.get_value(row,1)
			if self.toastMonitor.availableDevice == None:
				print "DEBUG: Nessun supporto rilevato"
				return
			
			if not self.toastMonitor.isMounted():
				self.toastMonitor.mount()
			
			self.ui_buttongroup.set_sensitive(False)
			self.cp_process = subprocess.Popen(["cp", self.cp_file, self.toastMonitor.availableMountPoint + "/"])
			self.status.set_text(_("Copying selected file on removable media"))
			Thread(target=self.cpWait).start()
	
	def cpWait (self):
		self.cp_process.wait()
		self.toastMonitor.unmount()
		self.progressbar.set_fraction(0.0)
		self.progressbar.set_text(_("Finish! You can safely unplug your removable media"))
		print "TODO: ask for a second operation or unmount"
		self.ui_buttongroup.set_sensitive(True)
	
	def btn_dd (self, widget):
		self.dd_file = None
		model, row = self.treeview.get_selection().get_selected()
		if row != None:
			self.dd_file = model.get_value(row,1)
			if self.toastMonitor.availableDevice == None:
				print "DEBUG: Nessun supporto rilevato"
				return
			
			if self.toastMonitor.isMounted():
				self.toastMonitor.unmount()
			
			self.dd_process = subprocess.Popen(
											["dd", "if="+self.dd_file,"of="+self.toastMonitor.availableDevice[:-1]],
											stderr=subprocess.PIPE,
											stdout=subprocess.PIPE )
			self.dd_outfile = self.dd_process.stderr
			self.dd_outfd = self.dd_outfile.fileno()
			self.dd_file_flags = fcntl.fcntl(self.dd_outfd, fcntl.F_GETFL)
			fcntl.fcntl(self.dd_outfd, fcntl.F_SETFL, self.dd_file_flags | os.O_NOFOLLOW)
			
			self.ui_buttongroup.set_sensitive(False)
			self.status.set_text(_("Transferring selected bootable image on removable media"))
			Thread(target=self.ddWait).start()
		return True

	def ddWait(self):
		self.dd_process.wait()
		self.progressbar.set_fraction(0.0)
		self.progressbar.set_text(_("Finish! You can safely unplug your removable media"))
		self.ui_buttongroup.set_sensitive(True)			
	
	def btn_exit (self, widget):
		if self.secure.check() == 'ok':
			self.quit()
		#self.quit()
		
	def delete_event(self, widget, event):
		print "DEBUG: funzione disattivata"
		return True
	
	def minimize_event (self, widget, event):
		print "FIXME: workaround per evitare la minimizzazione della finestra"
		self.window.deiconify()

	def showAbout(self, widget, data=None):
		aboutDialog = gtk.AboutDialog()
		aboutDialog.set_name("Toast Machine")
		aboutDialog.set_version(misc.APP_VERSION)
		aboutDialog.set_copyright("Copyright © 2010 Giampaolo Bozzali\n" + _("Original idea by LUG Cremona"))
		#aboutDialog.set_comments("«Burnin' Distros»")
		aboutDialog.set_logo(gtk.gdk.pixbuf_new_from_file(misc.get_app_logo()))
		aboutDialog.set_authors(["Giampaolo Bozzali <giampaolo.bozzali@gmail.com>"])
		aboutDialog.set_website("http://toastmachine.trinhackria.org")
		aboutDialog.set_license("GNU GPL - General Public License version 2")
		#aboutDialog.set_translator_credits("http://launchpad.net")
		aboutDialog.run()
		aboutDialog.destroy()	

	def run(self):
		gtk.main()
		
	def quit(self):
		sys.exit(0)

if __name__ == "__main__":
	app = toastMachineUI()
	app.run()
