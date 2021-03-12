class BaseAPIException(Exception):
    pass


class JSONClientException(BaseAPIException):
    pass


class XMLClientException(BaseAPIException):
    pass


class APIConstraintException(BaseAPIException):
    pass
