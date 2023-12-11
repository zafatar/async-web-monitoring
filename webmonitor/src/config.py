"""
Config file for the settings
"""
from typing import Optional, Union
from urllib.parse import quote

from pydantic import Field, PostgresDsn, ValidationInfo, field_validator
from pydantic_settings import BaseSettings

from src.exceptions.config import MissingDatabaseConnectionString


class Settings(BaseSettings):
    """Setting class for the configuration"""

    PROJECT_VERSION: str = Field(..., env="PROJECT_VERSION")

    POSTGRES_HOST: str = Field(..., env="POSTGRES_HOST")
    POSTGRES_PORT: str = Field(..., env="POSTGRES_PORT")
    POSTGRES_USER: str = Field(..., env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(..., env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field(..., env="POSTGRES_DB")

    # Db connection string.
    SQLALCHEMY_DATABASE_URI: Union[Optional[PostgresDsn], Optional[str]] = None

    # SECRET_KEY: str = Field(..., env='SECRET_KEY')  # secrets.token_urlsafe(32)

    DEBUG: bool = Field(..., env="DEBUG")

    # NOTE: This is unnecessary at the moment since we don't use SQLAlchemy.
    #       But it's good to have it for future reference if we decide to use it.
    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, dsn: Optional[str], values: ValidationInfo) -> str:
        """Builds the db string for the SQLAlchemy

        Args:
            v (Optional[str]): string itself
            values (Dict[str, Any]): list of connection attributes

        Returns:
            Any: Postgresql DSN
        """
        if isinstance(dsn, str):
            return dsn

        if values.data.get("POSTGRES_HOST") is not None:
            quoted_password = quote(values.data.get("POSTGRES_PASSWORD"))
            complete_host = (
                f'{values.data.get("POSTGRES_HOST")}:{values.data.get("POSTGRES_PORT")}'
            )

            dsn = PostgresDsn.build(  # noqa
                scheme="postgresql",
                username=values.data.get("POSTGRES_USER"),
                password=quoted_password,  # quote the special chars
                host=complete_host,
                path=f"{values.data.get('POSTGRES_DB') or ''}",
            )
        else:
            raise MissingDatabaseConnectionString

        return str(dsn)

    def __str__(self) -> str:
        """
        Customized str for the settings
        """
        rep_string = "Settings:\n"
        for key, value in self.model_dump().items():
            rep_string += f"\t{key}: {value}\n"

        return rep_string

    class Config:  # noqa
        """Config of BaseSettings"""

        case_sensitive = True
        env_file = ".env"  # we don't need this but good to have it for local run
        env_file_encoding = "utf-8"


settings = Settings()
