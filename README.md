A sample fastAPI app with sqlalchemy, alembic (for migrations) and JWT auth.

Install requirements for prod:
`pip install -r requirements.txt`

for dev add to the revious:
`pip install -r requirements-dev.txt`

To run tests:
`pytest ./src`

For management scripts and migrations add this folder to python path:
`export PYTHONPATH=.`

To run migrations:
`alembic upgrade head`
To autogenerate migration files:
`alembic revision --autogenerate -m "init"`

To add superuser to db use management script:
`python src/management_scripts/db_management.py ddv@da.com dav dav dav dav`

To run uvicorn server with the application:
`python ./src/main.py`
