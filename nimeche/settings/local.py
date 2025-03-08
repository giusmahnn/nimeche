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

ENABLE_MATRIC_NUMBER_VALIDATION = True

# IPWARE_META_PRECEDENCE_ORDER
IPWARE_META_PRECEDENCE_ORDER = (
    'HTTP_X_FORWARDED_FOR',  # First check this header
    'REMOTE_ADDR',           # Then check this header
)