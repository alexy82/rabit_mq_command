# coding=utf-8
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)
load_dotenv(os.path.join(BASE_DIR, '.env'), override=True, verbose=True)

DEBUG = (os.environ.get('DEBUG', 'False') == 'True')

SYSTEM_NAME = os.environ.get('SYSTEM_NAME', 'MQ')
ENVIRONMENT_NAME = os.environ.get('ENVIRONMENT_NAME', 'MQ')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s | %(levelname)s | %(process)d | %(thread)d | %(filename)s:%('
                      'lineno)d | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '%(levelname)s | %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },

    },
    'loggers': {
        'main': {
            'level': 'INFO',
            'handlers': os.environ.get('LOGGER_MAIN_HANDLERS', 'timed_rotating').split(','),
            'propagate': True,
        },
    },
}

TIME_ZONE = 'Asia/Ho_Chi_Minh'
AMQP = {
    'default': {
        'CLS': 'core.MQ.connection.BlockingConnection',
        'AMQP_URL': os.environ.get('DEFAULT_AMQP_URL',
                                   '*******'
                                   '******'),
        'HOST': os.environ.get('DEFAULT_AMQP_HOST', '******'),
        'PORT': int(os.environ.get('DEFAULT_AMQP_PORT', '*******')),
        'VHOST': os.environ.get('DEFAULT_AMQP_VHOST', '******'),
        'USER': os.environ.get('DEFAULT_AMQP_USER', '******'),
        'PASSWORD': os.environ.get('DEFAULT_AMQP_PASSWORD', '*****'),
        'OPTIONS': {}
    }
}

