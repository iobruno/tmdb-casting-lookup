import io

from google.cloud import storage
from google.cloud.storage import Bucket
from PIL.JpegImagePlugin import JpegImageFile

from tmdb.utils.config import Configuration


class GCSApi:

    def __init__(self):
        cfg = Configuration.load_config()
        client = storage.Client()
        self.bucket: Bucket = client.get_bucket(cfg.gcloud.storage.bucket_name)

    def image_upload(self, picture: JpegImageFile, blob_name: str):
        pic_buffer = io.BytesIO()
        picture.save(pic_buffer, format='JPEG', quality=100)
        blob = self.bucket.blob(blob_name)
        blob.upload_from_string(pic_buffer.getvalue(), content_type="image/jpeg")
        return "gs://{bucket_name}/{blob_name}".format(bucket_name=self.bucket.name,
                                                       blob_name=blob_name)
