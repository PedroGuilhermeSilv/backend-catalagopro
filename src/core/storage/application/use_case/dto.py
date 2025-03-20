from src.core.utils.file import UploadedFile
from src.core.utils.model import Model


class SaveFileInput(Model):
    file: UploadedFile


class SaveFileOutput(Model):
    file_url: str
