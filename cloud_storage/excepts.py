"""
@author Henley Kuang
@since 2019-06-13

@note: classes are in alphabetical order
"""


class CloudStorageBadRequestException(Exception):
    pass


class CloudStorageInvalidArgumentTypeException(Exception):
    pass


class CloudStorageServerErrorException(Exception):
    pass


class CloudStorageUnknownErrorException(Exception):
    pass


__all__ = (
    'CloudStorageBadRequestException',
    'CloudStorageInvalidArgumentTypeException',
    'CloudStorageServerErrorException',
    'CloudStorageUnknownErrorException',
)
