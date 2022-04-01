from psycopg2 import sql

from app.models import DatabaseConnector


class Anime(DatabaseConnector):
    def __init__(self, **kwargs) -> None:
        self.anime: str = kwargs["anime"].title()
        self.released_date: str = kwargs["released_date"]
        self.seasons: int = kwargs["seasons"]

    @classmethod
    def create_table(cls):
        cls.get_conn_cur()

        query = """
            CREATE TABLE IF NOT EXISTS animes (
                id BIGSERIAL PRIMARY KEY,
                anime VARCHAR(100) NOT NULL UNIQUE,
                released_date DATE NOT NULL,
                seasons INTEGER NOT NULL 
            );
        """

        cls.cur.execute(query)

        cls.commit_and_close()

    def insert_into(self):
        self.create_table()
        self.get_conn_cur()

        values = [sql.Literal(value) for value in self.__dict__.values()]

        query = sql.SQL(
            """
            INSERT INTO animes
                (anime, released_date , seasons)
            VALUES
                ({values})
            RETURNING 
                id, anime, 
                to_char(released_date,'DD/MM/YYYY') as released_date, 
                seasons;
        """
        ).format(values=sql.SQL(",").join(values))

        self.cur.execute(query)

        inserted_serie = self.cur.fetchone()

        self.commit_and_close()

        return inserted_serie

    @classmethod
    def select_all(cls) -> list:
        cls.create_table()
        cls.get_conn_cur()

        query = """
            SELECT 
                id, anime, 
                to_char(released_date,'DD/MM/YYYY') as released_date, 
                seasons 
            FROM animes
            ORDER BY id;
        """

        cls.cur.execute(query)

        result = cls.cur.fetchall()

        cls.commit_and_close()

        return result

    @classmethod
    def select_by_id(cls, anime_id: int):
        cls.get_conn_cur()

        sql_anime_id = sql.Literal(anime_id)

        query = sql.SQL(
            """
                SELECT 
                    id, anime, 
                    to_char(released_date,'DD/MM/YYYY') as released_date, 
                    seasons
                FROM animes
                WHERE id = {id};
            """
        ).format(id=sql_anime_id)

        cls.cur.execute(query)

        anime = cls.cur.fetchone()

        cls.commit_and_close(commit=False)

        return anime

    @classmethod
    def update_by_id(cls, anime_id: int, payload: dict):
        cls.get_conn_cur()

        columns = [sql.Identifier(key) for key in payload.keys()]
        values = [sql.Literal(value) for value in payload.values()]
        sql_anime_id = sql.Literal(anime_id)

        query = sql.SQL(
            """
                UPDATE
                    animes
                SET
                    ({columns}) = ROW({values})
                WHERE
                    id = {id}
                RETURNING
                    id, anime, 
                    to_char(released_date,'DD/MM/YYYY') as released_date, 
                    seasons;
            """
        ).format(
            columns=sql.SQL(",").join(columns),
            values=sql.SQL(",").join(values),
            id=sql_anime_id,
        )

        cls.cur.execute(query)

        updated_user = cls.cur.fetchone()

        cls.commit_and_close()

        return updated_user

    @classmethod
    def delete_by_id(cls, anime_id: int):
        cls.get_conn_cur()

        sql_anime_id = sql.Literal(anime_id)

        query = sql.SQL(
            """
                DELETE FROM animes
                WHERE id = {id}
                RETURNING *;
            """
        ).format(id=sql_anime_id)

        cls.cur.execute(query)

        deleted_anime = cls.cur.fetchone()

        cls.commit_and_close()

        return deleted_anime
