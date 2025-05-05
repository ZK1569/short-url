from typing import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from ..env import EnvVariable


class PostgresqlDatabase:
    def __init__(self) -> None:
        db_url = f"postgresql://{EnvVariable().db_user}:{EnvVariable().db_password}@{EnvVariable().db_host}:{EnvVariable().db_port}/{EnvVariable().db_name}"
        self.engine = create_engine(db_url, pool_pre_ping=True)
        self.session_local = sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False
        )
        self.base = declarative_base()

    def setup_database(self) -> None:
        self._check_connection()
        self.base.metadata.create_all(self.engine)

    def get_session(self) -> Generator[Session, None, None]:
        db = self.session_local()
        try:
            yield db
        finally:
            db.close()

    def _check_connection(self) -> None:
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
        except SQLAlchemyError as e:
            raise ConnectionError(f"Database connection failed: {e}")


postgresql_database = PostgresqlDatabase()
