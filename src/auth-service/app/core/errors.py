class AuthErrorException(Exception):
    pass 


class IntegrityErrorException(Exception):
    pass


class DataErrorException(Exception):
    pass


class OperationalErrorException(Exception):
    pass


class TokenErrorException(Exception):
    pass

class SQLAlchemyErrorException(Exception):
    pass


class ValidationErrorException(Exception):
    pass


class InvalidTokenError(Exception):
    pass


class ExpiredTokenError(Exception):
    pass

class TokenError(Exception):
    pass 