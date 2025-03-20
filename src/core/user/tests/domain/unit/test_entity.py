import pytest

from core.user.domain.entity import UserRole
from core.utils.enums import Status
from src.core.user.domain.entity import User
from src.core.user.domain.exceptions import (
    InvalidUserError,
)
from src.core.utils.hash import verify_password


class TestUnitClassUser:
    def test_user_instance(self):
        password_ = "12345678"  # noqa
        user = User(
            email="test@hotmail.com",
            password=password_,
            name="test",
            role=UserRole.ADMIN.value,
            status=Status.ACTIVE.value,
        )
        assert user.email == "test@hotmail.com"
        assert user.password != password_

    def test_user_instance_with_id(self):
        user = User(
            email="test@hotmail.com",
            password="12345678",
            name="test",
            role=UserRole.ADMIN.value,
            status=Status.ACTIVE.value,
        )
        assert user.id is not None

    def test_raise_exception_when_no_email(self):
        with pytest.raises(InvalidUserError) as excinfo:
            User(
                email="",
                password="12345678",
                name="test",
                role=UserRole.ADMIN.value,
                status=Status.ACTIVE.value,
            )
        assert str(excinfo.value) == "Invalid user"

    def test_raise_exception_when_password_less_than_8(self):
        with pytest.raises(Exception) as excinfo:
            User(email="test@hotmail.com", password="123456")
        assert str(excinfo.value) == "Password must be at least 8 characters long"

    def test_raise_exception_when_invalid_email(self):
        with pytest.raises(Exception) as excinfo:
            User(email="test", password="12345678")
        assert str(excinfo.value) == "Invalid email"

    def test_hash_password(self):
        user1 = User(
            email="test@hotmail.com",
            password="12345678",
            name="test",
            role=UserRole.ADMIN.value,
            status=Status.ACTIVE.value,
        )
        user2 = User(
            email="test@hotmail.com",
            password="12345678",
            name="test",
            role=UserRole.ADMIN.value,
            status=Status.ACTIVE.value,
        )
        assert user1.password != user2.password
        assert verify_password("12345678", user1.password)
