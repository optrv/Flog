import ConfigParser
import os

path = os.path.realpath(os.path.dirname(__file__))
config = ConfigParser.ConfigParser()
config.read(os.path.join(path,'flog.conf'))

DATABASE = config.get('PATH', 'database')
DB_DUMP = config.get('PATH', 'db_dump')
UPLOAD_FOLDER = config.get('PATH', 'upload_folder')
SECRET_KEY = config.get('AUTH', 'secret_key')
USERNAME = config.get('AUTH', 'username')
PASSWORD = config.get('AUTH', 'password')
IMAGE_WIDTH = config.get('SERVICE', 'image_width')
WATERMARK_PATH = config.get('SERVICE', 'watermark_path')
MP3_BITRATE = config.get('SERVICE', 'mp3_bitrate')
LOG_NAME = config.get('LOG', 'name')
LOG_FILE = config.get('LOG', 'file')
LOG_LEVEL = config.get('LOG', 'level')
LOG_FORMAT = config.get('LOG', 'format')
DEBUG = config.get('ETC', 'debug')
POSTS_PER_PAGE = config.get('ETC', 'posts_per_page')
FORCE_SQLITE = config.getboolean('ETC', 'force_sqlite')

ALLOWED_EXTENSIONS = ['mp3','jpg','jpeg','gif','png']