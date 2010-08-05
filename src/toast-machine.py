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

import os, sys
import locale
import gettext
import gtk.glade
import misc

from toastMachineUI import toastMachineUI
from toastMachineConfUI import toastMachineConfUI
from toastConfigurator import toastConfigurator

if __name__ == '__main__':
	for module in (gettext, gtk.glade):
		module.bindtextdomain(misc.APP_NAME, misc.getPath('locale'))
		module.textdomain(misc.APP_NAME)

	if '--configure' in sys.argv or '-c' in sys.argv:
		app = toastMachineConfUI()
		app.run()
	elif '--purge-config' in sys.argv or '-p' in sys.argv:
		print ("Purging configuration file..."),
		app = toastConfigurator()
		print "...",
		app.purgeDesc()
		print ("...Done!")
	elif '--help' in sys.argv or '-h' in sys.argv:
		print "\nUsage:", sys.argv[0], "[-c | --configure] [-h | --help] [-v | --version] [-p | --purge-config]\n"
	elif '--version' in sys.argv or '-v' in sys.argv:
		print "\nToastMachine %s - Burnin' Distros" % misc.APP_VERSION
		print "Copyright (c) 2010 Giampaolo Bozzali <giampaolo.bozzali@gmail.com>\n"
	elif len(sys.argv) == 1:
		#TODO: handle other window managers
		os.system("metacity&")
		app = toastMachineUI()
		app.run()
	else:
		print _("Unrecognized argument")
		sys.exit(255)
