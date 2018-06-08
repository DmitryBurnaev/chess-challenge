import os
import logging
import logging.config

LOG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'simple_output': {
            'format': '%(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple_output',
            'level': 'INFO',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'simple_output',
            'level': 'INFO',
            'filename': os.path.join(LOG_DIR, 'results.log'),
            'mode': 'w',
        }
    },
    'loggers': {
        'game_logic': {
            'handlers': ['console']
        },
        '__main__': {
            'handlers': ['console']
        }
    }
}


def get_log_file_handler():
    """Shortcut for getting file handler for our project """

    file_config = LOGGING_CONFIG['handlers']['file']
    f_name = file_config['filename']
    f_mode = file_config['mode']
    handler = logging.handlers.RotatingFileHandler(f_name, mode=f_mode)
    handler.setLevel(file_config['level'])
    return handler


def get_logger(name=None):
    """ Getting configured logger
    :param name: current module (if necessary)
    """

    logging.config.dictConfig(LOGGING_CONFIG)
    logger_name = name or 'game_logic'
    print(logger_name)
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    return logger


