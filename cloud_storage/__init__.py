from cloud_storage.__about__ import __version__
from cloud_storage.excepts import UnsupportedStorage
from cloud_storage.gcs_storage import GoogleCloudStorage
from cloud_storage.s3_storage_boto3 import S3CloudStorageBoto3

STORAGE_CLIENT_MAPPING = {
    'gcs': (GoogleCloudStorage,),
    's3': (S3CloudStorageBoto3,),
}


def create_storage_client(name):
    """
    Return new CloudStorage client

    Args:
        name
    """
    try:
        client_info = STORAGE_CLIENT_MAPPING[name]
    except KeyError:
        raise UnsupportedStorage('%s is not supported.' % name)
    return client_info[0]()


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
    'GoogleCloudStorage',
    'S3CloudStorageBoto3',
)
