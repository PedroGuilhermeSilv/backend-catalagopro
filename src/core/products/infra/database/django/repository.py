from asgiref.sync import sync_to_async
from django.db import transaction

from src.core.products.domain.entity import (
    Category,
    Image,
    Price,
    Product,
    Size,
    SizePrice,
)
from src.core.products.infra.database.django.models import (
    Category as CategoryModel,
)
from src.core.products.infra.database.django.models import (
    Image as ImageModel,
)
from src.core.products.infra.database.django.models import (
    Price as PriceModel,
)
from src.core.products.infra.database.django.models import (
    Product as ProductModel,
)
from src.core.products.infra.database.django.models import (
    Size as SizeModel,
)
from src.core.products.infra.database.django.models import (
    SizePrice as SizePriceModel,
)
from src.core.products.infra.database.django.models import (
    Store as StoreModel,
)
from src.core.products.infra.database.repository import (
    CategoryRepository,
    ImageRepository,
    ProductRepository,
    SizePriceRepository,
    SizeRepository,
)


class DjangoCategoryRepository(CategoryRepository):
    def __init__(self):
        self.model = CategoryModel

    async def create(self, category: Category) -> Category:
        store = await StoreModel.objects.aget(id=category.store_id)
        category_model = await self.model.objects.acreate(
            name=category.name,
            store=store,
        )
        return Category(
            id=str(category_model.id),
            name=category_model.name,
            store_id=str(category_model.store_id),
        )

    async def get_by_id(self, id: str) -> Category:
        category_model = await self.model.objects.aget(id=id)
        return Category(
            id=str(category_model.id),
            name=category_model.name,
            store_id=str(category_model.store_id),
        )

    async def list(self, store_id: str) -> list[Category]:
        get_categories = sync_to_async(
            lambda: list(self.model.objects.filter(store_id=store_id)),
        )
        categories = await get_categories()
        return [
            Category(
                id=str(category.id),
                name=category.name,
                store_id=str(category.store_id),
            )
            for category in categories
        ]


class DjangoSizeRepository(SizeRepository):
    def __init__(self):
        self.model = SizeModel

    def convert_to_domain(self, size_model: SizeModel) -> Size:
        return Size(
            id=str(size_model.id),
            name=size_model.name,
            store_id=str(size_model.store_id),
        )

    async def create(self, size: Size) -> Size:
        store = await StoreModel.objects.aget(id=size.store_id)
        size_model = await self.model.objects.acreate(
            name=size.name,
            store=store,
        )
        return Size(
            id=str(size_model.id),
            name=size_model.name,
            store_id=str(size_model.store_id),
        )

    async def list(self, store_id: str) -> list[Size]:
        get_sizes = sync_to_async(
            lambda: list(self.model.objects.filter(store_id=store_id)),
        )
        sizes = await get_sizes()
        return [
            Size(id=str(size.id), name=size.name, store_id=str(size.store_id))
            for size in sizes
        ]

    async def get_by_id(self, id: str) -> Size:
        size_model = await self.model.objects.aget(id=id)
        return self.convert_to_domain(size_model)


