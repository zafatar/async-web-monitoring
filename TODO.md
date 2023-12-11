# TO-DO list for this project

This is a TO-DO list for this project. This is just for the demonstration purposes.

## Features

- [x] Python DB API implementation (psycopg2) with PostgreSQL for links and access logs
- [x] Python custom scheduler implementation
- [x] Python web crawler based on `aiohttp`
- [x] Pydantic-based configuration

  - [x] Application configuration (db connection, etc)

- [x] List of websites to crawl in the database

  - [x] List of websites as initial database data
  - [x] Regular expression to match for each website

- [x] Dockerfile for the application
- [ ] Docker Compose

  - [x] For local development/implementation [docker-compose.yml](./docker-compose.yml)

- [x] GitHub Actions CI/CD (Simple one)
- [x] Testing with pytest and pytest-asyncio (not detailed)
- [x] Client to check the database and the results
- [x] Logging
- [x] Add Makefile in order to build, run, test, etc. the application as docker container
- [x] README as documentation

## Code quality

- [x] Linter (flake8)
  - [x] with direct command `flake8 tests src && isort tests src -c && black --check .`
  - [x] github action (not tested)
- [x] Formatter (black)
  - [x] with direct command `isort tests src && black .`
  - [x] github action (not tested)
