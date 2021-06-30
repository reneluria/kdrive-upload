import argparse
import sys
from .kdrive import KDrive


class CustomFormatter(
    argparse.RawDescriptionHelpFormatter, argparse.ArgumentDefaultsHelpFormatter
):
    pass


def main():
    parser = argparse.ArgumentParser(
        description="Upload to kDrive", prog="kdrive_upload"
    )
    parser.add_argument("--drive", default="mydrive")
    parser.add_argument("--keep", action="store_true", help="keep files after upload")
    parser.add_argument("dest", help="destination directory")
    parser.add_argument("file", type=argparse.FileType(), help="file to upload")
    args = parser.parse_args()
    try:
        kdrive = KDrive(args.drive)
    except ValueError as err:
        sys.exit(str(err))
    kdrive.upload(args.dest, args.file, args.keep)


if __name__ == "__main__":
    main()
