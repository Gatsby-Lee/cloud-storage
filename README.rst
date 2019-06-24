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


Playground Download
-------------------

* gcs_storage_playground.py
* s3_storage_boto3_playground.py

.. code-block:: bash

    python playground/<play_ground_module> upload --bucket-name <your_bucket> \
        --object-key "test_sample.html" \
        --upload-str "<html>hello</html>" \
        --content-encoding="gzip" \
        --content-type="text/html"

    python playground/<play_ground_module> download-gzipped --bucket-name <your_bucket> \
        --object-key "test_sample.html"

    python playground/<play_ground_module> download-gzipped --bucket-name <your_bucket> \
        --object-key "test_sample.html" \
        --do-gunzip

    python playground/<play_ground_module> download-gzipped --bucket-name <your_bucket> \
        --object-key "test_sample.html" \
        --download-path='test_sample.html'

    python playground/<play_ground_module> download-gzipped --bucket-name <your_bucket> \
        --object-key "test_sample.html" \
        --do-gunzip \
        --download-path test_sample.html


Playground Rename
-----------------

* gcs_storage_playground.py
* s3_storage_boto3_playground.py

.. code-block:: bash

    python playground/<play_ground_module> rename --bucket-name <your_bucket> \
        --object-key "test_sample.html" --new-object-key "test_sample1.html"


Playground Exists
-----------------

* gcs_storage_playground.py
* s3_storage_boto3_playground.py

.. code-block:: bash

    python playground/<play_ground_module> exists --bucket-name <your_bucket> \
        --object-key "test_sample1.html"


Playground Delete
-----------------

* gcs_storage_playground.py
* s3_storage_boto3_playground.py

.. code-block:: bash

    python playground/<play_ground_module> delete --bucket-name <your_bucket> \
        --object-key "test_sample1.html"
