from pydantic import BaseModel
from src.core.storage.application.use_case.dto import SaveFileInput, SaveFileOutput
from src.core.storage.domain.repository import StorageRepository


class SaveFile:
    def __init__(self, repository: StorageRepository):
        self.repository = repository

    def execute(self, input: SaveFileInput) -> SaveFileOutput:
        file_url = self.repository.save_file(input.file)
        return SaveFileOutput(file_url=file_url)
