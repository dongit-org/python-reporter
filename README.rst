python-reporter
===============

.. image:: https://github.com/dongit-org/python-reporter/workflows/test/badge.svg
   :target: https://github.com/dongit-org/python-reporter/actions
   :alt: Test Status

.. image:: https://codecov.io/gh/dongit-org/python-reporter/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/dongit-org/python-reporter
   :alt: Code Coverage

.. image:: https://readthedocs.org/projects/python-reporter/badge/?version=latest
   :target: https://python-reporter.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/securityreporter
   :target: https://pypi.org/project/securityreporter/
   :alt: PyPI

A Python wrapper around the `Reporter <https://securityreporter.app>`_ API.

Currently compatible with Reporter version `2022.08.04 <https://securityreporter.app/releases/20220804>`_.

Installation
------------

Currently, :code:`python-reporter` is compatible with Python 3.7+.

Use :code:`pip` to install the package:

.. code:: bash

    pip install --upgrade securityreporter

Documentation
-------------

Documentation is available on `Read the Docs <https://python-reporter.readthedocs.io/>`_.

About Reporter
---------------

.. image:: https://raw.githubusercontent.com/dongit-org/python-reporter/main/docs/_static/reporter_logo.png
   :target: https://securityreporter.app/
   :alt: Reporter Logo

Reporter is an all-in-one pentest reporting workspace designed to help your team organize pentests, interact with clients, and create high quality pentest reports.

Reporter is designed to allow managers to delegate tasks to individual pentesters easily. The pentesters in turn are easily able to see which tasks are assigned, and they can access all required assessment details to get started.

Reporter supports granular access control distinctions, ensuring that every user only has access to that which they are required to have access to.

With Reporter clients may directly interact with researchers or other team members. After research findings are published, clients may ask questions regarding specific findings, or they may request retests.

Reporter has many functionalities, such as custom and built-in finding templates and automatic PDF generation, that will save you large amounts of time during your research.