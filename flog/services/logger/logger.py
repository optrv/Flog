import logging
from functools import wraps
from flog.configs.conf import log_name, log_file, log_format, log_level

log_format = log_format.replace('?','%')
# logging.basicConfig(filename = log_file, level = log_level, format = log_format)

def logger():
    logger = logging.getLogger(log_name)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(file_handler)
    return logger

def log_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception, exc:
            log = logger()
            log.exception(exc)
    return wrapper