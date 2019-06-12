# Requirements
- [Docker](https://docs.docker.com/v17.12/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)


# Setup

1. Clone the repository
2. Navigate into project's directory
3. `cp .env-example .env` and paste API key into that file
4. `docker-compose build`
5. `docker-compose up`

To run tests:
`docker-compose run django bash -c "cd src; python manage.py test"`

