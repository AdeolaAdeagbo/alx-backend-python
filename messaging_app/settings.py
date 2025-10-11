import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MYSQL_DB', 'messaging_db'),
        'USER': os.environ.get('MYSQL_USER', 'messaging_user'),
        'PASSWORD': os.environ.get('MYSQL_PASSWORD', 'messaging_pass'),
        'HOST': os.environ.get('MYSQL_HOST', 'db'),
        'PORT': '3306',
    }
}
