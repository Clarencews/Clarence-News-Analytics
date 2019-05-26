Udacity Project 1 : News Analytics Report

Author : Clarence Stone

Objective: Create a program that displays the answers to the questions below fro a provided database.

1. What are the most popular three articles of all time? Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.

2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.

3. On which days did more than 1% of requests lead to errors? The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser. (Refer to this lesson for more information about the idea of HTTP status codes.)

Files: 3 total files required for this project.

1. news_views.py - Please run after initializing databse, required for reporting.

2. newsdata.py - creates reports to meet the objectives from above.

3. README.md - this file.

Setup via Vagrant Linux Environment 

1. SSH into Vagrant and navigate into parent folder of newsdata database 

2. Run psql with the command `psql -d news -f newsdata.py` to load data into DB

3. In PSQL create views from new_views.py

4. Run python script newsdata.py

HOW IT WORKS

news_views.py has two views that tie in all three tables of the news DB. 
1. create article_views takes a total count of views by matching the path from the log table to the url path, extra code to avoid 404 and omit "/" (homepage) is also included.
2. create popular_author takes the total counts of views from the previous view(article_views) and joins them based on the author name to sort articles by author popularity.

You must create both of these views befor proceeding.

newsdata.py 
1. imports psycopg2 (for DB connection) and datetime (for date clean up)
2. class font_styles establsihes font styles for python print command used in project
3. top 3 articles are displayed by joining article_views with articles and matching up slugs. Limit 3 because the project only wants top 3 articles.
4. top authors of all time are displayed by joining the popular_author view with the author table by matching v.author and a.id.
5. request errors are displayed with one large sql query from only the log table. It takes the date, divides 404 status over total status and creates a percentage. Then sorts it from highest to lowest and uses the "HAVING" statement to ony show error rates above 1%.


SQL code for Views

Article Views Ranked - gets a total count of views based on joining slug from article table and path from log table.
CREATE article_views AS 
SELECT substring(path,position('e/' IN path)+2) AS slug, 
		count(*) AS views 
	FROM log 
	WHERE status = '200 OK' 
	AND PATH != '/' 
	GROUP BY slug 
	ORDER BY views DESC;

Popular Authors Ranked by Article View - get total count of views from each authoer by ID by joining article_views table from above with author table
CREATE VIEW popular_author AS 
SELECT author, sum(views) AS sum 
	FROM articles AS a, article_views AS v 
	WHERE a.slug = v.slug 
	GROUP BY author 
	ORDER BY sum DESC;


