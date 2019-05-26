# Project 1 - Log Analysis


# 1. What are the most popular three articles of all time? Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.

# 2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.

# 3. On which days did more than 1% of requests lead to errors? The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser. (Refer to this lesson for more information about the idea of HTTP status codes.)

#!/usr/bin/env python3

import psycopg2
# need datetime to clean up error dates
import datetime

# Styling for printed font
class font_style:
	bold = '\033[1m'
	underline = '\033[4m'
	end = '\033[0m'

# print header to project
print(font_style.bold + "Project 1 - News Analytics" + font_style.end)


# 1. What are the most popular three articles of all time? Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.

print('\n' + font_style.underline + "Top 3 Most Views Articles" + font_style.end)
db = psycopg2.connect("dbname=news")
c=db.cursor()
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

# 2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.

print('\n' + font_style.underline + "Most Popular Authors" + font_style.end)
db = psycopg2.connect("dbname=news")
c=db.cursor()
c.execute('''
	SELECT a.name, CAST(v.sum as bigint) 
		FROM popular_author AS v 
		JOIN authors AS a 
		ON v.author = a.id;''')
for row in c.fetchall():
	name, views = row
	print("%s - %s views" % (name, views))
	db.close()


# 3. On which days did more than 1% of requests lead to errors? The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser. (Refer to this lesson for more information about the idea of HTTP status codes.)

print('\n' + font_style.underline + "Days with more than 1% of errors" + font_style.end)
db = psycopg2.connect("dbname=news")
c = db.cursor()
c.execute("SELECT DATE(log.time) as DATE, round(( COUNT (case when log.status != '200 OK' then log.time end)/ COUNT (log.status)::float * 100)::numeric,2) as performance FROM log GROUP BY DATE HAVING round(( COUNT (case when log.status != '200 OK' then time end)/ COUNT (log.status)::float * 100)::numeric,2) > 1;")
for row in c.fetchall():
  date, performance = row
  print("%s - %s%% error." % (date, performance))
  db.close()