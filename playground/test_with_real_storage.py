import argparse


def run_functionality_tests(client, bucket_name):

    import gzip
    import time
    content = b"<html>hello world - %b</html>" % str(time.time()).encode()
    gzipped_content = gzip.compress(content)
    content_encoding = 'gzip'
    content_type = 'text/html'
    object_key = 'cloud_storage_test.html'
    new_object_key = "renamed/%s" % object_key

    # setup: delete expected test object
    client.delete(bucket_name, object_key)
    client.delete(bucket_name, new_object_key)
    assert(client.is_exists(bucket_name, object_key) is False)
    assert(client.is_exists(bucket_name, new_object_key) is False)

    # test1: upload testing content
    client.upload(bucket_name, object_key, gzipped_content,
                  content_type, content_encoding)
    assert(client.is_exists(bucket_name, object_key) is True)

    # test2: download gzipped with do_gunzip=True
    test_content = client.download_gzipped(
        bucket_name, object_key, do_gunzip=True)
    assert(content == test_content), "{} != {}".format(
        gzipped_content, test_content)

    # test3: download gzipped with do_gunzip=False
    test_gzipped_content = client.download_gzipped(
        bucket_name, object_key, do_gunzip=False)
    test_content = gzip.decompress(test_gzipped_content)
    assert(content == test_content), "{} != {}".format(
        gzipped_content, test_content)

    # test4: renaming
    client.rename(bucket_name, object_key, new_object_key)
    assert(client.is_exists(bucket_name, object_key) is False)
    assert(client.is_exists(bucket_name, new_object_key) is True)

    # test4: deleting
    client.delete(bucket_name, object_key)
    client.delete(bucket_name, new_object_key)
    assert(client.is_exists(bucket_name, object_key) is False)
    assert(client.is_exists(bucket_name, new_object_key) is False)

    # test5: handling slash(/)
    object_key_with_prefix_slash = '///%s' % object_key
    client.delete(bucket_name, object_key_with_prefix_slash)
    assert(client.is_exists(bucket_name, object_key_with_prefix_slash) is False)

    client.upload(bucket_name, object_key_with_prefix_slash, gzipped_content,
                  content_type, content_encoding)
    assert(client.is_exists(bucket_name, object_key) is False)
    assert(client.is_exists(bucket_name, object_key_with_prefix_slash) is True)
    client.delete(bucket_name, object_key_with_prefix_slash)
    assert(client.is_exists(bucket_name, object_key_with_prefix_slash) is False)

    # test6: slash in middle of object key
    object_key_with_slash_in_middle = 'a//b//%s' % object_key
    possible_normalized_object_key = 'a/b/%s' % object_key
    client.delete(bucket_name, object_key_with_slash_in_middle)
    client.delete(bucket_name, possible_normalized_object_key)
    assert(client.is_exists(bucket_name, object_key_with_slash_in_middle) is False)
    assert(client.is_exists(bucket_name, possible_normalized_object_key) is False)
    client.upload(bucket_name, object_key_with_slash_in_middle, gzipped_content,
                  content_type, content_encoding)
    assert(client.is_exists(bucket_name, possible_normalized_object_key) is False)
    assert(client.is_exists(bucket_name, object_key_with_slash_in_middle) is True)
    client.delete(bucket_name, object_key_with_slash_in_middle)
    assert(client.is_exists(bucket_name, object_key_with_slash_in_middle) is False)


def _parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('--bucket-name')

    return parser.parse_args()


if __name__ == '__main__':

    from cloud_storage import create_storage_client
    args = _parse_args()

    for s in ['gcs', 's3']:
        print('testing cloud-storage=%s' % s)
        client = create_storage_client(s)
        run_functionality_tests(client, args.bucket_name)
