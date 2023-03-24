=====================
Configuration files
=====================

------------
Location
------------

By default, Gurutracker searches for configuration files in the 
following order, and reads the first one it encounters:

.. code-block:: python

   ["./configuration.ini",
   "~/.gurutracker/configuration.ini"]

.. note::
   The ``~/`` denotes your User home folder path. On Windows, this is
   ``%USERPROFILE%\`` or ``C:\Users\<Username>\``

By default, Gurutracker will use its default inbuilt settings, if both 
these files do not exist.

--------
Syntax
--------

The syntax of the configuration file is similar to that of Windows INI 
files. For a detailed explanation, see the Python documentation for the
`configparser module`_.

A simple example is below:

.. code-block:: ini

   [This is a section]
   this_is_an_option = with a value ;and this is a comment

.. _`configparser module`: https://docs.python.org/3/library/configparser.html#supported-ini-file-structure

-----------
Data types
-----------
There are 4 data types in the INI specification.

* **string**: A riting is a sequence of characters. Strings need not be
  enclosed in quotes as long as it does not contain the ``=``, ``[`` or 
  ``]`` character. Strings can be multiline too, as shown below:

  .. code-block:: ini
     
     [Multiline Values]
     chorus: I'm a lumberjack, and I'm okay
         I sleep all night and I work all day
  
  Note that the indentation at the beginning of the second line is 
  important.

  .. note::

     Under no circumstances can strings contain the ``#`` and ``;``
     characters, as these are reserved by the parser for comments.
* **boolean**: Config files can contain simple boolean values. A 
  boolean value can take two values - ``true``, which denotes an 'on' 
  state, and ``false``, which denotes an 'off' state. The parser 
  supports some other aliases for boolean values, as listed:

  .. list-table:: Aliases for boolean values

     * - ``true``
       - ``1``
       - ``yes``
       - ``on``
     * - ``false``
       - ``0``
       - ``no``
       - ``off``

------------------------
Configuration variables
------------------------

Database section
=================

.. csv-table:: 
   :file: ../_static/tables/cfg_database.csv
   :widths: 30, 40, 30
   :header-rows: 1

Here is a comparison of the in-built database adapters:

.. csv-table:: Comparison of in-built data adapters
   :file: ../_static/tables/database_adapter_comparison.csv
   :widths: 20, 40, 40
   :header-rows: 1

Storage section
===============

.. csv-table:: 
   :file: ../_static/tables/cfg_storage.csv
   :widths: 30, 40, 30
   :header-rows: 1

Options for ``filesystem.directory``
------------------------------------

.. csv-table:: 
   :file: ../_static/tables/cfg_st_filesystem.directory.csv
   :widths: 30, 40, 30
   :header-rows: 1

Notes section
==============

.. csv-table:: 
   :file: ../_static/tables/cfg_notes.csv
   :widths: 30, 40, 30
   :header-rows: 1

GUI preferences
================

.. csv-table:: 
   :file: ../_static/tables/cfg_gui.csv
   :widths: 30, 40, 30
   :header-rows: 1
