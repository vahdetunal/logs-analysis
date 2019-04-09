#!/usr/bin/env python3
import psycopg2
from tabulate import tabulate


def execute_query(query_string):
    """Executes the given query.

    Arguments:
    query_string -- The SQL query to be executed
    """
    conn = psycopg2.connect("dbname='news'")
    cur = conn.cursor()
    cur.execute(query_string)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result


def popular_articles():
    # Returns the three most viewed articles from news database

    # log table has only the statuses 200 OK and 404 ERROR where
    # request is made to an incorrect uri. Howeever, it could possibly
    # have POST requests from author or some errors.
    # Therefore, status and method conditions are left in the query.
    query = ("select articles.title, count(*) as num "
             "from articles, log "
             "where log.path like '/article/' || articles.slug "
             "and log.status='200 OK' and log.method='GET' "
             "group by title "
             "order by num desc "
             "limit 3;"
             )
    return execute_query(query)


def author_ranking():
    # Returns names of the authors and their view counts, sorted by views

    # Article URIs have the form /article/slug. Counting access to URIs
    # that are an exact match to the given form reveals how many times they
    # are viewed.
    query = ("select authors.name, count(*) as num "
             "from authors, articles, log "
             "where authors.id=articles.author "
             "and log.path like '/article/' || articles.slug "
             "group by authors.id "
             "order by num desc;"
             )
    return execute_query(query)


def error_statistics():
    # Returns the days when more than 2% of the requests resulted in an error.
    request_subquery = ("(select date(time) as days, count(*) as num from log "
                        "group by days) as requests "
                        )
    error_subquery = ("(select date(time) as days, count(*) as num from log "
                      "where status='404 NOT FOUND' "
                      "group by days) as errors "
                      )
    query = ("select requests.days, "
             "errors.num/cast(requests.num as float) as error_rate from "
             + request_subquery
             + 'left join '
             + error_subquery
             + "on requests.days = errors.days "
             "where errors.num/cast(requests.num as float) > 0.01 "
             "order by days;"
             )
    return execute_query(query)


def format_error_statistics(error_stats):
    # Formats the output of error query rate from floats to percntage strings
    for i in range(len(error_stats)):
        entry = error_stats[i]
        percentage = round(entry[1]*100, 2)
        percentage_str = str(percentage) + '%'
        error_stats[i] = (entry[0], percentage_str)
    return error_stats


def generate_report(articles, authors, error_stats):
    # Generates a report using query results and tabulate library
    article_headers = ['Title', 'Views']
    author_headers = ['Name', 'Views']
    error_headers = ['Date', 'Error Rate']

    article_table = tabulate(articles, headers=article_headers)
    author_table = tabulate(authors, headers=author_headers)
    error_table = tabulate(error_stats, headers=error_headers)

    report = ('===== Three Most Viewed Articles =====\n'
              + article_table
              + '\n\n'
              + '===== Author Ropularity Ranking =====\n'
              + author_table
              + '\n\n'
              + '===== Days with Request Errors Higher than 1% =====\n'
              + error_table
              )
    return report


def main():
    # Obtain the data for the report from the database
    articles = popular_articles()
    authors = author_ranking()
    error_stats = format_error_statistics(error_statistics())

    # Generate and print the report
    report = generate_report(articles, authors, error_stats)
    print(report)


# Run the main function if called from terminal.
if __name__ == '__main__':
    main()
