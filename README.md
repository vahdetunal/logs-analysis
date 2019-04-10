# logs-analysis

logs-analysis is a simple tool to generate reports from a newspaper website 
database. The tool answers three questions:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Getting Started

Following instructions will help you run the project on your local machine.

### Prerequisites

- Python 3: Instructions for installing python 3 can be found [here](
  https://realpython.com/installing-python/)
- psycopg2: Installation instructions can be found [here](
  http://initd.org/psycopg/docs/install.html)
- tabulate: You can install tabulate from the command line using:
  `pip install tabulate`

### Installing

If you have git installed, you can fork the project from terminal using:
`git clone https://github.com/vahdetunal/logs-analysis.git`

Alternatively, it can be downloaded directly from [github](
    https://github.com/vahdetunal/logs-analysis.git).

## How to Use?

news database analysed by the project should be placed into the same directory
as log_analysis.py.

Using `python3 log_analysis.py` command in the terminal will generate and print
the report.

## Design

The function `execute_query(query_string)` is used to run the queries using 
psycopg2 against the news database.

Functions `popular_articles()`, `author_ranking()` and `error_statistics()`
contain query strings to answer the three questions given above in order. These
functions run the queries making use of the execute_query function. The output
of error_statistics requires some further formatting which is done by
the function `format_error_statistics(error_stats)`.

The function `generate_report(articles, authors, error_stats)` uses the outputs
from three query functions to generate the report. tabulate library is used to
format the tables in plain text.

The main function makes use of the three query funcions `popular_articles()`, 
`author_ranking()`, `error_statistics()` and the generate_report function
to obtain and print the report.