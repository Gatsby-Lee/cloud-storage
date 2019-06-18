"""
:author: Henley Kuang
:since: 06/12/2019
"""
import boto3


class S3CloudStorage():

    def __init__(self):
        self.storage_client = boto3.client('s3')
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

    def isexists(self, bucket_name, object_key):
        """
        :return: True or False, whether the object exists in GCS
        """
        bucket = self.get_bucket(bucket_name)
        blob = bucket.blob(object_key)
        return blob.exists()

    def rename(self, bucket_name, object_key, new_object_key):
        """Renames a blob."""
        bucket = self.get_bucket(bucket_name)
        blob = bucket.blob(object_key)
        bucket.rename_blob(blob, new_object_key)

    def download_to_file(self, bucket_name, object_key, destination_file_name):
        bucket = self.get_bucket(bucket_name)
        blob = bucket.blob(object_key)
        blob.download_to_filename(destination_file_name)

    def download(self, bucket_name, object_key):
        bucket = self.get_bucket(bucket_name)
        blob = bucket.blob(object_key)
        return blob.download_as_string()

    def delete(self, bucket_name, object_key):
        self.storage_client.delete_object(
            Bucket=bucket_name,
            Key=object_key,
        )
