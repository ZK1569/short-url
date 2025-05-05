from typing import Generator

from fastapi import Depends
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..errors.error import NotFound, UrlAlreadyShortened
from ..models.url import Url
from ..utils.database.postgres import postgresql_database
from .repository import UrlRepositoryAbs


class UrlRepository(UrlRepositoryAbs):
    def __init__(self, db: Session) -> None:
        self.db = db

    def save(self, long_url: str, short_url: str) -> Url:
        url = Url(long_url=long_url, short_url=short_url)
        self.db.add(url)
        try:
            self.db.commit()
            self.db.refresh(url)
            return url
        except IntegrityError:
            self.db.rollback()
            raise UrlAlreadyShortened()

    def get_url_by_short_url(self, short_url: str) -> Url:
        url = self.db.query(Url).filter(Url.short_url == short_url).first()
        if url is None:
            raise NotFound()

        return url

    def increment_calls(self, url: Url) -> Url:
        url.calls += 1
        self.db.commit()
        self.db.refresh(url)

        return url

    def list_all(self) -> list[Url]:
        return self.db.query(Url).order_by(desc(Url.calls)).all()


def get_url_repository(
    db: Session = Depends(postgresql_database.get_session),
) -> Generator[UrlRepositoryAbs, None, None]:
    yield UrlRepository(db)
