# Article Views Ranked - gets a total count of views based on joining slug from article table and path from log table.
CREATE article_views AS 
SELECT substring(path,position('e/' IN path)+2) AS slug, 
		count(*) AS views 
	FROM log 
	WHERE status = '200 OK' 
	AND PATH != '/' 
	GROUP BY slug 
	ORDER BY views DESC;

# Authors Ranked by Article View - get total count of views from each authoer by ID by joining article_views table from above with author table
CREATE VIEW popular_author AS 
SELECT author, sum(views) AS sum 
	FROM articles AS a, article_views AS v 
	WHERE a.slug = v.slug 
	GROUP BY author 
	ORDER BY sum DESC;
