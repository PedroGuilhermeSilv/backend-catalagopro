import re
import unicodedata


def remove_accents_and_convert_to_slug(text: str) -> str:
    """
    Converte um texto para slug:
    - Remove acentos
    - Converte para minúsculo
    - Remove caracteres especiais
    - Substitui espaços por hífens
    - Remove hífens duplicados
    """

    text = unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode("utf-8")

    text = text.lower()

    text = re.sub(r"[^\w\s-]", " ", text)

    text = re.sub(r"[\s_]+", "-", text)

    return text.strip("-")
