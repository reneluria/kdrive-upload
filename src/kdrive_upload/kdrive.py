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
                raise ValueError(f"Wrong options in {files}")
            except configparser.NoSectionError:
                raise ValueError(f"No section credentials in {files}")
        # override with env vars
        self._username = os.getenv("DRIVE_USERNAME", config_username)
        self._password = os.getenv("DRIVE_PASSWORD", config_password)
        if self._username is None or self._password is None:
            raise ValueError("No credentials provided")
        options = {
            'webdav_hostname': self._url,
            'webdav_login': self._username,
            'webdav_password': self._password,
            'verbose': True
        }
        client = Client(options)
        self._client = client
        self._basepath = drive

    def mkdir_p(self, path):
        directory = f"{self._basepath}/{path}"
        try:
            self._client.info(directory)
        except webdav3.exceptions.RemoteResourceNotFound:
            print(f"Creating directory {directory}")
            self._client.mkdir(directory)
        return directory

    def upload(self, dest, file, keep=False):
        dest_filename = os.path.basename(file.name)
        directory = self.mkdir_p(dest)
        self._client.upload_sync(f"{directory}/{dest_filename}", file.name)
        print(f"{file.name} uploaded to {directory}/{dest_filename}")
        if not keep:
            os.unlink(file.name)
            print(f"{file.name} removed")
