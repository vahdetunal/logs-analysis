#!/usr/bin/env python3
import psycopg2


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
    query = ("select authors.name, count(*) as num "
             "from authors, articles, log "
             "where authors.id=articles.author "
             "and log.path like '/article/' || articles.slug "
             "group by authors.id "
             "order by num desc;"
             )
    return execute_query(query)
