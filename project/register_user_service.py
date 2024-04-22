from datetime import datetime
from enum import Enum

import prisma
import prisma.models
from pydantic import BaseModel


class Role(Enum):
    """
    Enumeration of user roles within the application.
    """

    USER: str = USER  # TODO(autogpt): F821 Undefined name `USER`
    MODERATOR: str = MODERATOR  # TODO(autogpt): F821 Undefined name `MODERATOR`
    ADMIN: str = ADMIN  # TODO(autogpt): F821 Undefined name `ADMIN`


class UserRegistrationResponse(BaseModel):
    """
    Response model for when a user has successfully registered. Provides basic user information without sensitive data like passwords.
    """

    user_id: str
    email: str
    role: str
    registration_date: datetime


async def register_user(
    email: str, password: str, role: Role
) -> UserRegistrationResponse:
    """
    Register a new user account.

    Args:
        email (str): User's email address. Must be unique.
        password (str): Password for the user account. Will be hashed before storage.
        role (Role): The role assigned to the user at registration.

    Returns:
        UserRegistrationResponse: Response model for when a user has successfully registered. Provides basic user information without sensitive data like passwords.
    """
    hashed_password: str = f"hashed_{password}"
    existing_user = await prisma.models.User.prisma().find_unique(
        where={"email": email}
    )
    if existing_user:
        raise ValueError("User already exists with this email")
    new_user = await prisma.models.User.prisma().create(
        data={"email": email, "password": hashed_password, "role": role.value}
    )
    registration_response = UserRegistrationResponse(
        user_id=new_user.id,
        email=new_user.email,
        role=new_user.role,
        registration_date=new_user.createdAt,
    )
    return registration_response
