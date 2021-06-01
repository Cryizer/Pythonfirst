import sys
assert sys.version_info.major >= 3, "Python version too old!"

sys.path.insert(0, '/home/kkwsgi/wsgi_public/')
from test import app as application
