Cloud Storage
=============
Installation
------------

.. code-block:: bash

    pip install cloud_storage

Usage
-----

.. code-block:: bash

    from cloud_storage import GoogleCloudStorageHelper
    google_cloud_storage_helper = GoogleCloudStorageHelper()

Functions
---------

list_buckets()
~~~~~~~~~~~~~~

Returns list of all buckets

upload_blob_from_file(bucket_name, source_file_name, destination_blob_name, content_type, content_encoding, storage_class)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Upload a file into the cloud

.. csv-table::
    :header: "Name", "Description", "Required", "Type", "Accepted Values", "Default Value"
    :widths: 15, 25, 5, 10, 10, 15

    "bucket_name", "Name of bucket", "Yes", "String"
    "source_file_name", "Full File Path", "Yes", "String", "", ""
    "destination_blob_name", "Object key to be stored in Cloud", "Yes", "String", "", ""
    "content_type", "Encoding Type of Content in File", No, String, "text/plain, text/html, application/gzip, etc", ""
    "content_encoding", "Encoding used for uploading content", No, "String", "gzip", ""
    "storage_class", "", No, "String", "", ""

upload_blob_from_string(bucket_name, buffer, destination_blob_name, content_type, content_encoding, storage_class)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Upload a string into the cloud

.. csv-table::
    :header: "Name", "Description", "Required", "Type", "Accepted Values", "Default Value"
    :widths: 15, 25, 5, 10, 10, 15

    "bucket_name", "Name of bucket", "Yes", "String"
    "buffer", "Content String", "Yes", "String", "", ""
    "destination_blob_name", "Object key to be stored in Cloud", "Yes", "String", "", ""
    "content_type", "Encoding Type of Content in File", No, String, "text/plain, text/html, application/gzip, etc", ""
    "content_encoding", "Encoding used for uploading content", No, "String", "gzip", ""
    "storage_class", "", No, "String", "", ""

get_blob_exists(bucket_name, source_blob_name)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns True/False whether an object key get_blob_exists

.. csv-table::
    :header: "Name", "Description", "Required", "Type", "Accepted Values", "Default Value"
    :widths: 15, 25, 5, 10, 10, 15

    "bucket_name", "Name of bucket", "Yes", "String"
    "source_blob_name", "Object key in Cloud", "Yes", "String", "", ""

rename_blob(bucket_name, blob_name, new_blob_name)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Renames an object key

.. csv-table::
    :header: "Name", "Description", "Required", "Type", "Accepted Values", "Default Value"
    :widths: 15, 25, 5, 10, 10, 15

    "bucket_name", "Name of bucket", "Yes", "String"
    "blob_name", "Object key in Cloud", "Yes", "String", "", ""
    "new_blob_name", "New object key to be renamed to", "Yes", "String", "", ""

download_blob_to_file(bucket_name, source_blob_name, destination_file_name)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Downloads content and save to file

.. csv-table::
    :header: "Name", "Description", "Required", "Type", "Accepted Values", "Default Value"
    :widths: 15, 25, 5, 10, 10, 15

    "bucket_name", "Name of bucket", "Yes", "String"
    "source_blob_name", "Object key in Cloud", "Yes", "String", "", ""
    "destination_file_name", "File Path to save content to", "Yes", "String", "", ""

download_blob_as_string(bucket_name, source_blob_name)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns content from an object key

.. csv-table::
    :header: "Name", "Description", "Required", "Type", "Accepted Values", "Default Value"
    :widths: 15, 25, 5, 10, 10, 15

    "bucket_name", "Name of bucket", "Yes", "String"
    "source_blob_name", "Object key in Cloud", "Yes", "String", "", ""

delete_blob(bucket_name, blob_name)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Delete an object key from cloud

.. csv-table::
    :header: "Name", "Description", "Required", "Type", "Accepted Values", "Default Value"
    :widths: 15, 25, 5, 10, 10, 15

    "bucket_name", "Name of bucket", "Yes", "String"
    "blob_name", "Object key in Cloud", "Yes", "String", "", ""
