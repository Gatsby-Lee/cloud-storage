from cloud_storage.__about__ import __version__
from cloud_storage.enums import CloudStorageType
from cloud_storage.excepts import UnsupportedStorage
from cloud_storage.local_storage import LocalStorage
from cloud_storage.gcs_storage import GoogleCloudStorage
from cloud_storage.s3_storage_boto3 import S3CloudStorageBoto3

STORAGE_CLIENT_MAPPING = {
    CloudStorageType.GCS: GoogleCloudStorage,
    CloudStorageType.LOCAL: LocalStorage,
    CloudStorageType.S3: S3CloudStorageBoto3,
}


def create_storage_client(name):
    """
    Return new CloudStorage client

    Args:
        name
    """
    try:
        client_class = STORAGE_CLIENT_MAPPING[name]
        return client_class()
    except KeyError:
        raise UnsupportedStorage('%s is not supported.' % name)


def int_or_str(value):
    try:
        return int(value)
    except ValueError:
        return value


VERSION = tuple(map(int_or_str, __version__.split('.')))

__all__ = (
    '__version__',
    'VERSION',
    'create_storage_client',
    'LocalStorage',
    'GoogleCloudStorage',
    'S3CloudStorageBoto3',
)
