import enum


class StringEnum(str, enum.Enum):
    def __str__(self):
        return self.value


class CloudStorageType(StringEnum):
    GCS = "gcs"
    LOCAL = "local"
    S3 = "s3"
