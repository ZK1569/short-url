from abc import ABC, abstractmethod

from ..models.url import Url


class UrlRepositoryAbs(ABC):

    @abstractmethod
    def save(self, long_url: str, short_url: str) -> Url:
        pass

    @abstractmethod
    def get_url_by_short_url(self, short_url: str) -> Url:
        pass

    @abstractmethod
    def increment_calls(self, url: Url) -> Url:
        pass

    @abstractmethod
    def list_all(self) -> list[Url]:
        pass
