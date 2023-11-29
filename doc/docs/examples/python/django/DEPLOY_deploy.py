DATABASES: dict[str, dict[str, str | None]] = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': environ.get('DATABASE_NAME'),
        'USER': environ.get('DATABASE_USER'),
        'PASSWORD': environ.get('DATABASE_PASSWORD'),
        'HOST': environ.get('DATABASE_HOST'),
        'PORT': '5432',
    }
}

DEBUG = bool(environ.get('DEBUG', 'False'))
SECRET_KEY: str | None = environ.get('SECRET_KEY')
ALLOWED_HOSTS: list[str] = str(environ.get('ALLOWED_HOSTS')).split(',')


# http -> https redirect
SECURE_PROXY_SSL_HEADER: tuple[str, str] = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT: bool = True
