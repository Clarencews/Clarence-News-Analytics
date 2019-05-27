#!/usr/bin/env python3

# Project 1 - Log Analysis

# 1. What are the most popular three articles of all time?
# 2. Who are the most popular article authors of all time?
# 3. On which days did more than 1% of requests lead to errors?

import psycopg2
# need datetime to clean up error dates
import datetime


class style:
    bold = '\033[1m'
    underline = '\033[4m'
    end = '\033[0m'


print(style.bold + "Project 1 - News Analytics" + style.end)


print('\n' + style.underline + "Top 3 Most Views Articles" + style.end)
db = psycopg2.connect("dbname=news")
c = db.cursor()
c.execute('''
    SELECT a.title, v.views
        FROM article_views AS v
        JOIN articles AS a
        ON a.slug = v.slug
        LIMIT 3;''')
for row in c.fetchall():
    title, views = row
    print("%s - %s views" % (title, views))
    db.close()


print('\n' + style.underline + "Most Popular Authors" + style.end)
db = psycopg2.connect("dbname=news")
c = db.cursor()
c.execute('''
    SELECT a.name, CAST(v.sum AS bigint)
        FROM popular_author AS v
        JOIN authors AS a
        ON v.author = a.id;''')
for row in c.fetchall():
    name, views = row
    print("%s - %s views" % (name, views))
    db.close()


print('\n' + style.underline + "Days with more than 1% of errors" + style.end)
db = psycopg2.connect("dbname=news")
c = db.cursor()
c.execute('''
    SELECT DATE(log.time)
    AS DATE,
    round(( COUNT (case when log.status != '200 OK' then log.time end)/
    COUNT (log.status)::float * 100)::numeric,2)
    AS performance
    FROM log
    GROUP BY DATE
    HAVING round(( COUNT (case when log.status != '200 OK' then time end)/
    COUNT (log.status)::float * 100)::numeric,2) > 1;''')
for row in c.fetchall():
    date, performance = row
    print("%s - %s%% error." % (date, performance))
    db.close()
