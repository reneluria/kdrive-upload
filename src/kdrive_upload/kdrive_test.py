import pytest
import kdrive_upload.kdrive
import os


def test_kdrive_drive_needed():
    """One should provide the drive to upload to"""
    with pytest.raises(TypeError):
        kdrive_upload.kdrive.KDrive()


def test_kdrive_environ():
    """Use env vars"""
    os.environ['DRIVE_USERNAME'] = "john1"
    os.environ['DRIVE_PASSWORD'] = "password"

    kdrive = kdrive_upload.kdrive.KDrive('mydrive')

    assert kdrive._username == "john1"
    assert kdrive._password == "password"

    del(os.environ["DRIVE_USERNAME"])
    del(os.environ["DRIVE_PASSWORD"])


def test_kdrive_cfg():
    """Use cfg file"""
    cfg = """
[credentials]
username = johncfg
password = hello
"""
    with open("kdrive-upload.cfg", "w") as f:
        f.write(cfg)

    try:
        kdrive = kdrive_upload.kdrive.KDrive('mydrive')

        assert kdrive._username == "johncfg"
        assert kdrive._password == "hello"

    finally:
        os.unlink("kdrive-upload.cfg")


def test_kdrive_cfg_environ():
    """Override config file with environment"""
    cfg = """
[credentials]
username = john2
password = hello
"""
    with open("kdrive-upload.cfg", "w") as f:
        f.write(cfg)

    try:

        os.environ['DRIVE_USERNAME'] = "lucy"

        kdrive = kdrive_upload.kdrive.KDrive('mydrive')

        assert kdrive._username == "lucy"
        assert kdrive._password == "hello"

    finally:
        os.unlink("kdrive-upload.cfg")
        del(os.environ['DRIVE_USERNAME'])
