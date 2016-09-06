from flask import Flask
from configs.conf import database, secret_key, username, password, debug, upload_folder, allowed_extensions
import os

app = Flask(__name__, static_url_path = '/static')

from flog import controllers, models
#os.path.join(app.root_path, database)
app.config.update(DATABASE = database,
                  SECRET_KEY = secret_key,
                  USERNAME = username,
                  PASSWORD = password,
                  DEBUG = debug,
                  UPLOAD_FOLDER = upload_folder,
                  ALLOWED_EXTENSIONS = allowed_extensions
                  )

app.add_url_rule('/', view_func = controllers.show_posts, methods=['GET'])
app.add_url_rule('/login', view_func = controllers.login, methods=['GET', 'POST'])
app.add_url_rule('/logout', view_func = controllers.logout, methods=['GET'])
app.add_url_rule('/add_post', view_func = controllers.add_post, methods=['POST'])