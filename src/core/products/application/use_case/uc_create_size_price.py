from core.products.infra.database.django.models import SizePrice
from core.products.infra.database.repository import SizePriceRepository


class UCCreateSizePrice:
    def __init__(self, size_price_repository: SizePriceRepository):
        self.size_price_repository = size_price_repository

    async def execute(self, size_price: SizePrice) -> SizePrice:
        return await self.size_price_repository.create(size_price)
