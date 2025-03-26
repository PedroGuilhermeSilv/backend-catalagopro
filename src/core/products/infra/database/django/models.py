import uuid

from django.db import models

from src.core.store.infra.database.django.models import Store


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)


class Size(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)


class Price(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    value = models.DecimalField(max_digits=10, decimal_places=2)


class SizePrice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.ForeignKey(Price, on_delete=models.CASCADE)


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    default_price = models.ForeignKey(
        Price,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    size_price = models.ManyToManyField(SizePrice, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
