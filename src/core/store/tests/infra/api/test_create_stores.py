import io
import json
import os

import pytest
import pytest_asyncio
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, override_settings
from django.test.client import BOUNDARY, encode_multipart
from ninja.testing import TestAsyncClient
from PIL import Image
from src.core.store.domain.enums import DayOfWeek
from src.core.user.domain.entity import User
from src.core.user.infra.database.repository import DjangoUserRepository
from src.framework.urls import api

os.environ["NINJA_SKIP_REGISTRY"] = "yes"

STATUS_CODE_201 = 201
STATUS_CODE_401 = 401


@pytest_asyncio.fixture
async def create_user(client, debug_settings):
    # Criação do usuário
    user = await DjangoUserRepository().save(
        User(
            email="teste@teste.com",
            password="12345678",
            name="Teste",
            role="ADMIN",
            status="ACTIVE",
        ),
    )

    yield user


@pytest.fixture
def client():
    return TestAsyncClient(api)


@pytest.fixture
def debug_settings():
    with override_settings(DEBUG=True):
        yield


@pytest.mark.django_db(transaction=True)
class TestControllerCreateStores:
    @pytest.mark.django_db
    def test_create_store_sync(self, debug_settings, create_user: User):
        # Criar um cliente de teste síncrono
        client = Client()

        url = "/api/store/"

        image = Image.new("RGB", (100, 100), color="red")
        image_io = io.BytesIO()
        image.save(image_io, "PNG")
        image_io.seek(0)
        image_bytes = image_io.getvalue()

        test_file = SimpleUploadedFile(
            name="image.png",
            content=image_bytes,
            content_type="image/png",
        )
        test_file.seek(0)

        # Preparar os dados do business_hours como JSON string
        business_hours_json = json.dumps(
            [
                {
                    "day": DayOfWeek.MONDAY.value,
                    "open_hour": "09:00",
                    "close_hour": "18:00",
                },
            ],
        )

        # Preparar os dados para o request
        data = {
            "name": "Teste",
            "email_owner": create_user.email,
            "description": "Teste",
            "address": "Rua Teste",
            "whatsapp": "1234567890",
            "business_hours": business_hours_json,
            "status": "ACTIVE",
            "image": test_file,
        }

        content = encode_multipart(BOUNDARY, data)
        content_type = f"multipart/form-data; boundary={BOUNDARY}"

        response = client.post(
            url,
            data=content,
            content_type=content_type,
            HTTP_AUTHORIZATION="Bearer 1234567890",
        )

        assert response.status_code == STATUS_CODE_201

        response_json = response.json()
        assert response_json["name"] == "Teste"
        assert response_json["description"] == "Teste"
        assert response_json["address"] == "Rua Teste"
        assert response_json["whatsapp"] == "1234567890"
        assert response_json["owner_id"] == str(create_user.id)
