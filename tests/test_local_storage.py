import os
import shutil

import pytest

from cloud_storage import LocalStorage

LOCAL_STORAGE_ROOT_DIR = '/tmp/local_storage_test'


@pytest.fixture
def storage():
    try:
        shutil.rmtree(LOCAL_STORAGE_ROOT_DIR)
    except FileNotFoundError:
        pass
    return LocalStorage(LOCAL_STORAGE_ROOT_DIR)


def test_get_full_path(storage):
    full_path = storage._get_full_path('abc', 'efg.txt')
    expected_path = '/tmp/local_storage_test/abc/efg.txt'
    assert os.path.normpath(full_path) == os.path.normpath(expected_path)


def test_list_bucket_names(storage):
    buckets = storage.list_bucket_names()
    assert buckets == []


def test_create_bucket(storage):
    storage.create_bucket('abc')
    buckets = storage.list_bucket_names()
    assert buckets == ['abc']


def test_upload(storage):
    bucket_name = 'abc'
    object_key = 'hello.txt'
    buffer = b'world'
    storage.create_bucket(bucket_name)
    storage.upload(bucket_name, object_key, buffer)

    assert storage.is_exists(bucket_name, object_key) is True
