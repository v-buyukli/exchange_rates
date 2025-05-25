from decouple import config

from .settings import *

SECRET_KEY = config("SECRET_KEY")


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "test_db.sqlite3",
    }
}

RATE_API_KEY = config("RATE_API_KEY")
