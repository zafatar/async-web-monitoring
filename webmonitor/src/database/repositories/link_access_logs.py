from datetime import datetime

from psycopg2 import Error

from src.database.repositories.base import BaseRepository
from src.exceptions.database import DatabaseInsertError


class LinkAccessLogsRepository(BaseRepository):
    # LinkAccessLogs repository to handle the database operations
    table_name = "link_access_logs"
    table_fields = ["link_id", "accessed_at", "status_code", "is_regex_match"]

    def __init__(self):
        super().__init__(table_name=self.table_name, table_fields=self.table_fields)

    def get_all_logs_by_link_id(self, link_id: int) -> list:
        """Get all logs from the database by link ID

        Args:
            link_id (int): the ID of the link

        Returns:
            list: list of logs
        """
        with self.conn:
            cursor = self._set_cursor()
            cursor.execute(
                f"""SELECT {self.fields_as_str}
                    FROM {self.table_name}
                    WHERE link_id = %s""",
                (link_id,),
            )
            return cursor.fetchall()

    def get_first_log_by_link_id(self, link_id: int) -> dict:
        """Get the first log from the database by link ID

        Args:
            link_id (int): the ID of the link

        Returns:
            dict: the first log
        """
        with self.conn:
            cursor = self._set_cursor()
            cursor.execute(
                f"""SELECT {self.fields_as_str}
                    FROM {self.table_name}
                    WHERE link_id = %s ORDER BY accessed_at ASC LIMIT 1""",
                (link_id,),
            )
            return cursor.fetchone()

    def get_last_log_by_link_id(self, link_id: int) -> dict:
        """Get the last log from the database by link ID

        Args:
            link_id (int): the ID of the link

        Returns:
            dict: the last log
        """
        with self.conn:
            cursor = self._set_cursor()
            cursor.execute(
                f"""SELECT {self.fields_as_str}
                    FROM {self.table_name}
                    WHERE link_id = %s ORDER BY accessed_at DESC LIMIT 1""",
                (link_id,),
            )
            return cursor.fetchone()

    def get_all_stats(self) -> dict[int, dict]:
        """Get all stats from the database

        Returns:
            list: list of stats
        """
        with self.conn:
            cursor = self._set_cursor()
            cursor.execute(
                f"""SELECT
                    link_id,
                    COUNT(*) AS total_access,
                    MIN(accessed_at) AS first_accessed_at,
                    MAX(accessed_at) AS last_accessed_at
                FROM {self.table_name}
                GROUP BY link_id""",
            )

            stats = cursor.fetchall()

            # Convert the stats to a dict
            stats_dict = {}
            for link_stat in stats:
                stats_dict[link_stat["link_id"]] = link_stat

            return stats_dict

    def get_stats_by_link_id(self, link_id: int) -> dict:
        """Get the stats from the database by link ID

        Args:
            link_id (int): the ID of the link

        Returns:
            dict: the stats
        """
        with self.conn:
            cursor = self._set_cursor()
            cursor.execute(
                f"""SELECT
                    COUNT(*) AS total_access,
                    MIN(accessed_at) AS first_accessed_at,
                    MAX(accessed_at) AS last_accessed_at
                FROM {self.table_name} WHERE link_id = %s""",
                (link_id,),
            )
            return cursor.fetchone()

    def insert(
        self,
        link_id: int,
        accessed_at: datetime,
        status_code: int,
        is_regex_match: bool,
    ) -> None:
        """Insert a new log in the database with the given parameters"""
        with self.conn as conn:
            try:
                cursor = self._set_cursor()
                cursor.execute(
                    f"""INSERT INTO {self.table_name} ({self.fields_as_str})
                        VALUES (%s, %s, %s, %s)""",
                    (link_id, accessed_at, status_code, is_regex_match),
                )
                conn.commit()
            except Error as e:
                raise DatabaseInsertError(f"Error inserting log: {e}")
            finally:
                self._close_cursor(cursor)

    def update(self, link_id: int, **kwargs) -> None:
        raise NotImplementedError("Update method not implemented")
