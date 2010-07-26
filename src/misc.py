import os
import sys

__base_path__ = os.path.dirname(os.path.abspath(__file__))

APP_NAME = 'toast-machine'
APP_TITLE = 'Toast Machine'
APP_VERSION = '0.2'

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
  "Returns the correct path for the specified key"
  for path in PATHS[key]:
    if os.path.isdir(path):
      if append:
        return os.path.abspath(os.path.join(path, append))
      else:
        return os.path.abspath(path)

def get_app_logo():
  "Returns the path of the icon logo"
  return getPath('icons', '%s.png' % APP_NAME)


### --- This Class helps to check the current user's password due to
###    the need to ask the current user his password to shutdown the application
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
