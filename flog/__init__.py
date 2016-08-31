from flask import Flask

app = Flask(__name__, static_url_path='/static')
# app.config.from_object('flog.conf')

from flog import models, controllers