from src.core.storage.application.use_case.dto import SaveFileInput, SaveFileOutput

from core.storage.infra.interfaces.repository import StorageRepository


class SaveFile:
    def __init__(self, repository: StorageRepository):
        self.repository = repository

    def execute(self, input: SaveFileInput, file_name: str) -> SaveFileOutput:
        file_url = self.repository.save_file(input.file, file_name)
        return SaveFileOutput(file_url=file_url)
