STATIC_URL: str = '/static/'
STATIC_ROOT: str = BASE_DIR / 'staticfiles'
STATICFILES_DIRS: list[str] = [
    BASE_DIR / 'static',
]
STATICFILES_STORAGE: list[str] = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
