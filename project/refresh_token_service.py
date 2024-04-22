from datetime import datetime, timedelta

from jose import JWTError, jwt
from pydantic import BaseModel


class RefreshTokenResponse(BaseModel):
    """
    Response model for successfully refreshing a user's authentication token. Contains a new JWT for the user.
    """

    access_token: str
    token_type: str
    expires_in: int


SECRET_KEY = "your_secret_key_here"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


async def refresh_token(refresh_token: str) -> RefreshTokenResponse:
    """
    Refresh JWT token for authenticated users.

    Args:
        refresh_token (str): The valid refresh token provided by the user to obtain a new JWT.

    Returns:
        RefreshTokenResponse: Response model for successfully refreshing a user's authentication token. Contains a new JWT for the user.
    """
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if "sub" not in payload:
            raise Exception("Subject (sub) not found in the token payload.")
        user_id = payload.get("sub")
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        new_access_token = jwt.encode(
            {"sub": user_id, "exp": datetime.utcnow() + access_token_expires},
            SECRET_KEY,
            algorithm=ALGORITHM,
        )
        return RefreshTokenResponse(
            access_token=new_access_token,
            token_type="Bearer",
            expires_in=int(access_token_expires.total_seconds()),
        )
    except JWTError:
        raise Exception("Invalid refresh token.")
