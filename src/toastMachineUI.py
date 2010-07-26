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

import gtk
import gtk.glade
import pygtk
import gobject
pygtk.require('2.0')

import handlepaths

class toastMachineUI(object):
	def __init__(self):
		print 'starting %s' % handlepaths.APP_NAME
		
		gladeUI = handlepaths.getPath('ui', 'toast-machine.glade')
		self.wTree = gtk.glade.XML(gladeUI,"window1")
		
		self.window = self.wTree.get_widget("window1")
		return

app = toastMachineUI()
app.run()
		
	
