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

    cmd_parser = parser.add_subparsers(dest='cmd')
    cmd_parser.required = True

    upload_parser = cmd_parser.add_parser('upload', parents=[base_parser])
    upload_parser.add_argument('--upload-str', required=True)
    upload_parser.add_argument('--content-encoding')
    upload_parser.add_argument('--content-type')

    download_gzipped_parser = cmd_parser.add_parser(
        'download-gzipped', parents=[base_parser])
    download_gzipped_parser.add_argument(
        '--do-gunzip', action='store_true')
    download_gzipped_parser.add_argument(
        '--download-path')

    cmd_parser.add_parser('exists', parents=[base_parser])
    cmd_parser.add_parser('delete', parents=[base_parser])

    return parser.parse_args()


def _main():
    args = _parse_args()
    bucket_name = args.bucket_name
    object_key = args.object_key

    client = GoogleCloudStorage()

    if args.cmd == 'upload':
        upload_str = args.upload_str.encode('utf-8')
        if args.content_encoding == 'gzip':
            import gzip
            upload_str = gzip.compress(upload_str)
            LOGGER.info('content-encoding=gzip. applying gzip.compress.')
        client.upload(bucket_name, object_key, upload_str,
                      args.content_type, args.content_encoding)
    elif args.cmd == 'download-gzipped':
        if args.download_path:
            client.download_gzipped_to_file(
                args.bucket_name, args.object_key, args.download_path, args.do_gunzip)
        else:
            content = client.download_gzipped(
                args.bucket_name, args.object_key, args.do_gunzip)
            print(content)
    elif args.cmd == 'exists':
        exists = client.is_exists(bucket_name, object_key)
        print(exists)
    elif args.cmd == 'delete':
        client.delete(bucket_name, object_key)


if __name__ == '__main__':
    logging.basicConfig(format=DEFAULT_LOG_FORMAT_STRING,
                        datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)
    _main()
