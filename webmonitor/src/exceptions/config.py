"""Custom exceptions for the config module."""


class ConfigFileNotFound(Exception):
    """Raised when the config file is not found."""

    def __init__(self, message="Config file not found."):
        self.message = message
        super().__init__(self.message)


class MissingDatabaseConnectionString(Exception):
    """Raised when the database connection string is missing."""

    def __init__(self, message="Missing database connection string."):
        self.message = message
        super().__init__(self.message)
