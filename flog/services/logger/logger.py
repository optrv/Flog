import logging
from functools import wraps
from flog.configs.conf import LOG_NAME, LOG_FILE, LOG_FORMAT, LOG_LEVEL

log_format = LOG_FORMAT.replace('?', '%')


def logger():
    """
    The logger object with specified parameters
    """
    logger = logging.getLogger(LOG_NAME)
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(LOG_LEVEL)
    file_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(file_handler)
    return logger


def log_error(func):
    """
    The wrapper of function that need to logging
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            log = logger()
            log.exception(exc)
    return wrapper
