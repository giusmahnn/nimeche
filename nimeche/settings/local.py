from dotenv import load_dotenv
from .base import *
import os
load_dotenv()

DEBUG = True
ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

ENABLE_MATRIC_NUMBER_VALIDATION = False
