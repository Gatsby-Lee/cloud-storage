"""
:author: Gatsby Lee
:since: 2019-04-10
"""
import boto3
import pytest

from moto import mock_s3
from cloud_storage import S3CloudStorageBoto3


def test_init_obj():
    """
    Test that RedisQueue instance could be created with
    default value argument.
    """
    S3CloudStorageBoto3()


@mock_s3
def test_list_bucket_names():
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket='cloud-storage-test')
    assert S3CloudStorageBoto3().list_bucket_names() == ['cloud-storage-test']


@mock_s3
def test_upload():
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket='cloud-storage-test')

    bucket_name = 'cloud-storage-test'
    object_key = '1/2/3/4.txt'
    buffer = 'hello world'
    with pytest.raises(AssertionError):
        assert S3CloudStorageBoto3().upload(
            bucket_name, object_key, buffer
        )

    buffer = b'hello world'
    assert S3CloudStorageBoto3().upload(
        bucket_name, object_key, buffer
    ) is None


@mock_s3
def test_is_exists():
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket='cloud-storage-test')

    bucket_name = 'cloud-storage-test'
    object_key = '1/2/3/4.txt'
    buffer = 'hello world'

    buffer = b'hello world'
    S3CloudStorageBoto3().upload(bucket_name, object_key, buffer)
    assert S3CloudStorageBoto3().is_exists(bucket_name, object_key) is True
