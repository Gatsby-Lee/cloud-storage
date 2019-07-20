.. image:: https://badge.fury.io/py/cloud-storage.svg
    :target: https://badge.fury.io/py/cloud-storage

Cloud Storage
=============

Why this is built?
------------------

In order to provide interface for upload, download, and exceptions for AWS S3 and GCS.

If you have use cases using both Cloud Storage in one project, You might want to try this package.

I'm also using this on production as well.


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
