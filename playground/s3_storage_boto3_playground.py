"""
:author: Gatsby Lee
:since: 2019-06-21
"""
import argparse
import logging

from cloud_storage import create_storage_client


LOGGER = logging.getLogger(__name__)


def _parse_args():
    parser = argparse.ArgumentParser()

    base_parser = argparse.ArgumentParser(add_help=False)
    base_parser.add_argument(
        '--bucket-name', help='bucket name', required=True)
    base_parser.add_argument(
        '--object-key', help='destination of blob', required=True)

    rename_arg_parser = argparse.ArgumentParser(add_help=False)
    rename_arg_parser.add_argument('--new-object-key', required=True)

    cmd_parser = parser.add_subparsers(dest='cmd')
    cmd_parser.required = True

    bucket_cmd_parser = cmd_parser.add_parser('bucket')
    bucket_cmd_subparser = bucket_cmd_parser.add_subparsers(dest='sub_cmd')
    bucket_cmd_subparser.required = True
    bucket_cmd_subparser.add_parser('list')

    upload_parser = cmd_parser.add_parser('upload', parents=[base_parser])
    upload_parser.add_argument('--upload-str')
    upload_parser.add_argument('--content-encoding')
    upload_parser.add_argument('--content-type')

    download_gzipped_parser = cmd_parser.add_parser(
        'download-gzipped', parents=[base_parser])
    download_gzipped_parser.add_argument(
        '--do-gunzip', action='store_true')
    download_gzipped_parser.add_argument(
        '--download-path')

    cmd_parser.add_parser('delete', parents=[base_parser])
    cmd_parser.add_parser('exists', parents=[base_parser])
    cmd_parser.add_parser('rename', parents=[base_parser, rename_arg_parser])

    return parser.parse_args()


def _main():

    args = _parse_args()

    client = create_storage_client('s3')
    if args.cmd == 'bucket' and args.sub_cmd == 'list':
        print(client.list_bucket_names())
    elif args.cmd == 'download-gzipped':
        if args.download_path:
            client.download_gzipped_to_file(
                args.bucket_name, args.object_key, args.download_path, args.do_gunzip)
        else:
            content = client.download_gzipped(
                args.bucket_name, args.object_key, args.do_gunzip)
            print(content)
    elif args.cmd == 'upload':
        upload_str = args.upload_str.encode()
        if args.content_encoding == 'gzip':
            import gzip
            upload_str = gzip.compress(upload_str)
            LOGGER.info('content-encoding=gzip. applying gzip.compress.')
        client.upload(args.bucket_name, args.object_key, upload_str,
                      args.content_type, args.content_encoding)
    elif args.cmd == 'delete':
        client.delete(args.bucket_name, args.object_key)
    elif args.cmd == 'exists':
        print(client.is_exists(args.bucket_name, args.object_key))
    elif args.cmd == 'rename':
        client.rename(args.bucket_name, args.object_key, args.new_object_key)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    _main()
