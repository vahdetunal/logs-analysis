#!/usr/bin/env python3
import psycopg2


def popular_articles():
    # Returns the three most viewed articles from news database
    conn = psycopg2.connect("dbname='news'")
    cur = conn.cursor()
    cur.execute(
        "select articles.title, count(*) as num "
        "from articles, log "
        "where log.path like '/article/' || articles.slug "
        "and log.status='200 OK' and log.method='GET' "
        "group by title "
        "order by num desc "
        "limit 3;"
    )
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result
