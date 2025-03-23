import json
import re
from ninja import File, Form, Path
from ninja.files import UploadedFile
from core.storage.infra.tebi_io.tebi_io_repository import TebiIOStorageRepository
from src.core.store.application.services.dtos import InputServiceUpdateStore
from src.core.store.application.services.store_service import StoreService
from src.core.store.domain.entity import StoreStatus
from src.core.store.infra.api.controllers.dtos import StoreUpdateDto
from src.core.store.infra.database.repository import DjangoStoreRepository
from src.core.user.infra.database.repository import DjangoUserRepository
from src.core.utils.file import UploadedFile as DomainUploadedFile
from src.core.utils.date import DayOfWeek, BusinessHour


def parse_multipart_form_data(request):
    """Extrai dados do corpo multipart/form-data."""
    form_data = {}
    content_type = request.headers.get("content-type", "")
    match = re.search(r"boundary=(.+)", content_type)

    if match and match.group(1):
        boundary = match.group(1)
        body_text = request.body.decode("utf-8", errors="replace")
        parts = body_text.split("--" + boundary)

        for part in parts:
            if "Content-Disposition: form-data;" in part:
                name_match = re.search(r'name="([^"]+)"', part)
                if name_match:
                    field_name = name_match.group(1)
                    value_parts = part.split("\r\n\r\n", 1)
                    if len(value_parts) > 1:
                        field_value = value_parts[1].split("\r\n--", 1)[0].strip()
                        form_data[field_name] = field_value

    return form_data


def extract_form_values(form_data, **defaults):
    """Extrai valores do formulário, utilizando valores default quando necessário."""
    values = {}

    # Campos de texto simples
    text_fields = ["name", "description", "address", "whatsapp", "owner_id"]
    for field in text_fields:
        values[field] = form_data.get(field, defaults.get(field) or "")

    # Campo business_hours (requer parsing JSON)
    business_hours_val = form_data.get(
        "business_hours", defaults.get("business_hours") or "[]"
    )
    try:
        values["business_hours"] = (
            json.loads(business_hours_val) if business_hours_val else []
        )
    except json.JSONDecodeError:
        values["business_hours"] = []

    # Campo status (requer conversão para enum)
    status_str = form_data.get("status")
    values["status"] = StoreStatus(status_str) if status_str else defaults.get("status")

    # Campo image (será tratado separadamente)

    return values


def create_input_data(values, store_id, image=None):
    """Cria o objeto de entrada para o serviço."""
    input_data = {
        "name": values["name"],
        "description": values["description"],
        "address": values["address"],
        "whatsapp": values["whatsapp"],
        "business_hours": values["business_hours"],
        "image": DomainUploadedFile.from_upload(image) if image else None,
        "status": values["status"],
        "store_id": store_id,
        "owner_id": values["owner_id"],
    }

    # Remover campos None para não sobrescrever valores existentes
    return {k: v for k, v in input_data.items() if v is not None}


async def update(
    request,
    id: str,
    image: UploadedFile | None = File(None),
    name: str | None = Form(None),
    description: str | None = Form(None),
    address: str | None = Form(None),
    whatsapp: str | None = Form(None),
    business_hours: str | None = Form(None),
    status: StoreStatus | None = Form(None),
    owner_id: str | None = Form(None),
):
    try:
        # Processar o corpo multipart/form-data
        form_data = parse_multipart_form_data(request)

        # Extrair valores do formulário
        defaults = {
            "name": name,
            "description": description,
            "address": address,
            "whatsapp": whatsapp,
            "business_hours": business_hours,
            "status": status,
            "owner_id": owner_id,
        }
        values = extract_form_values(form_data, **defaults)

        # Criar objeto de entrada para o serviço
        input_data = create_input_data(values, id, image)

        # Chamar o serviço
        service = StoreService(
            store_repository=DjangoStoreRepository(),
            storage_repository=TebiIOStorageRepository(),
            user_repository=DjangoUserRepository(),
        )

        response = await service.update_store(
            input=InputServiceUpdateStore(**input_data),
        )

        return 201, StoreUpdateDto(**response.model_dump())

    except Exception as e:
        # Tratamento de erros
        if hasattr(e, "status_code"):
            return e.status_code, {"message": str(e.msg)}
        return 500, {"message": str(e)}
