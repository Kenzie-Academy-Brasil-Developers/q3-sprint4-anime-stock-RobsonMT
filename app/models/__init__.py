from psycopg2 import extras
import psycopg2
import os


configs = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}


class DatabaseConnector:
    @classmethod
    def get_conn_cur(cls):
        cls.conn = psycopg2.connect(**configs)
        cls.cur = cls.conn.cursor(cursor_factory=extras.RealDictCursor)

    @classmethod
    def commit_and_close(cls, commit=True):
        if commit:
            cls.conn.commit()
        cls.cur.close()
        cls.conn.close()
