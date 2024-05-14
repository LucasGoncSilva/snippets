from os import environ as env


DATABASES: dict[str, dict[str, str | None]] = {
    # 'default': URL
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.get('DATABASE_NAME'),
        'USER': env.get('DATABASE_USER'),
        'PASSWORD': env.get('DATABASE_PASSWORD'),
        'HOST': env.get('DATABASE_HOST'),
        'PORT': '5432',
    }
}

DEBUG: bool = False
SECRET_KEY: str | None = env.get('SECRET_KEY')
ALLOWED_HOSTS: list[str] = str(env.get('ALLOWED_HOSTS')).split()


# http -> https redirect
SECURE_PROXY_SSL_HEADER: tuple[str, str] = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT: bool = True
