import io
import json
import os
import uuid

import pytest
import pytest_asyncio
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, override_settings
from django.test.client import BOUNDARY, encode_multipart
from ninja.testing import TestAsyncClient
from PIL import Image, ImageDraw
from src.core.store.application.use_case.create_store import CreateStoreUseCase
from src.core.store.domain.entity import Store
from src.core.store.domain.enums import BusinessHour, DayOfWeek
from src.core.store.infra.django.repository import DjangoStoreRepository
from src.core.user.domain.entity import User
from src.core.user.infra.database.repository import DjangoUserRepository
from src.framework.urls import api

os.environ["NINJA_SKIP_REGISTRY"] = "yes"

STATUS_CODE_200 = 200
STATUS_CODE_401 = 401
STATUS_CODE_201 = 201


@pytest_asyncio.fixture
async def create_store(client, debug_settings):
    # Criação do usuário com email único
    unique_email = f"teste_{uuid.uuid4().hex[:8]}@teste.com"

    user = await DjangoUserRepository().save(
        User(
            email=unique_email,
            password="12345678",
            name="Teste",
            role="ADMIN",
            status="ACTIVE",
        ),
    )

    # Criação da loja
    use_case = CreateStoreUseCase(DjangoStoreRepository())
    store = await use_case.execute(
        Store(
            name="Teste",
            slug="teste",
            owner_id=str(user.id),
            status="ACTIVE",
            address="Rua Teste",
            logo_url="https://www.google.com",
            description="Teste",
            whatsapp="1234567890",
            business_hours=[
                BusinessHour(
                    day=DayOfWeek.MONDAY,
                    open_hour="09:00",
                    close_hour="18:00",
                ),
            ],
        ),
    )

    yield store


@pytest.fixture
def client():
    return TestAsyncClient(api)


@pytest.fixture
def debug_settings():
    with override_settings(DEBUG=True):
        yield


@pytest.mark.django_db(transaction=True)
class TestControllerUpdateStore:
    @pytest.mark.django_db
    def test_update_store_sync(self, debug_settings, create_store):
        client = Client()

        store_id = str(create_store.id)
        url = f"/api/store/{store_id}"

        image = Image.new("RGB", (200, 200), color="blue")
        draw = ImageDraw.Draw(image)
        draw.rectangle([(50, 50), (150, 150)], fill="yellow")

        image_io = io.BytesIO()
        image.save(image_io, "PNG")
        image_io.seek(0)
        image_bytes = image_io.getvalue()

        test_file = SimpleUploadedFile(
            name="new_image.png",
            content=image_bytes,
            content_type="image/png",
        )
        test_file.seek(0)

        business_hours_json = json.dumps(
            [
                {
                    "day": DayOfWeek.MONDAY.value,
                    "open_hour": "08:00",  # Horário atualizado
                    "close_hour": "20:00",  # Horário atualizado
                },
                {
                    "day": DayOfWeek.TUESDAY.value,  # Novo dia
                    "open_hour": "09:00",
                    "close_hour": "18:00",
                },
            ],
        )

        data = {
            "name": "Loja Atualizada",
            "description": "Descrição atualizada",
            "business_hours": business_hours_json,
            "image": test_file,
        }

        content = encode_multipart(BOUNDARY, data)
        content_type = f"multipart/form-data; boundary={BOUNDARY}"

        response = client.patch(
            url,
            data=content,
            content_type=content_type,
            HTTP_AUTHORIZATION="Bearer 1234567890",
        )

        assert response.status_code == STATUS_CODE_201

        response_json = response.json()

        assert response_json["name"] == "Loja Atualizada"
        assert response_json["description"] == "Descrição atualizada"

        assert response_json["slug"] == create_store.slug
        assert response_json["address"] == create_store.address
        assert response_json["whatsapp"] == create_store.whatsapp
        assert response_json["status"] == create_store.status.value
        assert response_json["owner_id"] == str(create_store.owner_id)

        assert "logo_url" in response_json
        assert response_json["logo_url"] is not None
