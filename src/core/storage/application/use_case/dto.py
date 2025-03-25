from src.core.shared.file import UploadedFile
from src.core.shared.model import Model


class SaveFileInput(Model):
    file: UploadedFile


class SaveFileOutput(Model):
    file_url: str
