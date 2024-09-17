import uuid

from pydantic import field_validator , BaseModel  , model_validator
from src.category.entities.exceptions import erros



class Category(BaseModel):
    id: uuid.UUID
    name: str

    def __str__(self):
        return f'Category: id={self.id}, name={self.name}'

    @model_validator(mode='before')
    @classmethod
    def check_based_info(cls,data: dict)-> dict:
        if not data.get('id'):
            raise erros.IdIsRequired
        if not isinstance(data.get('id'), uuid.UUID):
            raise erros.IdShouldBeUUID
        if not data.get('name'):
            raise erros.NameIsRequired
        if not isinstance(data.get('name'), str):
            raise erros.NameShouldBeString
        return data

    @field_validator('name')
    @classmethod
    def validate_name(cls, value: str):
        if len(value) > 150:
            raise erros.NameShouldBeLessThan150Characters
        return value
    
    

    





