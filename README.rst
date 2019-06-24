.. image:: https://badge.fury.io/py/cloud-storage.svg
    :target: https://badge.fury.io/py/cloud-storage

=============
Cloud Storage
=============

Installation
------------

.. code-block:: bash

    pip install cloud-storage


How to use
----------

.. code-block:: python

    >>> from cloud_storage import GoogleCloudStorage
    >>> storage = GoogleCloudStorage()


.. code-block:: python

    >>> from cloud_storage import create_storage_client
    >>> storage = create_storage_client()


Playground Test - GCS
---------------------

.. code-block:: python

    python playground/gcs_storage_playground.py upload --bucket-name <your_bucket> \
        --object-key "test_sample.html" \
        --upload-str "<html>hello</html>" \
        --content-encoding="gzip" \
        --content-type="text/html"

    python playground/gcs_storage_playground.py download-gzipped --bucket-name <your_bucket>
        --object-key "test_sample.html"

    python playground/gcs_storage_playground.py download-gzipped --bucket-name <your_bucket>
        --object-key "test_sample.html" \
        --do-gunzip

    python playground/gcs_storage_playground.py download-gzipped --bucket-name <your_bucket>
        --object-key "test_sample.html" \
        --download-path='test_sample.html'

    python playground/gcs_storage_playground.py download-gzipped --bucket-name <your_bucket>
        --object-key "test_sample.html" \
        --do-gunzip \
        --download-path test_sample.html


Playground Test - S3
---------------------

.. code-block:: python

    python playground/s3_storage_boto3_playground.py upload --bucket-name <your_bucket> \
        --object-key "test_sample.html" \
        --upload-str "<html>hello</html>" \
        --content-encoding="gzip" \
        --content-type="text/html"

    python playground/s3_storage_boto3_playground.py download-gzipped --bucket-name <your_bucket>
        --object-key "test_sample.html"

    python playground/s3_storage_boto3_playground.py download-gzipped --bucket-name <your_bucket>
        --object-key "test_sample.html" \
        --do-gunzip

    python playground/s3_storage_boto3_playground.py download-gzipped --bucket-name <your_bucket>
        --object-key "test_sample.html" \
        --download-path='test_sample.html'

    python playground/s3_storage_boto3_playground.py download-gzipped --bucket-name <your_bucket>
        --object-key "test_sample.html" \
        --do-gunzip \
        --download-path test_sample.html
