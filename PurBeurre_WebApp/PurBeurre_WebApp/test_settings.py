from .settings import *

DEBUG = False
TEMPLATE_DEBUG = False
PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]