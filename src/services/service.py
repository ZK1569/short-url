from abc import ABC, abstractmethod

from ..models.url import Url


class UrlServiceAbs(ABC):

    @abstractmethod
    def get_all_urls(self) -> list[Url]:
        pass

    @abstractmethod
    def generate_url(self, long_url: str) -> str:
        pass

    @abstractmethod
    def get_long_url_and_increment(self, short_url: str) -> str:
        pass
