import os
from abc import abstractmethod
from typing import Any

from src.core.utils.model import Model


class StorageRepository(Model):
    service_name: str = os.environ.get("SERVICE_NAME", "s3")
    endpoint_url: str = os.environ.get("ENDPOINT_URL")
    aws_access_key_id: str = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str = os.environ.get("AWS_SECRET_ACCESS_KEY")
    bucket_name: str = os.environ.get("BUCKET_NAME")

    def connection(self):
        raise NotImplementedError

    @abstractmethod
    def save_file(self, file: Any, file_name: str) -> str:
        raise NotImplementedError

    def update_file(self, file: Any, file_name: str) -> str:
        raise NotImplementedError
