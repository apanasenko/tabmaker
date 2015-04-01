# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# Settings to postgresql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'debates_tournament',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'host',
        'PORT': 'port',
    }
}
