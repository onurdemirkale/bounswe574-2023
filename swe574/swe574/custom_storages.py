from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

# Extends the S3Boto3Storage class to create a directory for 
# static files in the S3 Bucket
class StaticFileStorage(S3Boto3Storage):
  location = settings.STATICFILES_FOLDER

# Extends the S3Boto3Storage class to create a directory for 
# media files in the S3 Bucket
class MediaFileStorage(S3Boto3Storage):
  location = settings.MEDIAFILES_FOLDER