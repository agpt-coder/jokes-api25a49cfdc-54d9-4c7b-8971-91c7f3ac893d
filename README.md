---
date: 2024-04-22T17:29:15.463783
author: AutoGPT <info@agpt.co>
---

# jokes-api2

Based on our conversation and the information gathered, our project will involve creating a single API endpoint using FastAPI that returns one random dad joke. Here's a summary of the steps and best practices to employ in building this API:

1. **API Structure and Endpoint Design**: Create a clear and intuitive API structure with one main endpoint (e.g., /random-joke) that returns a random dad joke upon request.

2. **Use of Pydantic Models**: Employ Pydantic models to validate incoming requests and serialize outgoing responses to ensure data consistency and integrity.

3. **Asynchronous Request Handling**: Implement async functions to handle requests efficiently, improving scalability and performance.

4. **OpenAPI Documentation**: Utilize FastAPI’s automatic OpenAPI documentation feature for easy exploration and testing of the API endpoint.

5. **Security Measures**: Secure the API by integrating basic authentication or JWT tokens to control access.

6. **Background Tasks and Rate Limiting**: Incorporate background tasks for any heavy processing and rate limiting to prevent abuse and ensure the API remains responsive.

7. **Database Integration with PostgreSQL and Prisma ORM**: Use PostgreSQL for database needs and integrate with Prisma ORM for database operations, enabling the storage and retrieval of jokes.

8. **Endpoint Testing**: Ensure thorough testing of the endpoint using FastAPI’s test client, covering various scenarios and validations.

9. **Adherence to RESTful Principles**: Design the API according to RESTful principles, ensuring a resource-oriented approach and the use of appropriate HTTP methods.

10. **Code Cleanliness and Documentation**: Maintain clean, well-organized code and provide adequate documentation for future maintainability.

The user expressed a preference for dad jokes, which are known for being clean, family-friendly, and simple. This project aims to craft an inclusive API experience by delivering a random dad joke, aligning with the user's preferences.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'jokes-api2'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
