from google.genai import Client
from pydantic import BaseModel, Field
from typing import Optional

from src.core.externals.gemini.use_case.dto import InputCreateDescription


class UcCreateDescription(BaseModel):
    client: Client
    
    class Config:
        arbitrary_types_allowed = True


    def execute(self, input: InputCreateDescription) -> str:
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[f"""Faça um texto descritivo de venda com emjois e simples para venda desse produto, Nome: {
                              input.product_name}, Prreço min: {input.price_min}, Preço max: {input.price_max},
                               link de venda: {input.offer_link}. fromate o link de venda para enviar no whatsapp
      
                      """]
        )
        return response.text

