"""
:author: Gatsby Lee
:since: 06/21/2019
"""
import gzip
import io
import logging

import boto3
import botocore

from http import HTTPStatus

from cloud_storage.excepts import (
    CloudStorageInvalidArgumentTypeException,
    CloudStorageNotFoundException,
    CloudStorageUnknownErrorException,
)

LOGGER = logging.getLogger(__name__)

"""
https://stackoverflow.com/questions/42809096/difference-in-boto3-between-resource-client-and-session
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/clients.html
"""


def s3_boto3_api_exception_handler(f):
    def decorate(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except botocore.exceptions.ClientError as e:
            if e.response['ResponseMetadata']['HTTPStatusCode'] == HTTPStatus.NOT_FOUND:
                raise CloudStorageNotFoundException(str(e)) from None
            # not handled, bring up.
            raise e
        except AssertionError as e:
            raise CloudStorageInvalidArgumentTypeException(str(e)) from e
        except Exception as e:
            raise CloudStorageUnknownErrorException(str(e)) from e
    return decorate


class S3CloudStorageBoto3(object):

    def __init__(self):
        self.storage_client = boto3.client('s3')

    def list_bucket_names(self):
        """Return list of bucket names

        Returns:
            bucket_names(list)
        """
        api_response = self.storage_client.list_buckets()
        bucket_raw_info_list = api_response['Buckets']
        bucket_names = []
        for bucket_raw_info in bucket_raw_info_list:
            bucket_names.append(bucket_raw_info['Name'])
        return bucket_names

    def upload_file(self, bucket_name, object_key, source_file_name,
                    content_type=None, content_encoding=None):
        """
        Uploads a local file to a bucket
        """
        # Allowed values for ExtraArgs
        # ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/s3.html#boto3.s3.transfer.S3Transfer.ALLOWED_UPLOAD_ARGS
        self.storage_client.upload_file(
            Bucket=bucket_name, Key=object_key, Filename=source_file_name,
            ExtraArgs={'ContentType': content_type,
                       'ContentEncoding': content_encoding}
        )

    def upload(self, bucket_name, object_key, buffer,
               content_type='', content_encoding=''):
        """Upload content to a bucket

        Args:
            bucket_name(str):  Bucket name to use
            buffer(bytes): Content to upload
            object_key(str): Object key stored in bucket
        Kwargs:
            content_type(str): Type of Content
            content_encoding(str): Encoding used on content for uploading
        Returns:
            None
        """
        assert isinstance(buffer, bytes)
        self.storage_client.put_object(
            Bucket=bucket_name, Key=object_key, Body=buffer,
            ContentType=content_type, ContentEncoding=content_encoding
        )

    def is_exists(self, bucket_name, object_key):
        """Check if an object exists in bucket

        Args:
            bucket_name (str):  Bucket name to use
            object_key (str): Object key stored in bucket

        Returns:
            True if exists.
        """
        try:
            self.storage_client.head_object(Bucket=bucket_name, Key=object_key)
            return True
        except botocore.exceptions.ClientError as e:
            if e.response['ResponseMetadata']['HTTPStatusCode'] == HTTPStatus.NOT_FOUND:
                return False
            # not handled, bring up.
            raise e

    @s3_boto3_api_exception_handler
    def rename(self, bucket_name, object_key, new_object_key):
        """Renames an object

        Args:
            bucket_name (str):  Bucket name to use
            object_key (str): Object Key to rename
            new_object_key (str): Object Key to be renamed to
        Returns:
            None
        """
        assert(object_key != new_object_key), \
            "object_key can't be same to new_object_key"

        # Since this is not atomic operation, deleting current key might fail.
        self.storage_client.copy_object(
            Bucket=bucket_name, Key=new_object_key,
            CopySource={
                'Bucket': bucket_name, 'Key': object_key},
        )
        self.delete(bucket_name, object_key)

    @s3_boto3_api_exception_handler
    def download_gzipped_to_file(self, bucket_name, object_key, destination_file_name,
                                 do_gunzip=False):
        """Download an object to local

         Args:
             bucket_name(str):  Bucket name to use
             object_key(str): Object Key to rename
             destination_file_name(str): Local file path
        Kwargs:
            do_gunzip(bool): True to gunzip(default: False)
        Returns:
            None
         """
        if do_gunzip:
            object_content = self.download_gzipped(
                bucket_name, object_key, do_gunzip)
            with open(destination_file_name, 'wb') as f:
                f.write(object_content)
        else:
            self.storage_client.download_file(
                Bucket=bucket_name, Key=object_key, Filename=destination_file_name)

    @s3_boto3_api_exception_handler
    def download_gzipped(self, bucket_name, object_key, do_gunzip=False):
        """Download an gzipped object content to memory

        Args:
            bucket_name(str):  Bucket name to use
            object_key(str): Object Key to rename
        Kwargs:
            do_gunzip(bool): True to gunzip(default: False)
        Returns:
            bytes. Content stored in the object
        """
        if do_gunzip:
            with io.BytesIO() as bytes_buffer:
                with gzip.GzipFile(fileobj=bytes_buffer, mode='rb') as rgzip_buffer:
                    self.storage_client.download_fileobj(
                        Bucket=bucket_name, Key=object_key, Fileobj=bytes_buffer)
                    bytes_buffer.seek(0)
                    return rgzip_buffer.read()

        with io.BytesIO() as bytes_buffer:
            self.storage_client.download_fileobj(
                Bucket=bucket_name, Key=object_key, Fileobj=bytes_buffer)
            return bytes_buffer.getvalue()

    @s3_boto3_api_exception_handler
    def delete(self, bucket_name, object_key):
        """Delete an object from bucket

        Args:
            bucket_name(str):  Bucket name to use
            object_key(str): Object Key to rename
        Returns:
            None
        @note: No exception raises although object doesn't exist.
        """
        self.storage_client.delete_object(
            Bucket=bucket_name,
            Key=object_key,
        )
