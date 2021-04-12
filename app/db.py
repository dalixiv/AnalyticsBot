from typing import Optional
from pydantic import BaseModel
from sqlalchemy import create_engine, text

from app.config import ctx


def get_pg_url() -> str:
    # heroku stuff
    pg_url = ctx.pg_url
    if not pg_url.startswith('postgresql'):
        return pg_url.replace('postgres://', 'postgresql+psycopg2://')
    return pg_url


engine = create_engine(get_pg_url())


class User(BaseModel):
    uid: Optional[int] = None
    name: str
    surname: str
    age: int


def create_tables() -> None:
    with engine.connect() as conn:
        # RAW sql xD
        conn.execute(text(
            """
            CREATE TABLE IF NOT EXISTS users (
                uid SERIAL PRIMARY KEY,
                name varchar(255) NOT NULL CHECK (name <> ''),
                surname varchar(255),
                age integer
            )
            """
        ))


def add_user(user: User) -> None:
    with engine.connect() as conn:
        conn.execute(text(
            "INSERT INTO users (name, surname, age) VALUES (:name, :surname, :age)"
        ), [user.dict()])


__all__ = (
    'User',
    'create_tables',
    'add_user',
)
