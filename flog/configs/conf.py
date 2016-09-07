import ConfigParser
import os

path = os.path.realpath(os.path.dirname(__file__))
config = ConfigParser.ConfigParser()
config.read(os.path.join(path,'flog.conf'))

database = config.get('PATH', 'DATABASE')
secret_key = config.get('AUTH', 'SECRET_KEY')
username = config.get('AUTH', 'USERNAME')
password = config.get('AUTH', 'PASSWORD')
debug = config.get('ETC', 'DEBUG')
upload_folder = config.get('PATH', 'UPLOAD_FOLDER')

allowed_extensions = set(['mp3','jpg','jpeg','gif','png'])