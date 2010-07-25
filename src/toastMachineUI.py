import os
from gettext import gettext as _

import gtk
import gtk.glade
import pygtk
import gobject
pygtk.require('2.0')

import handlepaths

class toastMachineUI(object):
  def __init__(self):
    print 'starting %s' % handlepaths.APP_NAME
	
app = toastMachineUI()