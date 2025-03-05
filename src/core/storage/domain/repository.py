from abc import abstractmethod
from pydantic import BaseModel
import os
from typing import Any


class StorageRepository(BaseModel):
    service_name: str = os.environ.get("SERVICE_NAME", "s3")
    endpoint_url: str = os.environ.get("ENDPOINT_URL")
    aws_access_key_id: str = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str = os.environ.get("AWS_SECRET_ACCESS_KEY")
    bucket_name: str = os.environ.get("BUCKET_NAME")

    def connection(self):
        raise NotImplementedError

    @abstractmethod
    def save_file(self, file: Any) -> str:
        raise NotImplementedError

    model_config = {"arbitrary_types_allowed": True}
