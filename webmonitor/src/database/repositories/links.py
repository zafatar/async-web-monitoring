from psycopg2 import Error

import logging

from src.database.repositories.base import BaseRepository
from src.exceptions.database import DatabaseInsertError

logger = logging.getLogger(__name__)


class LinksRepository(BaseRepository):
    # Links repository to handle the database operations
    table_name = "links"
    table_fields = [
        "id",
        "title",
        "description",
        "url",
        "search_regex",
        "access_interval",
        "created_at",
        "updated_at",
    ]

    def __init__(self):
        super().__init__(table_name=self.table_name, table_fields=self.table_fields)

    def get_all(self, offset: int = 0, limit: int = None) -> list:
        """Get all links from the database

        Returns:
            list: list of links
        """
        with self.conn:
            cursor = self._set_cursor()

            query = f"SELECT {self.fields_as_str} FROM {self.table_name}"
            if limit is not None:
                query += f" OFFSET {offset}"
                query += f" LIMIT {limit}"

            cursor.execute(query)
            return cursor.fetchall()

    def get_by_id(self, id: int) -> tuple:
        """Get a link by its ID

        Args:
            id (int): the ID of the link

        Returns:
            tuple: the link
        """
        with self.conn:
            cursor = self._set_cursor()
            cursor.execute(
                f"SELECT {self.fields_as_str} FROM {self.table_name} WHERE id = %s",
                (id,),
            )
            return cursor.fetchone()

    def get_by_url(self, url: str) -> tuple:
        """Get a link by its URL

        Args:
            url ): URL of the link

        Returns:
            tuple: _description_
        """
        with self.conn:
            cursor = self._set_cursor()
            cursor.execute(
                f"SELECT {self.fields_as_str} FROM {self.table_name} WHERE url = %s",
                (url,),
            )
            return cursor.fetchone()

    def insert(
        self,
        title: str,
        description: str,
        url: str,
        search_regex: str,
        access_interval: int,
    ) -> None:
        """Insert a link into the database with the given parameters"""
        with self.conn as conn:
            cursor = self._set_cursor()

            try:
                necessary_link_fields = [
                    field
                    for field in self.table_fields
                    if field not in ["id", "created_at", "updated_at"]
                ]

                query = (
                    "INSERT INTO links ("
                    + ", ".join(necessary_link_fields)
                    + ") \
                        VALUES ("
                    + ", ".join(["%s"] * len(necessary_link_fields))
                    + ")"
                )

                cursor.execute(
                    query, (title, description, url, search_regex, access_interval)
                )
                conn.commit()
            except Error as e:
                logger.error("Error({0}): {1}".format(e.pgcode, e.pgerror))
                raise DatabaseInsertError(message=f"Error inserting link: {e}")
            finally:
                self._close_cursor(cursor)

    def update(self, id, **kwargs):
        raise NotImplementedError("Update method not implemented")
