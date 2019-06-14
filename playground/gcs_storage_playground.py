import argparse
import logging

from cloud_storage.gcs_storage import GoogleCloudStorage

DEFAULT_LOG_FORMAT_STRING = "%(asctime)s (%(filename)s, %(funcName)s, %(lineno)d) [%(levelname)8s] %(message)s"

LOGGER = logging.getLogger(__name__)


def _parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)

    base_parser = argparse.ArgumentParser(add_help=False)
    base_parser.add_argument(
        '--bucket-name', default='playground-test-bucket', help='bucket name')
    base_parser.add_argument(
        '--object-key', default='test/key/1.html', help='destination of blob')

    upload_parser = argparse.ArgumentParser(add_help=False)
    upload_parser.add_argument(
        '--upload-str', default='Test Upload String', help='string value to upload for testing')

    download_parser = argparse.ArgumentParser(add_help=False)
    download_parser.add_argument(
        '--download-path', help='path to download blob')

    command_subparser = parser.add_subparsers(dest='sub_command')
    command_subparser.required = True

    command_subparser.add_parser(
        'upload', parents=[base_parser, upload_parser])
    command_subparser.add_parser(
        'download', parents=[base_parser, download_parser])
    command_subparser.add_parser('exists', parents=[base_parser])
    command_subparser.add_parser('delete', parents=[base_parser])

    return parser.parse_args()


def _main():
    options = _parse_args()
    bucket_name = options.bucket_name
    object_key = options.object_key

    gcs_storage = GoogleCloudStorage()

    if options.sub_command == 'upload':
        upload_str = options.upload_str.encode('utf-8')
        content_type = 'text/html'
        content_encoding = None
        gcs_storage.upload(bucket_name, upload_str,
                           object_key, content_type, content_encoding)
    elif options.sub_command == 'download':
        download_path = options.download_path
        if download_path:
            gcs_storage.download_to_file(
                bucket_name, object_key, download_path)
        else:
            content = gcs_storage.download(bucket_name, object_key)
            LOGGER.info(content)
    elif options.sub_command == 'exists':
        exists = gcs_storage.is_exists(bucket_name, object_key)
        LOGGER.info(exists)
    elif options.sub_command == 'delete':
        gcs_storage.delete(bucket_name, object_key)


if __name__ == '__main__':
    logging.basicConfig(format=DEFAULT_LOG_FORMAT_STRING,
                        datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)
    _main()
