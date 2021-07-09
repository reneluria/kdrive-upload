import os
from http.client import HTTPConnection
from webdav3.client import Client
import webdav3.exceptions
import configparser

HTTPConnection.debuglevel = 1

client = Client(
    {
        "webdav_hostname": "https://connect.drive.infomaniak.com",
        "webdav_login": os.getenv("DRIVE_USERNAME"),
        "webdav_password": os.getenv("DRIVE_PASSWORD"),
        "webdav_disable_check": True,
    }
)
