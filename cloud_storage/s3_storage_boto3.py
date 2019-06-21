"""
:author: Gatsby Lee
:since: 06/21/2019
"""
import gzip

import boto3


class S3CloudStorageBoto3(object):

    def __init__(self):
        self.storage_client = boto3.client('s3')

    def list_bucket_name(self):
        """Return list of bucket names

        Returns:
            bucket_names (list)
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
        self.storage_client.put_object(
            Bucket=bucket_name, Key=object_key, Body=buffer,
            ContentType=content_type, ContentEncoding=content_encoding
        )

    def is_exists(self, bucket_name, object_key):
        """
        :return: True or False, whether the object exists in GCS
        """
        raise NotImplementedError

    def rename(self, bucket_name, object_key, new_object_key):
        """Renames a blob."""
        raise NotImplementedError

    def download_to_file(self, bucket_name, object_key, destination_file_name):
        """Download an object to local

         Args:
             bucket_name (str):  Bucket name to use
             object_key (str): Object Key to rename
             destination_file_name (str): Local file path
         """
        self.storage_client.download_file(
            Bucket=bucket_name, Key=object_key, Filename=destination_file_name)

    def download_gzipped(self, bucket_name, object_key, decode_gzip=False):
        """Download an gzipped object content to memory

        Args:
            bucket_name (str):  Bucket name to use
            object_key (str): Object Key to rename
            decode_gzip (bool): True to decode_gzip (default: False)

        Returns:
            bytes. Content stored in the object
        """
        response = self.storage_client.get_object(
            Bucket=bucket_name, Key=object_key)
        if response['ContentEncoding'] != 'gzip':
            raise ValueError('Object is not gzipped.')

        # Once response['Body'] is stream.
        # Therefore, once it is read, next reading will return empty.
        object_content = response['Body'].read()
        if decode_gzip:
            # @ref: https://gist.github.com/veselosky/9427faa38cee75cd8e27
            object_content = gzip.decompress(object_content)

        return object_content

    def delete(self, bucket_name, object_key):
        """Delete an object from bucket

        Args:
            bucket_name (str):  Bucket name to use
            object_key (str): Object Key to rename
        """
        self.storage_client.delete_object(
            Bucket=bucket_name,
            Key=object_key,
        )
