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

import os
import sys
import PAM
import gksu2

__base_path__ = os.path.dirname(os.path.abspath(__file__))

APP_NAME = 'toast-machine'
APP_TITLE = 'Toast Machine'
APP_VERSION = '0.1'

PATHS = {
		'locale': [
			'%s/../po' % __base_path__,
			'%s/share/locale' % sys.prefix],
		'ui': [
			'%s/../data/ui' % __base_path__],
		'icons': [
			'%s/../data/icons' % __base_path__],
		'data': [
			'%s/../data' % __base_path__],
		'doc': [
			'%s/../doc' % __base_path__,
			'%s/share/doc/%s' % (sys.prefix, APP_NAME)]
}

def getPath(key, append = ''):
	### Returns the correct path for the specified key
	for path in PATHS[key]:
		if os.path.isdir(path):
			if append:
				return os.path.abspath(os.path.join(path, append))
			else:
				return os.path.abspath(path)

def get_app_logo():
	### Returns the path of the icon logo
	return getPath('icons', '%s.png' % APP_NAME)


def humanSizeFile(file):
	### Returns the human-readable size of a file
	num = os.path.getsize(file)
	for x in ['bytes','KB','MB','GB','TB']:
		if num < 1024.0:
			return "%3.1f%s" % (num, x)
		num /= 1024.0
	return 0

def humanSize(num):
	### Returns the human-readable size of a size (long)
	for x in ['bytes','KB','MB','GB','TB']:
		if num < 1024.0:
			return "%3.1f%s" % (num, x)
		num /= 1024.0
	return 0



### --- This Class helps to check the current user's password due to
###	    the need to ask the current user his password to shutdown the application
class passwordChecker:
	def __init__(self):
		self.service = 'passwd'
		self.user = os.popen("whoami").readlines()[0][:-1]

	def pam_conv(self, auth, query_list, userData):
		resp = []
		for i in range(len(query_list)):
			query, type = query_list[i]
			if type == PAM.PAM_PROMPT_ECHO_ON:			
				resp.append((self.user, 0))
			elif type == PAM.PAM_PROMPT_ECHO_OFF:
				resp.append((gksu2.ask_password(), 0))
			elif type == PAM.PAM_PROMPT_ERROR_MSG or type == PAM.PAM_PROMPT_TEXT_INFO:
				print query
				resp.append(('', 0))
			else:
				return None
		return resp

	def check(self):
		auth = PAM.pam()
		auth.start(self.service)
		auth.set_item(PAM.PAM_USER, self.user)
		auth.set_item(PAM.PAM_CONV, self.pam_conv)
		try:
			auth.authenticate()
			auth.acct_mgmt()
		except PAM.error, resp:
			return 'error'
		except:
			return 'panic'
		else:
			return 'ok'
