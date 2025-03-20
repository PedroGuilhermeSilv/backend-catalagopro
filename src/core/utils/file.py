from typing import Any

from src.core.utils.model import Model


class UploadedFile(Model):
    name: str
    content: bytes
    content_type: str

    @classmethod
    def from_upload(cls, uploaded_file: Any) -> "UploadedFile":
        """
        Cria um UploadedFile a partir de um arquivo enviado via Django Ninja
        """
        # Lê o conteúdo do arquivo através do atributo file
        content = uploaded_file.file.read()
        # Retorna o ponteiro do arquivo para o início
        uploaded_file.file.seek(0)

        return cls(
            name=uploaded_file.name,
            content=content,
            content_type=uploaded_file.content_type,
        )
