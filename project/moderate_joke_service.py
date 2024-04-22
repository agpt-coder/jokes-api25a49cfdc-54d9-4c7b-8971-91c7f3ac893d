from enum import Enum

import prisma
import prisma.models
from pydantic import BaseModel


class JokeStatus(Enum):
    """
    An enum that describes the possible statuses for a dad joke in the moderation process.
    """

    APPROVED: str
    REJECTED: str
    PENDING: str


class ModerateJokeResponse(BaseModel):
    """
    Model for response data after moderating a dad joke, indicating the result of the moderation.
    """

    message: str
    moderated_joke_id: str
    new_status: str


async def moderate_joke(joke_id: str, new_status: JokeStatus) -> ModerateJokeResponse:
    """
    Moderate a submitted dad joke.

    Args:
    joke_id (str): The unique identifier for the dad joke being moderated.
    new_status (JokeStatus): The new moderation status of the dad joke, which can be either 'APPROVED', 'REJECTED', or 'PENDING'.

    Returns:
    ModerateJokeResponse: Model for response data after moderating a dad joke, indicating the result of the moderation.
    """
    updated_joke = await prisma.models.Joke.prisma().update(
        where={"id": joke_id}, data={"status": new_status.name}
    )
    if updated_joke:
        return ModerateJokeResponse(
            message="Dad joke has been successfully moderated.",
            moderated_joke_id=updated_joke.id,
            new_status=updated_joke.status,
        )
    else:
        return ModerateJokeResponse(
            message="Failed to moderate the dad joke.",
            moderated_joke_id=joke_id,
            new_status="FAILURE",
        )
