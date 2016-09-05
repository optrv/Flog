from flask import Flask
import ConfigParser
import os

app = Flask(__name__, static_url_path = '/static')

from flog import controllers, models

config = ConfigParser.ConfigParser()
config.read(os.path.join(app.root_path, '../flog.conf'))
app.config.update(DATABASE = os.path.join(app.root_path, config.get('PATH', 'DATABASE')),
                  SECRET_KEY = config.get('AUTH', 'SECRET_KEY'),
                  USERNAME = config.get('AUTH', 'USERNAME'),
                  PASSWORD = config.get('AUTH', 'PASSWORD'),
                  DEBUG = config.get('ETC', 'DEBUG'),
                  UPLOAD_FOLDER = config.get('PATH', 'UPLOAD_FOLDER'),
                  ALLOWED_EXTENSIONS = set(['mp3','jpg','jpeg','gif','png']),
                  )
