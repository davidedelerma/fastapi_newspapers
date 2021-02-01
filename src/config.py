import os

DATABASE_URL = os.getenv("DB_URL", "sqlite:///./sql_app.db")
