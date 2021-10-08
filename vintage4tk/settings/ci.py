from .base import *  # noqa

SECRET_KEY = "django-inscureef^w#(kdjz#q+-1kblrhsft93vl&mc=)3$*@2t$#!vi1(&e7jr"
DEBUG = True
THUMBNAIL_DEBUG = True
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "gh",
        "USER": "gh",
        "PASSWORD": "gh",
        "HOST": "localhost",
    }
}
