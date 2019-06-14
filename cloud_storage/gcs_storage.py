"""
:author: Henley Kuang
:since: 06/12/2019
"""
import traceback

import google.api_core.exceptions
import google.cloud.storage

from cloud_storage.excepts import (
    CloudStorageBadRequestException,
    CloudStorageInvalidArgumentTypeException,
    CloudStorageServerErrorException,
    CloudStorageUnknownErrorException,
)


def gcs_api_exception_handler(f):
    def decorate(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except google.api_core.exceptions.BadRequest:
            raise CloudStorageBadRequestException(traceback.format_exc())
        except (google.api_core.exceptions.InternalServerError,
                google.api_core.exceptions.ServerError,
                google.api_core.exceptions.ServiceUnavailable):
            raise CloudStorageServerErrorException(traceback.format_exc())
        except AssertionError:
            raise CloudStorageInvalidArgumentTypeException(
                traceback.format_exc())
        except Exception:
            raise CloudStorageUnknownErrorException(traceback.format_exc())
    return decorate


class GoogleCloudStorage():

    def __init__(self):
        self.storage_client = google.cloud.storage.Client()
        self._buckets = {}

    def __get_bucket(self, bucket_name):
        try:
            return self._buckets[bucket_name]
        except KeyError:
            self._buckets[bucket_name] = self.storage_client.get_bucket(
                bucket_name)
            return self._buckets[bucket_name]

    def list_buckets(self):
        """ Get the list of buckets in GCS
        Returns:
            list. List of strings of bucket names

        Example.

        >>> GoogleCloudStorage().list_buckets()
        ["bucket1", "bucket2"]
        """
        return list(self.storage_client.list_buckets())

    @gcs_api_exception_handler
    def upload_file(self, bucket_name, source_file_name, object_key,
                    content_type=None, content_encoding=None):
        """Upload a file to a bucket

        Args:
            bucket_name (str):  Bucket name to use
            source_file_name (str): Local file path
            object_key (str): Object key stored in bucket

        Kwargs:
            content_type (str): Type of Content
            content_encoding(str): Encoding used on content for uploading

        """
        bucket = self.__get_bucket(bucket_name)
        blob = bucket.blob(object_key)
        if content_encoding is not None:
            blob.content_encoding = content_encoding

        blob.upload_from_filename(source_file_name, content_type=content_type)

    @gcs_api_exception_handler
    def upload(self, bucket_name, buffer, object_key,
               content_type=None, content_encoding=None):
        """Upload content to a bucket

        Args:
            bucket_name (str):  Bucket name to use
            buffer (bytes): Content to upload
            object_key (str): Object key stored in bucket

        Kwargs:
            content_type (str): Type of Content
            content_encoding(str): Encoding used on content for uploading

        """
        assert isinstance(buffer, bytes)
        bucket = self.__get_bucket(bucket_name)
        blob = bucket.blob(object_key)

        if content_encoding is not None:
            blob.content_encoding = content_encoding

        blob.upload_from_string(buffer, content_type=content_type)

    @gcs_api_exception_handler
    def is_exists(self, bucket_name, object_key):
        """Check if an object exists in bucket

        Args:
            bucket_name (str):  Bucket name to use
            object_key (str): Object key stored in bucket

        Returns:
            boolean. Values::
                True -- Exists in GCS
                False -- Does not exist in GCS

        Example.

        >>> GoogleCloudStorage().is_exists("my_bucket", "my_object_key")
        True
        """
        bucket = self.__get_bucket(bucket_name)
        blob = bucket.blob(object_key)
        return blob.exists()

    @gcs_api_exception_handler
    def rename(self, bucket_name, object_key, new_object_key):
        """Renames an object

        Args:
            bucket_name (str):  Bucket name to use
            object_key (str): Object Key to rename
            new_object_key (str): Object Key to be renamed to
        """
        bucket = self.__get_bucket(bucket_name)
        blob = bucket.blob(object_key)
        bucket.rename_blob(blob, new_object_key)

    @gcs_api_exception_handler
    def download_to_file(self, bucket_name, object_key, destination_file_name):
        """Download an object to local

        Args:
            bucket_name (str):  Bucket name to use
            object_key (str): Object Key to rename
            destination_file_name (str): Local file path
        """
        bucket = self.__get_bucket(bucket_name)
        blob = bucket.blob(object_key)
        blob.download_to_filename(destination_file_name)

    @gcs_api_exception_handler
    def download(self, bucket_name, object_key):
        """Download an object to memory

        Args:
            bucket_name (str):  Bucket name to use
            object_key (str): Object Key to rename

        Returns:
            bytes. Content stored in the object

        Example.

        >>> GoogleCloudStorage().download("my_bucket", "my_object_key")
        b'This is content in your object key'
        """
        bucket = self.__get_bucket(bucket_name)
        blob = bucket.blob(object_key)
        return blob.download_as_string()

    @gcs_api_exception_handler
    def delete(self, bucket_name, object_key):
        """Delete an object from bucket

        Args:
            bucket_name (str):  Bucket name to use
            object_key (str): Object Key to rename
        """
        bucket = self.__get_bucket(bucket_name)
        blob = bucket.blob(object_key)
        blob.delete()
