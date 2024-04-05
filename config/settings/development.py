from .base import *  # noqa
from .base import config

# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ["django_extensions"]  # noqa: F405

# Email
EMAIL_BACKEND = config("DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
