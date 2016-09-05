from flask import Flask
import ConfigParser
import os

app = Flask(__name__, static_url_path = '/static')

from flog import controllers, models

config = ConfigParser.ConfigParser()
config.read(os.path.join(app.root_path, '../flog.conf'))
database = os.path.join(app.root_path, config.get('PATH', 'DATABASE'))
secret_key = config.get('AUTH', 'SECRET_KEY')
username = config.get('AUTH', 'USERNAME')
password = config.get('AUTH', 'PASSWORD')
debug = config.get('ETC', 'DEBUG')
upload_folder = config.get('PATH', 'UPLOAD_FOLDER')

app.config.update(DATABASE = database,
                  SECRET_KEY = secret_key,
                  USERNAME = username,
                  PASSWORD = password,
                  DEBUG = debug,
                  UPLOAD_FOLDER = upload_folder,
                  ALLOWED_EXTENSIONS = set(['mp3','jpg','jpeg','gif','png'])
                  )