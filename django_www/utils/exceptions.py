class APIException(Exception):
    def __init__(self, msg):
        super().__init__()
        self.msg = msg


class ParamException(Exception):
    def __init__(self, msg):
        super().__init__()
        self.msg = msg


class ParseShortenUrlException(Exception):
    def __init__(self, msg):
        super().__init__()
        self.msg = msg


class UrlNotExistException(Exception):
    def __init__(self):
        super().__init__()
