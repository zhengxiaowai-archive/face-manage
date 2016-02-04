import os     
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')

if not os.path.exists(LOGS_DIR):
    os.mkdir(LOGS_DIR)

LOGGING = {
    'version': 1,
    'dusable_existing_loggers': True,
    'formatters': {
        'normal': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s %(filename)s[line:%(lineno)d]'
        },   
        'simple': {
            'format': '%(levelname)s %(module)s %(message)s'
        }
    },
    'handlers': {
        'django': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'D',
            'interval': 1,
            'backupCount': 5,
            'filename': os.path.join(LOGS_DIR, 'django.log'),
            'formatter': 'normal'           
        },
        'app': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'D',
            'interval': 1,
            'backupCount': 5,
            'filename': os.path.join(LOGS_DIR, 'app.log'),
            'formatter': 'normal'           
        }
    },
    'loggers': {
        'django': {
            'handlers': ['django'],         
            'propagate': False,
            'level': 'DEBUG'
        },
        '': {
            'handlers': ['app'],            
            'level': 'DEBUG'
        }
    }
}
