import os
from webdav3.client import Client
import webdav3.exceptions
import configparser


class KDrive:
    _url = "https://connect.drive.infomaniak.com"

    def __init__(self, drive):
        config = configparser.ConfigParser()
        files = config.read(["/etc/kdrive-upload.cfg", "kdrive-upload.cfg", os.path.expanduser("~/.config/kdrive-upload.cfg")])
        config_username = None
        config_password = None
        if len(files) > 0:
            try:
                config_username = config.get('credentials', 'username')
                config_password = config.get('credentials', 'password')
            except configparser.NoOptionError:
                raise ValueError("Wrong options in {}".format(files))
            except configparser.NoSectionError:
                raise ValueError("No section credentials in {}".format(files))
        # override with env vars
        self._username = os.getenv("DRIVE_USERNAME", config_username)
        self._password = os.getenv("DRIVE_PASSWORD", config_password)
        if self._username is None or self._password is None:
            raise ValueError("No credentials provided")
        options = {
            'webdav_hostname': self._url,
            'webdav_login': self._username,
            'webdav_password': self._password,
            'webdav_disable_check': True,
        }
        client = Client(options)
        self._client = client
        self._basepath = drive

    def mkdir_p(self, path):
        parent = os.path.dirname(path)
        if parent == self._basepath:
            raise ValueError("Would not create the drive itself")
        try:
            self._client.mkdir(parent)
        except webdav3.exceptions.ResponseErrorCode as err:
            if err.code == 409:
                self.mkdir_p(parent)
                print("mkdir {}".format(parent))
                self._client.mkdir(parent)
            else:
                raise

    def upload(self, dest, file, keep=False):
        dest_filename = "{}/{}/{}".format(self._basepath, dest, os.path.basename(file.name))
        try:
            self._client.upload_sync(dest_filename, file.name)
        except webdav3.exceptions.ResponseErrorCode as err:
            if err.code == 409:
                # Files cannot be created in non-existent collections
                self.mkdir_p(dest_filename)
                self._client.upload_sync(dest_filename, file.name)
            else:
                raise
        print("{} uploaded to {}".format(file.name, dest_filename))
        if not keep:
            os.unlink(file.name)
            print("{} removed".format(file.name))
