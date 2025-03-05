from django.db import models
from uuid import uuid4
from src.core.user.infra.database.models import User


class Store(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, unique=True)
    logo_url = models.URLField()
    description = models.TextField()
    address = models.TextField()
    whatsapp = models.CharField(max_length=255)
    business_hours = models.JSONField()

    def __str__(self):
        return self.name
