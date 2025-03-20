from src.core.utils.file import UploadedFile

from core.storage.infra.interfaces.repository import StorageRepository


class InMemoryStorageRepository(StorageRepository):
    def connection(self):
        return None

    def save_file(self, file: UploadedFile, file_name: str) -> str:
        return f"https://{file_name}"
