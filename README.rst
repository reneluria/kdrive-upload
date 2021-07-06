kdrive\_upload
==============

Upload files to `kDrive -
Infomaniak <https://www.infomaniak.com/kdrive>`__

Installation
------------

.. code:: shell

    python3 setup.py install

Configuration
-------------

Create an app password here:
https://manager.infomaniak.com/v3/profile/application-password

Then you create a file ``kdrive-upload.cfg`` inside current directory,
or ``~/.config/kdrive-upload.cfg`` or ``/etc/kdrive-upload.cfg`` like
this:

.. code:: ini

    [credentials]
    username = xxx
    password = xxx

You can also export ``KDRIVE_USERNAME`` or ``KDRIVE_PASSWORD``
environment variables to override these

Usage
-----

.. code:: shell

    $ kdrive-upload --help
    usage: kdrive_upload [-h] [--drive DRIVE] [--keep] dest file

    Upload to kDrive

    positional arguments:
      dest           destination directory
      file           file to upload

    optional arguments:
      -h, --help     show this help message and exit
      --drive DRIVE
      --keep         keep files after upload

As you can see, by default it deletes local file after upload
