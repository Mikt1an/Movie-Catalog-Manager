import os
import pymysql
import dotenv
from pymysql.cursors import DictCursor

dotenv.load_dotenv()


class DBSQL():
    """
       MySQL database context manager.

       Environment variables:
           DB_HOST_EDIT: Database host.
           DB_USER_EDIT: Database username.
           DB_PASSWORD_EDIT: Database password.
           DB_NAME_WORLD: World database name.

       Handles:
            - database connection
            - query execution
            - transaction commits
    """
    def __init__(self):
        self.__config = {"host": os.getenv("DB_HOST"),
                         "user": os.getenv("DB_USER"),
                         "password": os.getenv("DB_PASSWORD"),
                         "database": os.getenv("DB_NAME_WORLD"),
                         'cursorclass': DictCursor,
                         }
        self.database = self.__config.get("database")

    def __enter__(self):
        self.__conn = pymysql.connect(**self.__config)
        self.__cursor = self.__conn.cursor()
        print("Connection SQL successful!")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__cursor.close()
        self.__conn.close()
        return False

    def _execute(self, query, params = None):
        self.__cursor.execute(query, params)
        return self.__cursor.fetchall()

    def _commit(self):
        self.__conn.commit()


class Command(DBSQL):
    """
    Provides commands for searching films in the Sakila database.
    """
    def use_db(self, database):
        text = f"""
                USE {database}
        """
        print(f"Connecting to {database}")
        return self._execute(text)

    def get_film(self):
        text = """
                SELECT *
                FROM film
                limit 10;
               """
        return self._execute(text)

    def count_films_by_keyword(self, keyword, search_field):
        if search_field == 1:
            condition = "film.title LIKE %s"
        elif search_field == 2:
            condition = "film.description LIKE %s"
        elif search_field == 3:
            condition = """
                EXISTS (
                    SELECT 1
                    FROM film_actor
                    JOIN actor
                        ON film_actor.actor_id = actor.actor_id
                    WHERE film_actor.film_id = film.film_id
                      AND CONCAT(actor.first_name, ' ', actor.last_name) LIKE %s
                )
            """
        else:
            return 0

        query = f"""
            SELECT COUNT(*) AS total
            FROM film
            WHERE {condition}
        """

        result = self._execute(query, (f"%{keyword}%",))
        return result[0]["total"]

    def search_films_by_keyword_field(
            self,
            keyword,
            search_field,
            limit=10,
            offset=0
    ):
        if search_field == 1:
            condition = "film.title LIKE %s"
        elif search_field == 2:
            condition = "film.description LIKE %s"
        elif search_field == 3:
            condition = """
                EXISTS (
                    SELECT 1
                    FROM film_actor
                    JOIN actor
                        ON film_actor.actor_id = actor.actor_id
                    WHERE film_actor.film_id = film.film_id
                      AND CONCAT(actor.first_name, ' ', actor.last_name) LIKE %s
                )
            """
        else:
            return []

        query = f"""
            SELECT
                film.film_id,
                film.title,
                film.description,
                film.release_year,
                film.rating,
                category.name AS category
            FROM film
            JOIN film_category
                ON film.film_id = film_category.film_id
            JOIN category
                ON film_category.category_id = category.category_id
            WHERE {condition}
            ORDER BY film.title
            LIMIT %s
            OFFSET %s
        """

        return self._execute(
            query,
            (f"%{keyword}%", limit, offset)
        )

    def get_categories(self):
        text = """
               SELECT category_id, name
               FROM category
               ORDER BY name 
               """
        return self._execute(text)

    def get_min_max_years(self, category_id = None):
        if category_id is None:
            text = """
                   SELECT MIN(release_year) AS min_year, 
                          MAX(release_year) AS max_year
                   FROM film 
                   """
            return self._execute(text)[0]
        text = """
                SELECT MIN(release_year) AS min_year, 
                      MAX(release_year) AS max_year
                FROM film
                JOIN film_category
                ON film.film_id = film_category.film_id
                WHERE film_category.category_id = %s
                """
        return self._execute(text, (category_id,))[0]

    def count_films_by_category_and_years(
            self,
            category_id,
            year_from,
            year_to,
    ):
        text = """
               SELECT COUNT(*) AS total
               FROM film
                        JOIN film_category
                             ON film.film_id = film_category.film_id
               WHERE film_category.category_id = %s
                 AND film.release_year BETWEEN %s AND %s 
               """
        result = self._execute(text, (category_id, year_from, year_to))
        return result[0]["total"]

    def search_films_by_category_and_years(
            self,
            category_id,
            year_from,
            year_to,
            limit=10,
            offset=0,
    ):
        text = """
               SELECT film.film_id, \
                      film.title, \
                      film.description, \
                      film.release_year, \
                      film.rating, \
                      category.name AS category
               FROM film
                        JOIN film_category
                             ON film.film_id = film_category.film_id
                        JOIN category
                             ON film_category.category_id = category.category_id
               WHERE category.category_id = %s
                 AND film.release_year BETWEEN %s AND %s
               ORDER BY film.title
                   LIMIT %s
               OFFSET %s \
               """

        return self._execute(
            text,
            (category_id, year_from, year_to, limit, offset)
        )