import logging
import logging.config
from datetime import datetime
from typing import Optional

INFO_LEVEL = "info"

def time_encoder(record: logging.LogRecord) -> str:
    return datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

def set_handler(level: int) -> None:
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'custom': {
                'format': '{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}',
                'datefmt': None,
                '()': CustomFormatter,
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'custom',
            },
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': level,
            },
        },
    }
    
    logging.config.dictConfig(logging_config)

class CustomFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        record.asctime = time_encoder(record)
        return super().format(record)

def verbosity(level: str) -> None:
    if level == "error":
        set_handler(logging.ERROR)
    elif level == "info":
        set_handler(logging.INFO)
    elif level == "debug":
        set_handler(logging.DEBUG)
    else:
        set_handler(logging.DEBUG)
