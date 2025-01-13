from dotenv import load_dotenv
from .base import *
import os
load_dotenv()

DEBUG = False
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

ENABLE_MATRIC_NUMBER_VALIDATION = True
SESSION_COOKIE_AGE = 3600
SESSION_EXPIRE_AT_BROWSER_CLOSE = True 
SESSION_COOKIE_SECURE = True