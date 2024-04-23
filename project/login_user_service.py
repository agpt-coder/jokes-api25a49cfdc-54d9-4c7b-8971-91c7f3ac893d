import prisma
import prisma.models
from fastapi import HTTPException, status
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel


class LoginResponse(BaseModel):
    """
    Response model for a successful login operation, returning a JWT token.
    """

    jwt_token: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

ALGORITHM = "HS256"


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.

    Args:
        plain_password (str): Plaintext password to verify.
        hashed_password (str): Hashed password for comparison.

    Returns:
        bool: True if passwords match, false otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(email: str, password: str) -> prisma.models.User | None:
    """
    Authenticate user by checking if user exists and password is correct.

    Args:
        email (str): The user's email address.
        password (str): The user's password.

    Returns:
        prisma.models.User | None: The authenticated user or None if authentication failed.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    if not user:
        return None
    if not await verify_password(password, user.password):
        return None
    return user


async def create_access_token(data: dict) -> str:
    """
    Create a JWT access token.

    Args:
        data (dict): The payload data to encode in the token.

    Returns:
        str: The encoded JWT token
    """
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def login_user(email: str, password: str) -> LoginResponse:
    """
    Authenticate users and return a JWT token.

    Args:
      email (str): The email address associated with the user's account.
      password (str): The password for the user's account.

    Returns:
      LoginResponse: Response model for a successful login operation, returning a JWT token.
    """
    user = await authenticate_user(email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = await create_access_token(data={"sub": user.email})
    return LoginResponse(jwt_token=access_token)
