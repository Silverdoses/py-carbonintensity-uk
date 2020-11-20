class APIException(Exception):
    pass


class APIStatusError(APIException):
    pass


class APITypeError(APIException):
    pass


class APIConstraintException(APIException):
    pass
