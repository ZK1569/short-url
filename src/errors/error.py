class UrlAlreadyShortened(Exception):
    def __init__(self, message="This url is already shortened"):
        super().__init__(message)


class NotFound(Exception):
    def __init__(self, message="Not found"):
        super().__init__(message)
