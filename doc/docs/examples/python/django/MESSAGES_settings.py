from django.contrib.messages import constants as messages


# Messages configs
MESSAGE_TAGS: dict[int, str] = {
    messages.DEBUG: 'alert-primary',
    messages.ERROR: 'alert-danger',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
}