class DjangoProductRepository(ProductRepository):
    def __init__(self):
        self.product_model = ProductModel
        self.image_model = ImageModel
        self.category_model = CategoryModel
        self.size_model = SizeModel
        self.price_model = PriceModel
        self.size_price_model = SizePriceModel

    async def convert_to_domain_async(self, product_model: ProductModel) -> Product:
        @sync_to_async
        def get_domain_model():
            category = Category(
                id=str(product_model.category.id),
                name=product_model.category.name,
                store_id=str(product_model.category.store_id),
            )

            default_price = None
            if product_model.default_price:
                default_price = Price(
                    id=str(product_model.default_price.id),
                    value=product_model.default_price.value,
                )

            size_prices = []
            for size_price in product_model.size_price.all():
                size = Size(
                    id=str(size_price.size.id),
                    name=size_price.size.name,
                    store_id=str(size_price.size.store_id),
                )
                price = Price(
                    id=str(size_price.price.id),
                    value=size_price.price.value,
                )
                size_prices.append(SizePrice(size=size, price=price))

            # Buscar imagens filtrando pelo produto
            images = [
                Image(id=str(img.id), url=img.url)
                for img in ImageModel.objects.filter(product=product_model)
            ]

            return Product(
                id=str(product_model.id),
                name=product_model.name,
                description=product_model.description,
                category=category,
                default_price=default_price,
                size_price=size_prices if size_prices else None,
                image=images,
                store_id=str(product_model.store_id),
                created_at=product_model.created_at,
                updated_at=product_model.updated_at,
            )

        return await get_domain_model()

    async def create(self, product: Product) -> Product:
        @sync_to_async
        def create_product_sync():
            with transaction.atomic():
                # Verifica se a categoria existe, senão cria
                try:
                    category_model = self.category_model.objects.get(
                        id=str(product.category.id),
                    )
                except self.category_model.DoesNotExist:
                    # Cria a categoria se não existir
                    store_model = StoreModel.objects.get(id=str(product.store_id))
                    category_model = self.category_model.objects.create(
                        id=str(product.category.id),
                        name=product.category.name,
                        store=store_model,
                    )

                # Continua com a criação do produto
                store_model = StoreModel.objects.get(id=str(product.store_id))
                product_model = self.product_model.objects.create(
                    name=product.name,
                    description=product.description,
                    category=category_model,
                    store=store_model,
                )
                # adiciona as images
                for image in product.image:
                    ImageModel.objects.create(
                        id=str(image.id),
                        url=image.url,
                        product=product_model,
                    )
                if product.default_price:
                    price_model = self.price_model.objects.create(
                        value=product.default_price.value,
                    )
                    product_model.default_price = price_model
                    product_model.save()
                else:
                    for size_price in product.size_price:
                        size_model = self.size_model.objects.get(id=size_price.size.id)
                        price_model = self.price_model.objects.create(
                            value=size_price.price.value,
                        )
                        size_price_model = self.size_price_model.objects.create(
                            size=size_model,
                            price=price_model,
                        )
                        product_model.size_price.add(size_price_model)
                        product_model.save()
                return product_model

        product_model = await create_product_sync()
        return await self.convert_to_domain_async(product_model)


class DjangoSizePriceRepository(SizePriceRepository):
    def __init__(self):
        self.size_model = SizeModel
        self.price_model = PriceModel
        self.size_price = SizePriceModel

    def convert_to_domain(self, size_price_model: SizePriceModel) -> SizePrice:
        """Converte um modelo SizePrice para a entidade de domínio"""
        size = Size(
            id=str(size_price_model.size.id),
            name=size_price_model.size.name,
            store_id=str(size_price_model.size.store_id),
        )

        price = Price(
            id=str(size_price_model.price.id),
            value=size_price_model.price.value,
        )

        return SizePrice(
            id=str(size_price_model.id),
            size=size,
            price=price,
        )

    async def convert_to_domain_async(
        self,
        size_price_model: SizePriceModel,
    ) -> SizePrice:
        """Versão assíncrona para converter um modelo SizePrice para a entidade de domínio"""

        @sync_to_async
        def get_domain_model():
            return self.convert_to_domain(size_price_model)

        return await get_domain_model()

    async def create(self, size_price: SizePrice) -> SizePrice:
        size_model = await self.size_model.objects.aget(id=size_price.size.id)
        price_model = await self.price_model.objects.acreate(
            id=size_price.price.id,
            value=size_price.price.value,
        )
        size_price_model = await self.size_price.objects.acreate(
            id=size_price.id,
            size=size_model,
            price=price_model,
        )
        return await self.convert_to_domain_async(size_price_model)


class DjangoImageRepository(ImageRepository):
    def __init__(self):
        self.model = ImageModel
        self.product_model = ProductModel

    async def create(self, image: Image, product_id: str) -> Image:
        product_model = await self.product_model.objects.aget(id=product_id)
        image_model = await self.model.objects.acreate(
            id=image.id,
            url=image.url,
            product=product_model,
        )
        return Image(
            id=str(image_model.id),
            url=image_model.url,
        )
