from .base import *  # noqa
from .base import config

# django-storages
# ------------------------------------------------------------------------------
INSTALLED_APPS += ["storages"]  # noqa: F405

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

# Moving static assets to DigitalOcean Spaces as per:
# https://www.digitalocean.com/community/tutorials/how-to-set-up-object-storage-with-django
AWS_ACCESS_KEY_ID = config("STATIC_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("STATIC_SECRET_KEY")

AWS_STORAGE_BUCKET_NAME = config("STATIC_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = config("STATIC_ENDPOINT_URL")
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
AWS_LOCATION = "static"
AWS_DEFAULT_ACL = "public-read"

STORAGES = {
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
}

STATIC_URL = f"https://{AWS_S3_ENDPOINT_URL}/{AWS_LOCATION}/"
