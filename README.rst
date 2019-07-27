
.. image:: https://img.shields.io/badge/License-GPL%20v3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0

.. image:: https://badge.fury.io/py/cloud-storage.svg
    :target: https://pypi.org/project/cloud-storage/

.. image:: https://img.shields.io/travis/Gatsby-Lee/cloud-storage.svg
   :target: https://travis-ci.org/Gatsby-Lee/cloud-storage


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

    # For Google Cloud Storage
    >>> from cloud_storage import GoogleCloudStorage
    >>> storage = GoogleCloudStorage()
    # For AWS S3
    >>> storage = S3CloudStorageBoto3()


.. code-block:: python

    # using factory
    >>> from cloud_storage import create_storage_client
    >>> gcs_storage = create_storage_client('gcs')
    >>> s3_storage = create_storage_client('s3')

