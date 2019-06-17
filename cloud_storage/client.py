from cloud_storage.gcs_storage import GoogleCloudStorage

def create_storage_client(name):
    return GoogleCloudStorage()

__all__ = (
    'create_storage_client',
    'GoogleCloudStorage',
)
