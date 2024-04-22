from typing import Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class SubmitJokeResponse(BaseModel):
    """
    Response model for dad joke submission, indicating success and providing a reference ID.
    """

    success: bool
    joke_id: Optional[str] = None
    message: str


async def submit_joke(content: str) -> SubmitJokeResponse:
    """
    Submit a new dad joke.

    Args:
        content (str): The content of the dad joke being submitted.

    Returns:
        SubmitJokeResponse: Response model for dad joke submission, indicating success and providing a reference ID.
    """
    user_id = "your-user-id-here"
    try:
        joke = await prisma.models.Joke.prisma().create(
            data={
                "content": content,
                "status": prisma.enums.JokeStatus.PENDING,
                "submittedBy": user_id,
            }
        )
        return SubmitJokeResponse(
            success=True, joke_id=joke.id, message="Joke submitted successfully."
        )
    except Exception as e:
        return SubmitJokeResponse(success=False, message="Failed to submit the joke.")
