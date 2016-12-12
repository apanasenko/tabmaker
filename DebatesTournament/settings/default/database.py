# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# Settings to postgresql
DATABASES = {
    'default': {
        'ENGINE': '<django.db.backends.postgresql>',  # 'django.db.backends.postgresql_psycopg2',
        'NAME': '<database_name>',
        'USER': '<user>',
        'PASSWORD': '<password>',
        'HOST': '<host>',
        'PORT': '<port>',
    }
}

# Settings to SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '<database_name>',
    }
}
