from storages.backends.gcloud import GoogleCloudStorage
from urllib.parse import urljoin
from django.conf import settings


class GoogleCloudMediaFileStorage(GoogleCloudStorage):
    """Custom Google Cloud Storage backend that respects GS_LOCATION."""

    def _save(self, name, content):
        # Ensure the path starts with GS_LOCATION
        if not name.startswith(settings.GS_LOCATION):
            name = f"{settings.GS_LOCATION}/{name.lstrip('/')}"  # Add GS_LOCATION
        print(f"Uploading file to: {name}")  # Debugging
        name = super()._save(name, content)

        # Make the file public
        blob = self.bucket.blob(name)
        blob.make_public()
        print(f"File public URL: {blob.public_url}")
        return name

    def url(self, name):
        # Ensure URLs include MEDIA_URL as root
        return urljoin(settings.MEDIA_URL, name.lstrip('/'))
