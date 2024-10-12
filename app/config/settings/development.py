from .base import *
from .base import env

import sys

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-vf4y@0%vcdf(1$g(min55fkm_%q=q068_1hzf(zun)ku)rfhav"   # env("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True   # env("DJANGO_DEBUG")

ALLOWED_HOSTS = []  # env.list("DJANGO_ALLOWED_HOSTS")
