"""
@author Henley Kuang
@since 2019-06-13

@note: classes are in alphabetical order
"""


class UploadBadRequestException(Exception):
    pass


class UploadServerErrorException(Exception):
    pass


class UploadUnknownErrorException(Exception):
    pass


__all__ = (
    'UploadBadRequestException',
    'UploadServerErrorException',
    'UploadUnknownErrorException',
)
