import psycopg2.extras

from src.database.db import conn as db_conn


table_fields = []


class BaseRepository:
    # Links repository to handle the database operations
    table_name = None
    table_fields = []
    fields_as_str = None
    conn = None

    def __init__(self, conn=db_conn, table_name=None, table_fields=None):
        self.table_name = table_name or self.table_name
        self.table_fields = table_fields or self.table_fields
        self.fields_as_str = ", ".join(self.table_fields)

        if self.conn is None:
            self.conn = conn

    def _set_cursor(self):
        return self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def _close_cursor(self, cursor):
        cursor.close()

    def insert(self, **kwargs):
        raise NotImplementedError("Insert method not implemented")

    def update(self, **kwargs):
        raise NotImplementedError("Update method not implemented")
