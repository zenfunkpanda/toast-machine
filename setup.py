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

from distutils.core import setup
from distutils.command.install_data import install_data
from distutils.dep_util import newer
from distutils.log import info
from glob import glob
import os
import sys

class InstallData(install_data):
  def run (self):
    self.data_files.extend (self._compile_po_files ())
    install_data.run (self)

  def _compile_po_files (self):
    data_files = []

    # Don't install language files on win32
    if sys.platform == 'win32':
      return data_files

    PO_DIR = 'po'
    tmp = []
    for poz in os.listdir(PO_DIR):
    	if poz.endswith(".po"):
    		tmp.append(poz.strip(".po"))
    
    for lang in tmp: #open(os.path.join(PO_DIR, 'availables'), 'r').readlines():
      lang = lang.strip()
      if lang:
        po = os.path.join(PO_DIR, '%s.po' % lang)
        mo = os.path.join('build', 'mo', lang, 'toast-machine.mo')

        directory = os.path.dirname(mo)
        if not os.path.exists(directory):
          info('creating %s' % directory)
          os.makedirs(directory)

        if newer(po, mo):
          # True if mo doesn't exist
          cmd = 'msgfmt -o %s %s' % (mo, po)
          info('compiling %s -> %s' % (po, mo))
          if os.system(cmd) != 0:
            raise SystemExit('Error while running msgfmt')

        dest = os.path.dirname(os.path.join('share', 'locale', lang, 'LC_MESSAGES', 'toast-machine.mo'))
        data_files.append((dest, [mo]))

    return data_files


setup(
  name='Toast Machine',
  version='0.1',
  description='Self Service Distributor of Free Software',
  author='Giampaolo Bozzali',
  author_email='giampaolo.bozzali@gmail.com',
  url='http://toastmachine.trinhackria.org',
  license='GPL v2',
  scripts=['toast-machine'],
  data_files=[
    ('share/xsessions', ['data/xsessions/toast-machine.desktop']),
    ('share/applications', ['data/toast-machine_conf.desktop']),
    ('share/toast-machine/data/icons', glob('data/icons/*')),
    ('share/toast-machine/data/ui', glob('data/ui/*.glade')),
    ('share/doc/toast-machine', ['doc/README', 'doc/CHANGELOG', 'doc/THANKS']),
    ('share/toast-machine/src', glob('src/*.py'))
  ],
  cmdclass={'install_data': InstallData}
)
