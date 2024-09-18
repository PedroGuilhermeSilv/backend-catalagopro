import uuid

import pytest
from src.core.user.domain.dto.user_dto import UserInput
from src.core.user.infra.in_memory_user import InMemoryUserRepository
from src.core.utils.security.application.dto.jwt import InputAuthUserDto
from src.core.utils.security.application.service.auth_jwt import JWTCreator
from src.core.utils.security.jwt import decode_jwt

EXP = 60


class TestCreateJWT:
    @pytest.mark.asyncio
    async def test_create_jwt(self):
        repository = InMemoryUserRepository()
        user_input = UserInput(
            id=uuid.uuid4(),
            email="test@hotmail.com",
            password="12345678",
        )
        await repository.save(user_input)

        request = InputAuthUserDto(email="test@hotmail.com", password="12345678")
        service = JWTCreator(repository)
        response = await service.execute(input=request)

        assert response.token is not None
        assert response.exp == EXP
        decode = decode_jwt(response.token)
        assert decode["email"] == "test@hotmail.com"
        assert decode["exp"] == EXP
