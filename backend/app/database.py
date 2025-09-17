import os

from sqlmodel import Session, create_engine  # type: ignore

# DATABASE_URL = "sqlite:///database.db"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")

engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session
