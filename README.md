# Movie DB
#### This application allows you to search and store movie data. If there's no movie in DB it will look for it in OMDB API and save it for later.

## Requirements
- [Docker](https://docs.docker.com/v17.12/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Setup

1. Clone the repository
2. Navigate into project's directory
3. `cp .env-example .env` and paste OMDB API key into `.env` file
4. `docker-compose build`
5. `docker-compose up`

To run tests:
`docker-compose run django bash -c "cd src; python manage.py test"`

When updating requirements:
1. Add package in requirements.in file (remember to pin version)
2. Run `pip-compile --output-file requirements.txt requirements.in`

### You can find list of all endpoints in documentation at `/docs/`
