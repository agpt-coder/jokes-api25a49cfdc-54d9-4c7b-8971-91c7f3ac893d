import logging
from contextlib import asynccontextmanager
from typing import Optional

import project.get_random_joke_service
import project.login_user_service
import project.moderate_joke_service
import project.refresh_token_service
import project.register_user_service
import project.submit_joke_service
import project.update_profile_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="jokes-api2",
    lifespan=lifespan,
    description="Based on our conversation and the information gathered, our project will involve creating a single API endpoint using FastAPI that returns one random dad joke. Here's a summary of the steps and best practices to employ in building this API:\n\n1. **API Structure and Endpoint Design**: Create a clear and intuitive API structure with one main endpoint (e.g., /random-joke) that returns a random dad joke upon request.\n\n2. **Use of Pydantic Models**: Employ Pydantic models to validate incoming requests and serialize outgoing responses to ensure data consistency and integrity.\n\n3. **Asynchronous Request Handling**: Implement async functions to handle requests efficiently, improving scalability and performance.\n\n4. **OpenAPI Documentation**: Utilize FastAPI’s automatic OpenAPI documentation feature for easy exploration and testing of the API endpoint.\n\n5. **Security Measures**: Secure the API by integrating basic authentication or JWT tokens to control access.\n\n6. **Background Tasks and Rate Limiting**: Incorporate background tasks for any heavy processing and rate limiting to prevent abuse and ensure the API remains responsive.\n\n7. **Database Integration with PostgreSQL and Prisma ORM**: Use PostgreSQL for database needs and integrate with Prisma ORM for database operations, enabling the storage and retrieval of jokes.\n\n8. **Endpoint Testing**: Ensure thorough testing of the endpoint using FastAPI’s test client, covering various scenarios and validations.\n\n9. **Adherence to RESTful Principles**: Design the API according to RESTful principles, ensuring a resource-oriented approach and the use of appropriate HTTP methods.\n\n10. **Code Cleanliness and Documentation**: Maintain clean, well-organized code and provide adequate documentation for future maintainability.\n\nThe user expressed a preference for dad jokes, which are known for being clean, family-friendly, and simple. This project aims to craft an inclusive API experience by delivering a random dad joke, aligning with the user's preferences.",
)


@app.get(
    "/jokes/random",
    response_model=project.get_random_joke_service.GetRandomJokeResponse,
)
async def api_get_get_random_joke() -> project.get_random_joke_service.GetRandomJokeResponse | Response:
    """
    Retrieve a random dad joke.
    """
    try:
        res = await project.get_random_joke_service.get_random_joke()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/jokes/submit", response_model=project.submit_joke_service.SubmitJokeResponse
)
async def api_post_submit_joke(
    content: str,
) -> project.submit_joke_service.SubmitJokeResponse | Response:
    """
    Submit a new dad joke.
    """
    try:
        res = await project.submit_joke_service.submit_joke(content)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/jokes/moderate", response_model=project.moderate_joke_service.ModerateJokeResponse
)
async def api_put_moderate_joke(
    joke_id: str, new_status: project.moderate_joke_service.JokeStatus
) -> project.moderate_joke_service.ModerateJokeResponse | Response:
    """
    Moderate a submitted dad joke.
    """
    try:
        res = await project.moderate_joke_service.moderate_joke(joke_id, new_status)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/auth/login", response_model=project.login_user_service.LoginResponse)
async def api_post_login_user(
    email: str, password: str
) -> project.login_user_service.LoginResponse | Response:
    """
    Authenticate users and return a JWT token.
    """
    try:
        res = await project.login_user_service.login_user(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/auth/refresh", response_model=project.refresh_token_service.RefreshTokenResponse
)
async def api_post_refresh_token(
    refresh_token: str,
) -> project.refresh_token_service.RefreshTokenResponse | Response:
    """
    Refresh JWT token for authenticated users.
    """
    try:
        res = await project.refresh_token_service.refresh_token(refresh_token)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/users/register",
    response_model=project.register_user_service.UserRegistrationResponse,
)
async def api_post_register_user(
    email: str, password: str, role: project.register_user_service.Role
) -> project.register_user_service.UserRegistrationResponse | Response:
    """
    Register a new user account.
    """
    try:
        res = await project.register_user_service.register_user(email, password, role)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/users/profile",
    response_model=project.update_profile_service.UserProfileUpdateResponse,
)
async def api_put_update_profile(
    email: Optional[str],
    password: Optional[str],
    role: Optional[project.update_profile_service.Role],
) -> project.update_profile_service.UserProfileUpdateResponse | Response:
    """
    Update user profile information.
    """
    try:
        res = await project.update_profile_service.update_profile(email, password, role)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
