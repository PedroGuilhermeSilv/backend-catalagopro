import os
import warnings

import boto3
import urllib3
from botocore.config import Config
from src.core.utils.file import UploadedFile

from core.storage.infra.interfaces.repository import StorageRepository


class TebiIOStorageRepository(StorageRepository):
    def __init__(self):
        super().__init__(
            service_name=os.environ.get("SERVICE_NAME", "s3"),
            endpoint_url=os.environ.get("ENDPOINT_URL", "https://s3.tebi.io"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", ""),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", ""),
            bucket_name=os.environ.get("BUCKET_NAME", "ifood-crm"),
        )

    def connection(self):
        return boto3.client(
            "s3",
            endpoint_url=self.endpoint_url.replace("https://", "http://"),
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            config=Config(s3={"addressing_style": "path"}, signature_version="s3v4"),
            use_ssl=False,
            region_name="us-east-1",
        )

    def save_file(self, file: UploadedFile, file_name: str) -> str:

        warnings.filterwarnings(
            "ignore",
            category=urllib3.exceptions.InsecureRequestWarning,
        )

        self.connection().put_object(
            Bucket=self.bucket_name,
            Key=file_name,
            Body=file.content,
            ContentType=file.content_type,
            ACL="public-read",
        )

        return f"{self.endpoint_url}/{self.bucket_name}/{file_name}"

    def delete_file(self, file_name: str) -> None:
        self.connection().delete_object(Bucket=self.bucket_name, Key=file_name)

    def update_file(self, file: UploadedFile, file_name: str) -> str:
        self.delete_file(file_name)
        return self.save_file(file, file_name)
