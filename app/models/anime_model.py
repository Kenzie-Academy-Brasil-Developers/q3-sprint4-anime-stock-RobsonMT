from psycopg2 import sql

from app.models import DatabaseConnector


class Anime(DatabaseConnector):
    table_name = "animes"

    def __init__(self, **kwargs) -> None:
        self.anime = kwargs["anime"].title()
        self.released_date = kwargs["released_date"]
        self.seasons = kwargs["seasons"]

    def insert_into(self):
        self.get_conn_cur()

        sql_table_name = sql.Identifier(self.table_name)
        columns = [sql.Identifier(key) for key in self.__dict__.keys()]
        values = [sql.Literal(value) for value in self.__dict__.values()]

        query = sql.SQL(
            """
            INSERT INTO {table}
                ({columns})
            VALUES
                ({values})
            RETURNING id, anime, to_char(released_date,'DD/MM/YYYY'), seasons;
        """
        ).format(
            table=sql_table_name,
            columns=sql.SQL(",").join(columns),
            values=sql.SQL(",").join(values),
        )

        self.cur.execute(query)

        inserted_serie = self.cur.fetchone()

        self.commit_and_close()

        return inserted_serie

    @classmethod
    def select_all(cls):
        cls.get_conn_cur()

        sql_table_name = sql.Identifier(cls.table_name)

        query = sql.SQL(
            """
                SELECT * FROM {table}
            """
        ).format(table=sql_table_name)

        cls.cur.execute(query)

        result = cls.cur.fetchall()

        print("=" * 100)
        print(query.as_string(cls.cur))
        print("=" * 100)

        cls.commit_and_close()

        return result
