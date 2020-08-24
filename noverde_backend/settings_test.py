from noverde_backend.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
}

CELERY_BROKER_URL = ''
CELERY_RESULT_BACKEND = ''
CELERY_TASK_ALWAYS_EAGER = True
