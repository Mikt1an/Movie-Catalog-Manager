# Sakila Movie Explorer

Interactive console application for searching movies in the Sakila MySQL database.

## Features

* Search films by keyword
* Search by title, description, or actor name
* Search films by category and release year range
* Paginated output (10 films per page)
* Save search history in MongoDB
* Show 5 most popular searches
* Show last 5 searches
* Display film information:

  * Title
  * Description
  * Release year
  * Rating
  * Category

## Technologies

* Python 3
* MySQL
* MongoDB
* PyMySQL
* PyMongo
* python-dotenv

## Project Structure

```text
Movie-Catalog-Manager/
├── main.py
├── mysql_connector.py
├── log_writer.py
├── requirements.txt
├── .env.example
└── README.md
```

## Environment Variables

Create a `.env` file in the project root directory:

```env
DB_HOST=
DB_USER=
DB_PASSWORD=
DB_NAME_WORLD=sakila

DB_HOST_MONGO=
DB_USER_MONGO=
DB_PASSWORD_MONGO=
DB_NAME_MONGO=
```

## Installation

Install project dependencies:

```bash
pip install -r requirements.txt
```

## Run Application

```bash
python main.py
```

## Main Menu

```text
0. Exit
1. Search films by keyword
2. Search films by genre and year range
3. Show 5 popular searches
4. Show last 5 searches
```

## Search by Keyword

Users can search films by:

```text
1. Title
2. Description
3. Actors
```

The application displays:

* Film ID
* Title
* Release Year
* Rating
* Category
* Short Description

## Search History

All search queries are stored in MongoDB collection:

```text
final_project_121225_anton_samoilenko
```

Stored information includes:

* Search type
* Search parameters
* Number of results found
* Timestamp


## Author

Anton Samoilenko

Final Project — Python Developer Course
