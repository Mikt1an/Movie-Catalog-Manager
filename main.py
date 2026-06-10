import mysql_connector as sql
from log_writer import LogWriter
from functools import wraps


def frame(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("=" * 50)
        result = func(*args, **kwargs)
        print("=" * 50)
        return result
    return wrapper


class MainApp(sql.Command, LogWriter):
    """
       Main application class for Sakila Movie Explorer.

       Features:
           - search films by keyword
           - search films by genre and year range
           - store search history in MongoDB
           - show popular searches
           - show recent searches
   """
    def __init__(self):
        sql.Command.__init__(self)
        LogWriter.__init__(self)

    def __enter__(self):
        sql.Command.__enter__(self)
        LogWriter.__enter__(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sql.Command.__exit__(self, exc_type, exc_val, exc_tb)
        LogWriter.__exit__(self, exc_type, exc_val, exc_tb)
        return False

    @frame
    def show_menu(self):
        print("--- Sakila Movie Explorer ---".center(50),
              "\n0. Exit\n"
              "1. Search films by keyword\n"
              "2. Search films by genre and year range\n"
              "3. Show 5 popular searches\n"
              "4. Show last 5 searches\n"
              )

    def os_menu(self):
        match self.menu:
            case 1:
                self.search_films_by_keyword()
            case 2:
                self.search_films_genre_year_range()
            case 3:
                self.popular_searches()
            case 4:
                self.last_searches()
            case 0:
                print("Goodbye!")
                return "0"
            case _:
                print("Invalid option. Try again.")

    def search_films_by_keyword(self):
        self.search_field = self._menu_keyword()
        if self.search_field is None:
            return

        self.keyword = self.get_input("Enter search keyword: ")

        self._total = self.count_films_by_keyword(
            self.keyword,
            self.search_field
        )

        if self._total == 0:
            print("\nNo films found. Try another search.")
            return self.search_films_by_keyword()

        print(f"\nFound {self._total} films")

        self.save_search_query(
            "keyword",
            {
                "field": self.search_field,
                "keyword": self.keyword
            },
            self._total
        )

        self._offset = 0

        res = self._choice_menu(
            self.search_films_by_keyword_field,
            self.keyword,
            self.search_field
        )

        # if res is None:
        #     return

    def _menu_keyword(self):
        while True:
            print(
                "\nSearch in:\n"
                "0. Exit\n"
                "1. Title\n"
                "2. Description\n"
                "3. Actors\n"
            )
            search_field = self.get_input("\nChoose search field: ",
                                          int
                                          )

            if search_field in (1, 2, 3):
                return search_field
            elif search_field == 0:
                return None
            print("Invalid option. Try again.")

    def search_films_genre_year_range(self):
        """
        Search films by selected genre
        and year range with pagination.
        """
        categories = self.get_categories()

        for category in categories:
            print(
                f"{category['category_id']:2} | "
                f"{category['name']}"
            )
        years = self.get_min_max_years()
        print(f"All available years: "
              f"{years['min_year']} - {years['max_year']}"
              )
        number_genre = self.get_input("Enter number genre: ", int)

        genre_name = None
        while genre_name is None:
            number_genre = self.get_input(
                "Enter number genre: ",
                int
            )

            for category in categories:
                if int(category["category_id"]) == number_genre:
                    genre_name = category["name"]
                    break

            if genre_name is None:
                print("Invalid genre number. Try again.")

        years = self.get_min_max_years(number_genre)

        number_min_year = self.get_input(
            f"Enter minimum year from {years['min_year']} "
            f"since {years['max_year']}: ",
                                         int,
        )

        number_max_year = self.get_input(
            f"Enter maximum year from {number_min_year} "
            f"since {years['max_year']}: ",
                                         int,
        )

        self._total = self.count_films_by_category_and_years(
            number_genre,
            number_min_year,
            number_max_year
        )

        print(f"\nFound {self._total} films")

        self.save_search_query(
            "genre_year",
            {
                "genre_id": number_genre,
                "genre_name": genre_name,
                "year_from": number_min_year,
                "year_to": number_max_year
            },
            self._total
        )

        self._offset = 0

        res = self._choice_menu(
            self.search_films_by_category_and_years,
            number_genre,
            number_min_year,
            number_max_year,
        )

    def popular_searches(self):
        print()
        queries = self.get_popular_queries()

        for query in queries:
            data = query["_id"]

            if isinstance(data, dict):

                if "keyword" in data:
                    print(
                        f"Keyword: {data['keyword']} "
                        f"({query['count']} times)"
                    )

                elif "genre_name" in data:
                    print(
                        f"Genre: {data['genre_name']} | "
                        f"Years: {data['year_from']}-{data['year_to']} "
                        f"({query['count']} times)"
                    )

            else:
                print(
                    f"{data} "
                    f"({query['count']} times)"
                )
        print()

    def last_searches(self):
        print()
        queries = self.get_last_queries()

        for i, query in enumerate(queries, start=1):
            search_type = query.get("search_type")
            data = query.get("query_data")
            created_at = query.get("created_at")

            if search_type == "keyword":
                keyword = (
                    data.get("keyword")
                    if isinstance(data, dict)
                    else data
                )

                print(
                    f"{i}. Keyword: {keyword} | "
                    f"{created_at:%d.%m.%Y %H:%M}"
                )

            elif search_type == "genre_year":
                genre = (
                        data.get("genre_name")
                        or data.get("genre")
                        or data.get("genre_id")
                )

                print(
                    f"{i}. Genre: {genre} | "
                    f"Years: {data.get('year_from')}-{data.get('year_to')} | "
                    f"{created_at:%d.%m.%Y %H:%M}"
                )

            else:
                print(f"{i}. {search_type}: {data} | "
                      f"{created_at:%d.%m.%Y %H:%M}")
        print()

    @frame
    def _choice_menu(self, search_func, *args):
        """
        Displays paginated search results
        and handles navigation between pages.
        """
        limit = 10
        while True:
            items = search_func(*args, limit=limit, offset=self._offset)

            if not items:
                print("No more results.")
                break
            print(
                f"\nShowing "
                f"{self._offset + 1}"
                f"-{min(self._offset + limit, self._total)} "
                f"of {self._total}"
            )

            for film in items:
                description = film["description"] or ""

                print(
                    f"{film['film_id']:4} | "
                    f"{film['title']}"
                )

                print(
                    f"Year: {film['release_year']} | "
                    f"Rating: {film['rating']} | "
                    f"Category: {film['category']}"
                )

                print(
                    f"Description: "
                    f"{description[:90]}..."
                )

                print("-" * 50)

            choice = self.get_input(
                "\n[N]ext 10 results\n"
                "[B]ack 10 results\n"
                "[M]ain menu\n"
                "Choose: ",
            ).lower()

            if choice == "n":
                if self._offset + limit >= self._total:
                    print("No more results.")
                else:
                    self._offset += limit

            elif choice == "b":
                if self._offset == 0:
                    print("Already on the first page.")
                else:
                    self._offset -= limit

            elif choice == "m":
                return None
            else:
                print("Invalid option. Try again.")

    def get_input(
            self,
            message,
            value_type=str
    ):
        while True:
            try:
                return value_type(input(message))
            except ValueError:
                print(
                    f"Please enter a valid "
                    f"{value_type.__name__}."
                )

    def run(self):
        with (self):
            while True:
                self.show_menu()
                self.menu = self.get_input("Enter number: ", int)
                if self.os_menu() == 0:
                    break


if __name__ == "__main__":
    app = MainApp()
    app.run()
