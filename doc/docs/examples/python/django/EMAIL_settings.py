# E-mail configs
EMAIL_BACKEND: str = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST: str = 'smtp.gmail.com'
EMAIL_PORT: int = 587
EMAIL_USE_TLS: bool = True
EMAIL_HOST_USER: str = str(environ.get('EMAIL_HOST_USER'))
EMAIL_HOST_PASSWORD: str = str(environ.get('EMAIL_HOST_PASSWORD'))
