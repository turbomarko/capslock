# Project Overview

This project consists of multiple services that are designed to be deployed as separate repositories. The current setup focuses on the development environment configuration (I use different config, Dockerfiles, requirements in production).

Since I was focusing more on the architecture and patterns, I did not have time to complete everything I wanted to, I'll list here the missing pieces:
- The mailing service hasn't been tested
- I did not include authentication / authorization
- I did not implement any tests
- Only the development environment is built, no production setup
- There might still be some burnt it constants (urls, usernames) in the code, I did not have the time to move everything to env files
- Optimization (caching, database indexes etc.)

## Architecture Notes

- The services are designed to be deployed as separate repositories for better maintainability and scalability, but here they are run by 1 docker-compose command
- There are 4 services:
    - analytics:
        - http://localhost:8000/api-docs
        - implemented with Django and DRF (built on top of [turbo-drf](https://github.com/turbomarko/turbo-drf), my open-source template application, rather than being built from scratch)
        - contains the database to store the raw data and the analysis results (as well as the task scheduling)
        - defines the endpoints to fetch the list and the details of the results
        - contains the scheduled analysis as a celery task (it has access to the database, but runs in the background, so it does not slow down data fetching). The task itself is a dummy task that does some calculations on a randomly generated dataset
    - llm:
        - http://localhost:8002/docs
        - simple FastAPI service
        - defines an endpoint through which the LLM of choice can be called (it is exposed for testing)
        - implemented as a separate service so that other services can call it (assuming that it's a part of a bigger system)
    - notifications:
        - http://localhost:8001/docs
        - simple FastAPI service
        - uses RabbitMQ for async communication (observer)
        - uses mailpit in development to see the emails
    - frontend:
        - http://localhost:3000/
        - Next.js with typescript
        - Redux and RTK toolkit for state management and data fetching
        - main logic in app folder, separate components folder for reusable components, redux folder for RTK related logic


## Setup instructions

- Set the OPENROUTER_API_KEY variable to a valid key in `llm/.envs/.local/.llm`
- Run `./cmd local setup`, this will build the containers, mmigrate the database, generate the sample data and run the containers
