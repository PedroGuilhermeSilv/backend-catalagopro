from google.genai import Client

from src.core.externals.gemini.use_case.uc_create_description import UcCreateDescription
from src.core.externals.gemini.use_case.dto import InputCreateDescription

class GeminiService:
    def __init__(self, client: Client) -> None:
        self.uc_create_description = UcCreateDescription(client=client)

    def create_description(self,input:InputCreateDescription)-> str:
        return self.uc_create_description.execute(input)