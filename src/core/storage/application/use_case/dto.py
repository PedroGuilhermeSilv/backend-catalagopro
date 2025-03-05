from pydantic import BaseModel
from typing import Any
from src.core.utils.file import UploadedFile


class SaveFileInput(BaseModel):
    file: UploadedFile

    model_config = {"arbitrary_types_allowed": True}


class SaveFileOutput(BaseModel):
    file_url: str
