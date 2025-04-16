from dataclasses import dataclass

from src.config import settings


@dataclass
class Connection:
    app_id = settings.APP_ID_SHOPEE
    secret = settings.SECRET_SHOPEE

    