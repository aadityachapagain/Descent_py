# Google Cloud Settings

"""Google Cloud Storage Configuration."""
import zipfile
import os
from os import environ, listdir
from os.path import isfile, join
from io import BytesIO, StringIO

from google.cloud import storage

import logging
FORMAT = '%(asctime)-15s %(name)s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger("data.storage.gcp")
logger.setLevel("INFO")


class GCP_Service(object):
    _obj = None

    def __new__(cls, *args, **kargs):
        if cls._obj:
            return cls._obj
        else:
            instance = super(GCP_Service, cls).__new__(cls, *args, **kargs)
            cls._obj = instance
            return instance


    def __init__(self, bucket_name:str = None):
        # Google Cloud Storage
        logger.info("Initializing GCP services..")
        self.bucket_name = environ.get('GCP_BUCKET_NAME') if bucket_name == None else bucket_name
        assert self.bucket_name, "Please provide BUCKET NAME."

        self.storage_client = storage.Client()
        self.bucket = self.storage_client.get_bucket(self.bucket_name)

    def upload_from_filename(self, filename:str, destpath:str):
        # Upload local file to bucket
        blob = self.bucket.blob(destpath)
        blob.upload_from_filename(filename)
        logger.info(f'Uploaded {filename} to "{self.bucket}" bucket.')

    def upload_from_file(self, file_obj, despath:str):
        """
        @file_obj: file object to upload to the bucket
        @despath: path of file to be uploaded into the bucket
        """
        despath = os.path.join(despath, file_obj.filename)
        blob = self.bucket.blob(despath)
        blob.upload_from_string(file_obj.read(), content_type=file_obj.content_type)
        logger.info(f'Uploaded {despath} to "{self.bucket}" bucket.')


    def upload_all(self, local_dir:str, bucket_dir:str):
        files = [f for f in listdir(local_dir) if isfile(join(local_dir, f))]
        for file in files: # TODO recursive upload
            local_file = local_dir + file
            blob = self.bucket.blob(bucket_dir + file)
            blob.upload_from_filename(local_file)
        logger.info(f'Uploaded {files} to "{self.bucket}" bucket.')

    def list_files(self, bucket_dir:str) -> list:
        # Return lists of files in a bucket dir.
        files = self.bucket.list_blobs(prefix=bucket_dir)
        file_list = [file.name for file in files if '.' in file.name]
        return file_list

    def download(self, bucket_filename:str, local_dir:str) -> str:
        blob = self.bucket.blob(bucket_filename)
        file_name = blob.name.split('/')[-1]
        dest_file = os.path.join(local_dir, file_name)
        blob.download_to_filename(dest_file)
        logger.info(f'{file_name} downloaded from bucket.')
        return dest_file

    def delete(self, bucket_filename:str):
        self.bucket.delete_blob(bucket_filename)

    def _get_blob(self, path):
        blob = self.bucket.blob(path)
        return blob

    def get_file_as_bytestring(self, path):
        blob = self._get_blob(path)
        s = blob.download_as_string()
        return s

    def get_file_obj(self, path):
        blob = self._get_blob(path)
        byte_stream = BytesIO()
        blob.download_to_file(byte_stream)
        byte_stream.seek(0)
        return byte_stream


    def sync_down_unzip(self, source:str, destination:str):
        downloaded_file = self.download(source, destination)
        logger.info("Unzipping the zip file.")
        zip = zipfile.ZipFile(downloaded_file)
        zip.extractall(destination)
        zip.close()
        logger.info("Successfully prepared directory.")

gcp = GCP_Service()
