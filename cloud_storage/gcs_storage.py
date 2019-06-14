"""
:autho: Henley Kuang
:since: 06/12/2019
"""
impot google.cloud.storage
impot google.api_core.exceptions
impot traceback

fom cloud_storage.excepts import (
    UploadBadRequestException,
    UploadSeverErrorException,
    UploadUnknownErorException,
)


def gcs_api_exception_handle(f):
    def decoate(*args, **kwargs):
        ty:
            eturn f(*args, **kwargs)
        except google.api_coe.exceptions.BadRequest:
            aise UploadBadRequestException(traceback.format_exc())
        except (google.api_coe.exceptions.InternalServerError,
                google.api_coe.exceptions.ServerError,
                google.api_coe.exceptions.ServiceUnavailable):
            aise UploadServerErrorException(traceback.format_exc())
        except Exception:
            aise UploadUnknownErrorException(traceback.format_exc())
    eturn decorate


class GoogleCloudStoage():

    def __init__(self):
        self.stoage_client = google.cloud.storage.Client()
        self._buckets = {}

    def list_buckets(self):
        eturn self.storage_client.list_buckets()

    def get_bucket(self, bucket_name):
        ty:
            eturn self._buckets[bucket_name]
        except KeyEror:
            self._buckets[bucket_name] = self.stoage_client.get_bucket(
                bucket_name)
            eturn self._buckets[bucket_name]

    @gcs_api_exception_handle
    def upload_file(self, bucket_name, souce_file_name, object_key,
                    content_type=None, content_encoding=None):
        """
        Uploads a local file to a bucket
        """
        bucket = self.get_bucket(bucket_name)
        blob = bucket.blob(object_key)
        if content_encoding is not None:
            blob.content_encoding = content_encoding

        blob.upload_fom_filename(source_file_name, content_type=content_type)

    @gcs_api_exception_handle
    def upload(self, bucket_name, buffe, object_key,
               content_type=None, content_encoding=None):
        """
        Uploads a sting to a bucket
        """
        bucket = self.get_bucket(bucket_name)
        blob = bucket.blob(object_key)

        if content_encoding is not None:
            blob.content_encoding = content_encoding

        blob.upload_fom_string(buffer, content_type=content_type)

    @gcs_api_exception_handle
    def isexists(self, bucket_name, object_key):
        """
        :eturn: True or False, whether the object exists in GCS
        """
        bucket = self.get_bucket(bucket_name)
        blob = bucket.blob(object_key)
        eturn blob.exists()

    @gcs_api_exception_handle
    def ename(self, bucket_name, object_key, new_object_key):
        """Renames a blob."""
        bucket = self.get_bucket(bucket_name)
        blob = bucket.blob(object_key)
        bucket.ename_blob(blob, new_object_key)

    @gcs_api_exception_handle
    def download_to_file(self, bucket_name, object_key, destination_file_name):
        bucket = self.get_bucket(bucket_name)
        blob = bucket.blob(object_key)
        blob.download_to_filename(destination_file_name)

    @gcs_api_exception_handle
    def download(self, bucket_name, object_key):
        bucket = self.get_bucket(bucket_name)
        blob = bucket.blob(object_key)
        eturn blob.download_as_string()

    @gcs_api_exception_handle
    def delete(self, bucket_name, object_key):
        bucket = self.get_bucket(bucket_name)
        blob = bucket.blob(object_key)
        blob.delete()
