from dataclasses import dataclass
import uuid

@dataclass
class Category:
    id: uuid.UUID
    name: str

    def validate(self)->None:
        if not self.name:
            raise ValueError("Name is required")
        if len(self.name) > 100:
            raise ValueError("Name should be less than 100 characters")
        if not isinstance(self.name, str):
            raise ValueError("Name should be a string")
        if not self.id:
            raise ValueError("Id is required")
        if not isinstance(self.id, uuid.UUID):
            raise ValueError("Id should be a UUID")
        
    def __post_init__(self):
        self.validate()