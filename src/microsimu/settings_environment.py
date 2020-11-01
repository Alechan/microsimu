from .read_env_file import *

DEBUG = int(os.environ.get("DEBUG"))

# 'DJANGO_ALLOWED_HOSTS' should be a single string of hosts with a space between each.
# For example: 'DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]'
ALLOWED_HOSTS = os.environ\
    .get("DJANGO_ALLOWED_HOSTS")\
    .split(" ")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

DATABASES = {
    "default": {
        "ENGINE"   : os.environ.get("SQL_ENGINE"),
        "NAME"     : os.environ.get("SQL_DATABASE"),
        "USER"     : os.environ.get("SQL_USER"),
        "PASSWORD" : os.environ.get("SQL_PASSWORD"),
        "HOST"     : os.environ.get("SQL_HOST"),
        "PORT"     : os.environ.get("SQL_PORT"),
    }
}
