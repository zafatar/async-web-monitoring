class DatabaseException(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, message):
        super().__init__(message)


class DatabaseConnectionError(DatabaseException):
    """Exception raised for errors in the database connection.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        super().__init__(message)


class DatabaseQueryError(DatabaseException):
    """Exception raised for errors in the database query.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        super().__init__(message)


class DatabaseInsertError(DatabaseException):
    """Exception raised for errors in the database insert.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        super().__init__(message)
