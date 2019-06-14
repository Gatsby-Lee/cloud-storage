"""
:author: Henley Kuang
:since: 06/12/2019
"""
import google.cloud.storage
import google.api_core.exceptions
import traceback

from cloud_storage.excepts import (
    UploadBadRequestException,
    UploadServerErrorException,
    UploadUnknownErrorException,
)


def gcs_api_exception_handler(f):
    def decorate(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except google.api_core.exceptions.BadRequest:
            raise UploadBadRequestException(traceback.format_exc())
        except (google.api_core.exceptions.InternalServerError,
                google.api_core.exceptions.ServerError,
                google.api_core.exceptions.ServiceUnavailable):
            raise UploadServerErrorException(traceback.format_exc())
        except Exception:
            raise UploadUnknownErrorException(traceback.format_exc())
    return decorate


class GoogleCloudStorage():

    def __init__(self):
        self.storage_client = google.cloud.storage.Client()
        self._buckets = {}

    def list_buckets(self):
        return self.storage_client.list_buckets()

    def get_bucket(self, bucket_name):
        try:
            return self._buckets[bucket_name]
        except KeyError:
            self._buckets[bucket_name] = self.storage_client.get_bucket(
                bucket_name)
            return self._buckets[bucket_name]

    @gcs_api_exception_handler
    def upload_file(self, bucket_name, source_file_name, object_key,
                    content_type=None, content_encoding=None):
        """
        Uploads a local file to a bucket
        """
        bucket = self.get_bucket(bucket_name)
        blob = bucket.blob(object_key)
        if content_encoding is not None:
            blob.content_encoding = content_encoding

        blob.upload_from_filename(source_file_name, content_type=content_type)

    @gcs_api_exception_handler
    def upload(self, bucket_name, buffer, object_key,
               content_type=None, content_encoding=None):
        """
        Uploads a string to a bucket
        """
        bucket = self.get_bucket(bucket_name)
        blob = bucket.blob(object_key)

        if content_encoding is not None:
            blob.content_encoding = content_encoding

        blob.upload_from_string(buffer, content_type=content_type)

    @gcs_api_exception_handler
    def isexists(self, bucket_name, object_key):
        """
        :return: True or False, whether the object exists in GCS
        """
        bucket = self.get_bucket(bucket_name)
        blob = bucket.blob(object_key)
        return blob.exists()

    @gcs_api_exception_handler
    def rename(self, bucket_name, object_key, new_object_key):
        """Renames a blob."""
        bucket = self.get_bucket(bucket_name)
        blob = bucket.blob(object_key)
        bucket.rename_blob(blob, new_object_key)

    @gcs_api_exception_handler
    def download_to_file(self, bucket_name, object_key, destination_file_name):
        bucket = self.get_bucket(bucket_name)
        blob = bucket.blob(object_key)
        blob.download_to_filename(destination_file_name)

    @gcs_api_exception_handler
    def download(self, bucket_name, object_key):
        bucket = self.get_bucket(bucket_name)
        blob = bucket.blob(object_key)
        return blob.download_as_string()

    @gcs_api_exception_handler
    def delete(self, bucket_name, object_key):
        bucket = self.get_bucket(bucket_name)
        blob = bucket.blob(object_key)
        blob.delete()
