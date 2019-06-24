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
        '--bucket-name', required=True, help='bucket name')
    base_parser.add_argument(
        '--object-key', required=True, help='destination of blob')

    cmd_parser = parser.add_subparsers(dest='sub_command')
    cmd_parser.required = True

    upload_parser = cmd_parser.add_parser('upload', parents=[base_parser])
    upload_parser.add_argument('--upload-str', required=True)
    upload_parser.add_argument('--content-encoding')
    upload_parser.add_argument('--content-type')

    download_parser = cmd_parser.add_parser('download', parents=[base_parser])
    download_parser.add_argument(
        '--download-path', help='path to download blob')

    cmd_parser.add_parser('exists', parents=[base_parser])
    cmd_parser.add_parser('delete', parents=[base_parser])

    return parser.parse_args()


def _main():
    args = _parse_args()
    bucket_name = args.bucket_name
    object_key = args.object_key

    client = GoogleCloudStorage()

    if args.sub_command == 'upload':
        upload_str = args.upload_str.encode('utf-8')
        if args.content_encoding == 'gzip':
            import gzip
            size_before_compression = len(upload_str)
            upload_str = gzip.compress(upload_str)
            size_after_compression = len(upload_str)
            LOGGER.info(
                'content-encoding=gzip. applying gzip.compress. before:%s, after:%s',
                size_before_compression, size_after_compression)
        client.upload(bucket_name, object_key, upload_str,
                      args.content_type, args.content_encoding)
    elif args.sub_command == 'download':
        download_path = args.download_path
        if download_path:
            client.download_to_file(
                bucket_name, object_key, download_path)
        else:
            content = client.download(bucket_name, object_key)
            print(content)
    elif args.sub_command == 'exists':
        exists = client.is_exists(bucket_name, object_key)
        print(exists)
    elif args.sub_command == 'delete':
        client.delete(bucket_name, object_key)


if __name__ == '__main__':
    logging.basicConfig(format=DEFAULT_LOG_FORMAT_STRING,
                        datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)
    _main()
