import click
from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import DATABASE_URL
from src.orm.user import User

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@click.command()
@click.argument("email")
@click.argument("user_name")
@click.argument("first_name")
@click.argument("last_name")
@click.argument("password")
def add_initial_superuser(email, user_name, first_name, last_name, password):
    hashed_pass = pwd_context.hash(password)
    db_user = User(
        email=email,
        user_name=user_name,
        first_name=first_name,
        last_name=last_name,
        password=hashed_pass,
        is_superuser=True,
    )
    db.add(db_user)
    db.commit()
    return f"user {user_name} added"


if __name__ == "__main__":
    add_initial_superuser()
