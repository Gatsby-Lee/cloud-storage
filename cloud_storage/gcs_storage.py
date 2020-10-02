"""
:author: Henley Kuang
:since: 06/12/2019
"""
import logging
import os

import google.api_core.exceptions
import google.cloud.storage

from google import resumable_media

from cloud_storage.excepts import (
    CloudStorageBadRequestException,
    CloudStorageInvalidArgumentTypeException,
    CloudStorageNotFoundException,
    CloudStorageServerErrorException,
    CloudStorageUnknownErrorException,
)


"""
@ref:
https://2.python-requests.org//en/master/user/quickstart/#binary-response-content
https://github.com/googleapis/google-resumable-media-python/blob/master/google/resumable_media/requests/__init__.py
https://github.com/googleapis/google-resumable-media-python/blob/master/google/resumable_media/requests/download.py#L120
https://github.com/googleapis/google-resumable-media-python/blob/master/google/resumable_media/requests/download.py#L139
https://github.com/googleapis/google-cloud-python/blob/master/storage/google/cloud/storage/blob.py
"""

LOGGER = logging.getLogger(__name__)


def gcs_api_exception_handler(f):
    def decorate(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except google.api_core.exceptions.BadRequest as e:
            raise CloudStorageBadRequestException(str(e))
        except (
            google.api_core.exceptions.InternalServerError,
            google.api_core.exceptions.ServerError,
            google.api_core.exceptions.ServiceUnavailable,
        ) as e:
            raise CloudStorageServerErrorException(str(e))
        except google.api_core.exceptions.NotFound as e:
            raise CloudStorageNotFoundException(str(e))
        except AssertionError as e:
            raise CloudStorageInvalidArgumentTypeException(str(e)) from e
        except Exception as e:
            raise CloudStorageUnknownErrorException(str(e)) from e

    return decorate


class GoogleCloudStorage(object):
    def __init__(self):
        self.storage_client = google.cloud.storage.Client()
        self._buckets = {}

    def _get_bucket(self, bucket_name):
        try:
            return self._buckets[bucket_name]
        except KeyError:
            self._buckets[bucket_name] = self.storage_client.get_bucket(bucket_name)
            return self._buckets[bucket_name]

    def list_bucket_names(self):
        """Get the list of buckets in GCS
        Returns:
            list. List of strings of bucket names

        Example.

        >>> GoogleCloudStorage().list_bucket_names()
        ["bucket1", "bucket2"]
        """
        return list(self.storage_client.list_buckets())

    @gcs_api_exception_handler
    def upload_file(
        self,
        bucket_name,
        object_key,
        source_file_name,
        content_type=None,
        content_encoding=None,
    ):
        """Upload a file to a bucket

        Args:
            bucket_name (str):  Bucket name to use
            source_file_name (str): Local file path
            object_key (str): Object key stored in bucket
        Kwargs:
            content_type (str): Type of Content
            content_encoding(str): Encoding used on content for uploading
        Returns:
            None
        """
        bucket = self._get_bucket(bucket_name)
        blob = bucket.blob(object_key)
        if content_encoding is not None:
            blob.content_encoding = content_encoding

        blob.upload_from_filename(source_file_name, content_type=content_type)

    @gcs_api_exception_handler
    def upload(
        self, bucket_name, object_key, buffer, content_type=None, content_encoding=None
    ):
        """Upload content to a bucket

        Args:
            bucket_name (str):  Bucket name to use
            buffer (bytes): Content to upload
            object_key (str): Object key stored in bucket
        Kwargs:
            content_type (str): Type of Content
            content_encoding(str): Encoding used on content for uploading
        Returns:
            None
        """
        assert isinstance(buffer, bytes)
        bucket = self._get_bucket(bucket_name)
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
        bucket = self._get_bucket(bucket_name)
        blob = bucket.blob(object_key)
        return blob.exists()

    @gcs_api_exception_handler
    def rename(self, bucket_name, object_key, new_object_key):
        """Renames an object

        Args:
            bucket_name (str):  Bucket name to use
            object_key (str): Object Key to rename
            new_object_key (str): Object Key to be renamed to
        Returns:
            None
        """
        assert (
            object_key != new_object_key
        ), "object_key can't be same to new_object_key"

        bucket = self._get_bucket(bucket_name)
        blob = bucket.blob(object_key)
        # Since this is not atomic operation, deleting current key might fail.
        bucket.rename_blob(blob, new_object_key)

    @gcs_api_exception_handler
    def download_gzipped_to_file(
        self, bucket_name, object_key, destination_file_name, do_gunzip=False
    ):
        """Download an object to local

        Args:
            bucket_name (str):  Bucket name to use
            object_key (str): Object Key to rename
            destination_file_name (str): Local file path
        Kwargs:
            do_gunzip(bool): True to gunzip(default: False)
        Returns:
            None
        """
        bucket = self._get_bucket(bucket_name)
        blob = bucket.blob(object_key)

        # blob.download_to_filename(destination_file_name)
        # https://googleapis.github.io/google-cloud-python/latest/_modules/google/cloud/storage/blob.html#Blob.download_to_file
        raw_download = not do_gunzip
        try:
            with open(destination_file_name, "wb") as file_obj:
                blob.download_to_file(file_obj, raw_download=raw_download)
        except resumable_media.DataCorruption:
            # Delete the corrupt downloaded file.
            os.remove(destination_file_name)
            raise

    @gcs_api_exception_handler
    def download_gzipped(self, bucket_name, object_key, do_gunzip=False):
        """Download an object to memory

        Args:
            bucket_name (str):  Bucket name to use
            object_key (str): Object Key to rename
        Kwargs:
            do_gunzip(bool): True to gunzip(default: False)
        Returns:
            bytes. Content stored in the object

        Example.
        >>> GoogleCloudStorage().download_gzipped("my_bucket", "my_object_key")
        b'This is content in your object key'
        """
        bucket = self._get_bucket(bucket_name)
        blob = bucket.blob(object_key)

        # Google uses python-requests.
        # And, The gzip and deflate transfer-encodings are automatically decoded.
        # ref: https://github.com/googleapis/google-resumable-media-python/blob/master/google/resumable_media/requests/download.py#L120
        if do_gunzip:
            return blob.download_as_string()

        return blob.download_as_string(raw_download=True)

    @gcs_api_exception_handler
    def delete(self, bucket_name, object_key):
        """Delete an object from bucket.

        Exception won't be raised although object_key doesn't exist.

        Args:
            bucket_name (str):  Bucket name to use
            object_key (str): Object Key to rename
        Returns:
            None
        """
        bucket = self._get_bucket(bucket_name)
        blob = bucket.blob(object_key)
        try:
            blob.delete()
        except google.api_core.exceptions.NotFound:
            # slience if object_key doesn't exists
            pass
