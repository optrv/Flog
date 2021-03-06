import ConfigParser
import os

path = os.path.realpath(os.path.dirname(__file__))
config = ConfigParser.ConfigParser()
config.read(os.path.join(path,'flog.conf'))

database = config.get('PATH', 'DATABASE')
upload_folder = config.get('PATH', 'UPLOAD_FOLDER')
secret_key = config.get('AUTH', 'SECRET_KEY')
username = config.get('AUTH', 'USERNAME')
password = config.get('AUTH', 'PASSWORD')
image_width = config.get('SERVICE', 'IMAGE_WIDTH')
watermark_path = config.get('SERVICE', 'WATERMARK_PATH')
mp3_bitrate = config.get('SERVICE', 'MP3_BITRATE')
log_name = config.get('LOG', 'NAME')
log_file = config.get('LOG', 'FILE')
log_level = config.get('LOG', 'LEVEL')
log_format = config.get('LOG', 'FORMAT')
debug = config.get('ETC', 'DEBUG')
posts_per_page = config.get('ETC', 'POSTS_PER_PAGE')

allowed_extensions = ['mp3','jpg','jpeg','gif','png']