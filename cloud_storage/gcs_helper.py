"""
:author: Henley Kuang
:since: 06/12/2019
"""
import google.cloud.storage


class GoogleCloudStorageHelper():

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

    def upload_blob_from_file(self, bucket_name, source_file_name, destination_blob_name,
                              content_type=None, content_encoding=None, storage_class=None):
        """
        Uploads a local file to a bucket
        """
        bucket = self.get_bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        if content_encoding is not None:
            blob.content_encoding = content_encoding
        if storage_class is not None:
            storage_class = storage_class

        blob.upload_from_filename(source_file_name, content_type=content_type)

    def upload_blob_from_string(self, bucket_name, buffer, destination_blob_name,
                                content_type=None, content_encoding=None, storage_class=None):
        """
        Uploads a string to a bucket
        """
        bucket = self.get_bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        if content_encoding is not None:
            blob.content_encoding = content_encoding
        if storage_class is not None:
            storage_class = storage_class

        blob.upload_from_string(buffer, content_type=content_type)

    def get_blob_exists(self, bucket_name, source_blob_name):
        """
        :return: True or False, whether the object exists in GCS
        """
        bucket = self.get_bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        return blob.exists()

    def rename_blob(self, bucket_name, blob_name, new_blob_name):
        """Renames a blob."""
        bucket = self.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        bucket.rename_blob(blob, new_blob_name)

    def download_blob_to_file(self, bucket_name, source_blob_name, destination_file_name):
        bucket = self.get_bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)

    def download_blob_as_string(self, bucket_name, source_blob_name):
        bucket = self.get_bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        return blob.download_as_string()

    def delete_blob(self, bucket_name, blob_name):
        bucket = self.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.delete()
