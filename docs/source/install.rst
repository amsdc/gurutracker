""""""""""
Quickstart
""""""""""

.. contents:: Overview
   :depth: 3

...............................
For those who don't know Python
...............................
==================
Windows Installers
==================

Coming Soon!

======================
Manual Install
======================

Initial steps
=============

#. Go to the `github repository`_.
#. Download the ZIP file by clicking the button ``Download ZIP``.
#. Unzip it to a given folder.
   
   For Windows, the  recommended folder is 
   ``%USERPROFILE%\AppData\Local\AMSDC\Gurutracker``. In other words, 
   paste ``%USERPROFILE%\AppData\Local`` into the File Explorer bar 
   (where the directory path is shown with arrows), then create the 
   folder ``AMSDC``, and then inside that ``Gurutracker``.

Chossing the right database adapter
===================================

.. csv-table:: Comparison of in-built data adapters
   :file: _static/tables/database_adapter_comparison.csv
   :widths: 20, 40, 40
   :header-rows: 1

.. note:: 
   If you are unsure of which adapter to choose, then choose MySQL as 
   the database backend, as it is easier to update versions and can 
   handle large amounts of data easily.

MySQL
-----

SQLite3
-------
There is no need to do anything, as by default, SQLite3 is the default 
database backend.

.. _`github repository`: https://github.com/amsdc/gurutracker