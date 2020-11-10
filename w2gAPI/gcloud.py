"""
  GoogleCloudStorage extension classes for MEDIA and STATIC uploads
  """
from django.conf import settings
from storages.backends.gcloud import GoogleCloudStorage
from storages.utils import setting
from urllib.parse import urljoin
import environ


env = environ.Env()
environ.Env.read_env(env_file='db.env')
SECRET_KEY = env("SECRET_KEY")


class GoogleCloudStaticFileStorage(GoogleCloudStorage):
    """
    Google file storage class which gives a media file path from STATIC_URL not google generated one.
    """
    bucket_name = env('GS_BUCKET_NAME')

    def url(self, name):
        """
        Gives correct STATIC_URL and not google generated url.
        """
        return urljoin(settings.STATIC_URL, name)