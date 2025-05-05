import hashlib
from typing import Generator

from fastapi import Depends

from ..models.url import Url
from ..repositories.repository import UrlRepositoryAbs
from ..repositories.url import get_url_repository
from ..utils.env import EnvVariable
from .service import UrlServiceAbs


class UrlService(UrlServiceAbs):
    def __init__(self, url_repository: UrlRepositoryAbs):
        self.url_repository = url_repository
        self._prefix = EnvVariable().short_url_prefix

    def get_all_urls(self) -> list[Url]:
        return self.url_repository.list_all()

    def generate_url(self, long_url: str) -> str:
        short_url = self._generate_short_url(long_url)
        self.url_repository.save(long_url, short_url)

        return f"{self._prefix}{short_url}"

    def get_long_url_and_increment(self, short_url: str) -> str:
        url = self.url_repository.get_url_by_short_url(short_url)

        self.url_repository.increment_calls(url)

        return str(url.long_url)

    def _generate_short_url(self, url: str, length=7) -> str:
        return hashlib.sha256(url.encode("utf-8")).hexdigest()[:length]


def get_url_service(
    repo: UrlRepositoryAbs = Depends(get_url_repository),
) -> Generator[UrlServiceAbs, None, None]:
    yield UrlService(repo)
