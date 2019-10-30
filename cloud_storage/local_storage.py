"""
:author: Gatsby Lee
:since: 2019-08-09
"""
import hashlib
import os
import gzip
import shutil

LOCAL_STORAGE_ROOT = '/tmp/local_storage'


class LocalStorage(object):

    def __init__(self, root_dir=LOCAL_STORAGE_ROOT):
        self._root_dir = root_dir
        if not os.path.exists(self._root_dir):
            os.mkdir(self._root_dir)

    def _get_full_path(self, bucket_name, object_key):
        object_key_hash = hashlib.md5(object_key.encode("utf-8")).hexdigest()
        bucket_directory = os.path.join(self._root_dir, bucket_name)
        if not os.path.exists(bucket_directory):
            self.create_bucket(bucket_name)
        return os.path.join(self._root_dir, bucket_name, object_key_hash)

    def create_bucket(self, bucket_name):
        """
        Create bucket
        """
        bucket_path = os.path.join(self._root_dir, bucket_name)
        os.mkdir(bucket_path)

    def list_bucket_names(self):
        """Return list of bucket names

        Returns:
            bucket_names(list)
        """
        bucket_names = []
        for x in os.listdir(self._root_dir):
            if os.path.isdir(os.path.join(self._root_dir, x)):
                bucket_names += x,
        return bucket_names

    def upload_file(self, bucket_name, object_key, source_file_name,
                    content_type=None, content_encoding=None):
        """
        Uploads a local file to a bucket
        """
        full_path = self._get_full_path(bucket_name, object_key)
        if content_encoding == 'gzip':
            with gzip.open(full_path, 'wb') as fw:
                with open(source_file_name, 'rb') as fr:
                    fw.write(fr.read())
        else:
            shutil.copy(source_file_name, full_path)

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

        full_path = self._get_full_path(bucket_name, object_key)
        if content_encoding == 'gzip':
            with gzip.open(full_path, 'wb') as fw:
                fw.write(buffer)
        else:
            with open(full_path, 'wb') as fw:
                fw.write(buffer)

    def is_exists(self, bucket_name, object_key):
        """Check if an object exists in bucket

        Args:
            bucket_name (str):  Bucket name to use
            object_key (str): Object key stored in bucket

        Returns:
            True if exists.
        """
        full_path = self._get_full_path(bucket_name, object_key)
        return os.path.exists(full_path)

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

        shutil.move(
            self._get_full_path(bucket_name, object_key),
            self._get_full_path(bucket_name, new_object_key),
        )

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
        src_full_path = self._get_full_path(bucket_name, object_key)
        dest_full_path = self._get_full_path(bucket_name, object_key)
        if do_gunzip:
            with gzip.open(src_full_path, 'rb') as fr:
                with open(dest_full_path, 'wb') as fw:
                    fw.write(fr.read())
        else:
            shutil.copy(src_full_path, dest_full_path)

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
        full_path = self._get_full_path(bucket_name, object_key)
        if do_gunzip:
            with gzip.open(full_path, 'rb') as fr:
                return fr.read()
        else:
            with open(full_path, 'rb') as fr:
                return fr.read()

    def delete(self, bucket_name, object_key):
        """Delete an object from bucket

        Args:
            bucket_name(str):  Bucket name to use
            object_key(str): Object Key to rename
        Returns:
            None
        @note: No exception raises although object doesn't exist.
        """
        full_path = self._get_full_path(bucket_name, object_key)
        os.remove(full_path)
