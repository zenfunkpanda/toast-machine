import os
import sys

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
