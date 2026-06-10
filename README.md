# Sakila Movie Explorer

Interactive console application for searching movies in the Sakila MySQL database with search history logging in MongoDB.

## Features

* Search films by keyword
* Search by:

  * Title
  * Description
  * Actor name
* Search films by category and release year range
* Input validation for:

  * Menu selections
  * Genre selection
  * Year ranges
* Paginated results (10 films per page)
* Display film information:

  * Film ID
  * Title
  * Release Year
  * Rating
  * Category
  * Short Description
* Save search history in MongoDB
* Show 5 most popular searches
* Show last 5 searches
* Error handling with reusable decorators

## Technologies

* Python 3
* MySQL (Sakila)
* MongoDB
* PyMySQL
* PyMongo
* python-dotenv

## Project Structure

```text
Movie-Catalog-Manager/
│
├── main.py
│   └── Application interface and business logic
│
├── mysql_connector.py
│   └── MySQL database operations
│
├── log_writer.py
│   └── MongoDB logging and statistics
│
├── decorators.py
│   └── Reusable decorators
│
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore
```

## Environment Variables

Create a `.env` file:

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

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

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

## Search History

All searches are stored in MongoDB collection:

```text
final_project_121225_anton_samoilenko
```

Each record contains:

* Search type
* Search parameters
* Number of results found
* Timestamp

## Author

Anton Samoilenko

Final Project — Python Developer Course

