from datetime import datetime
from enum import Enum
from typing import Optional

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


class User(BaseModel):
    """
    The User model reflecting the current state of the user's profile in the database.
    """

    id: str
    email: str
    role: Role
    createdAt: datetime
    updatedAt: datetime


class UserProfileUpdateResponse(BaseModel):
    """
    The response object reflecting the result of the user profile update operation. It includes the updated profile information.
    """

    success: bool
    message: str
    updated_profile: Optional[User] = None


async def update_profile(
    email: Optional[str], password: Optional[str], role: Optional[Role]
) -> UserProfileUpdateResponse:
    """
    Update user profile information.

    Args:
        email (Optional[str]): The new email address for the user. Optional.
        password (Optional[str]): The user's new password. Optional.
        role (Optional[Role]): The new role for the user. Must be one of the predefined roles. Optional.

    Returns:
        UserProfileUpdateResponse: The response object reflecting the result of the user profile update operation. It includes the updated profile information.
    """
    try:
        update_data = {}
        if email is not None:
            update_data["email"] = email
        if password is not None:
            update_data["password"] = password
        if role is not None:
            update_data["role"] = role.value
        user_id = "obtained_user_id"
        updated_user = await prisma.models.User.prisma().update(
            where={"id": user_id}, data=update_data
        )
        if updated_user:
            return UserProfileUpdateResponse(
                success=True,
                message="User profile updated successfully.",
                updated_profile=updated_user,
            )
        else:
            return UserProfileUpdateResponse(
                success=False, message="User profile update failed."
            )
    except Exception as e:
        return UserProfileUpdateResponse(
            success=False, message=f"An error occurred during profile update: {str(e)}"
        )
