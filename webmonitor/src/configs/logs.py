import logging
import logging.config


LOG_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {
            "format": ("[%(asctime)s]\t%(levelname)s\t%(message)s"),
            "datefmt": LOG_DATE_FORMAT,
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "DEBUG",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "default",
            "level": "INFO",
            "filename": "/tmp/webmonitor.log",
        },
    },
    "loggers": {
        "src": {"handlers": ["stdout", "file"], "level": "DEBUG", "propagate": False},
        "": {  # default logger, used for, eg, 3rd-party lib
            "handlers": ["stdout"],
            "level": "WARNING",
            "propagate": True,
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
