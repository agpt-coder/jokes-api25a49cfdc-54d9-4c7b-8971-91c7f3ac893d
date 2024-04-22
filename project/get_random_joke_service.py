from random import choice

import prisma
import prisma.models
from pydantic import BaseModel


class GetRandomJokeResponse(BaseModel):
    """
    This response model houses the random dad joke fetched from the database, providing a simple joke structure to the caller.
    """

    id: str
    content: str
    status: str


async def get_random_joke() -> GetRandomJokeResponse:
    """
    Retrieve a random dad joke from the database.

    Args:

    Returns:
        GetRandomJokeResponse: This response model houses the random dad joke fetched from the database, providing a simple joke structure to the caller.
    """
    approved_jokes: list[
        prisma.models.Joke
    ] = await prisma.models.Joke.prisma().find_many(where={"status": "APPROVED"})
    if not approved_jokes:
        return GetRandomJokeResponse(
            id="fallback",
            content="Sorry, no jokes available right now.",
            status="APPROVED",
        )
    random_joke: prisma.models.Joke = choice(approved_jokes)
    response: GetRandomJokeResponse = GetRandomJokeResponse(
        id=random_joke.id, content=random_joke.content, status=random_joke.status
    )
    return response
