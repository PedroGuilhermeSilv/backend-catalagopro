import pytest

from src.core.security.application.service.auth_jwt import JWTCreator
from src.core.security.application.service.dto.jwt import InputAuthUserDto
from src.core.user.domain.dto import UserInput
from src.core.user.domain.entity import User
from src.core.user.infra.in_memory.in_memory_user import InMemoryUserRepository
from src.core.utils.jwt_utils import decode_jwt

EXP = 60


class TestCreateJWT:
    @pytest.mark.asyncio
    async def test_create_jwt(self):
        repository = InMemoryUserRepository()
        user = User(
            email="test@hotmail.com",
            password="12345678",
        )

        user_input = UserInput(
            id=user.id,
            email=user.email,
            password=user.password,
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
