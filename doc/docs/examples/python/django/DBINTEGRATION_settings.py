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
