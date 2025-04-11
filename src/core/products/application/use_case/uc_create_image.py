from src.core.products.domain.entity import Image
from src.core.products.infra.database.repository import ImageRepository


class CreateImageUseCase:
    def __init__(self, image_repository: ImageRepository):
        self.image_repository = image_repository

    async def execute(self, image: Image, product_id: str) -> Image:
        return await self.image_repository.create(image, product_id)
