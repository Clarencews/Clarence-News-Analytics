#Udacity Project 1 : News Analytics Report

Author : Clarence Stone

##Objective: Create a program that displays the answers to the questions below fro a provided database.

1. What are the most popular three articles of all time? Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.

2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.

3. On which days did more than 1% of requests lead to errors? The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser. (Refer to this lesson for more information about the idea of HTTP status codes.)

##Required Files - 3 included - SQL db needs to be downloaded seperately

1. news_views.py - Please run after initializing databse, required for reporting.

2. newsdata.py - creates reports to meet the objectives from above.

3. README.md - this file.

4. newsdata.sql - download it from https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip and place it into the root folder of this repo. 
There is a git .ignore file included that will exclude the db file from being uploaded during commits.

##Setup via Vagrant Linux Environment 

1. Follow instructions below from udemy on how to set up a vagrant and virtual box.
```
Install VirtualBox
VirtualBox is the software that actually runs the virtual machine. You can download it from virtualbox.org, here. Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it; Vagrant will do that.

Ubuntu users: If you are running Ubuntu 14.04, install VirtualBox using the Ubuntu Software Center instead. Due to a reported bug, installing VirtualBox from the site may uninstall other software you need.

Install Vagrant
Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. Download it from vagrantup.com. Install the version for your operating system.

Windows users: The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.

If Vagrant is successfully installed, you will be able to run `vagrant --version`   in your terminal to see the version number.
If Vagrant is successfully installed, you will be able to run vagrant --version
in your terminal to see the version number.
The shell prompt in your terminal may differ. Here, the $ sign is the shell prompt.

Download the VM configuration
There are a couple of different ways you can download the VM configuration.

You can download and unzip this file: FSND-Virtual-Machine.zip This will give you a directory called FSND-Virtual-Machine. It may be located inside your Downloads folder.

Note: If you are using Windows OS you will find a Time Out error, to fix it use the new Vagrant file configuration to replace you current Vagrant file.

Alternately, you can use Github to fork and clone the repository https://github.com/udacity/fullstack-nanodegree-vm.

Either way, you will end up with a new directory containing the VM files. Change to this directory in your terminal with cd. Inside, you will find another directory called vagrant. Change directory to the vagrant directory:

Navigating to the FSND-Virtual-Machine directory and listing the files in it.
Navigating to the FSND-Virtual-Machine directory and listing the files in it.
This picture was taken on a Mac, but the commands will look the same on Git Bash on Windows.

Start the virtual machine
From your terminal, inside the vagrant subdirectory, run the command vagrant up. This will cause Vagrant to download the Linux operating system and install it. This may take quite a while (many minutes) depending on how fast your Internet connection is.
```

2. SSH into Vagrant using the command `vagrant ssh` and navigate into parent folder of this repo.

3. Run psql with the command `psql -d news -f newsdata.py` to load data into DB

4. In PSQL create views from new_views.py

5. Run python script newsdata.py

##HOW IT WORKS

news_views.py has two views that tie in all three tables of the news DB. 
1. create article_views takes a total count of views by matching the path from the log table to the url path, extra code to avoid 404 and omit "/" (homepage) is also included.
2. create popular_author takes the total counts of views from the previous view(article_views) and joins them based on the author name to sort articles by author popularity.

#You must create both of these views before proceeding.

newsdata.py 
1. imports psycopg2 (for DB connection) and datetime (for date clean up)
2. class font_styles establsihes font styles for python print command used in project
3. top 3 articles are displayed by joining article_views with articles and matching up slugs. Limit 3 because the project only wants top 3 articles.
4. top authors of all time are displayed by joining the popular_author view with the author table by matching v.author and a.id.
5. request errors are displayed with one large sql query from only the log table. It takes the date, divides 404 status over total status and creates a percentage. Then sorts it from highest to lowest and uses the "HAVING" statement to ony show error rates above 1%.

##Usage, code status, and how it can help you.
- newsdata.py has two dependencies, psycopg2 and datetime. Be sure to use `pip3 install psycopg2` and `pip3 install datetime` before running the program.
- all code included has is PEP8 compliant as tested via pycodestyle use `pip3 install pycodestyle` to install it yourself.
- all sql commands and methods can be reused to apply to any database.


##SQL code for Views

```
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
```

##Lisense information
All code created in this git repo is open for use under the MIT license. See more details about this license below.
https://github.com/angular/angular.js/blob/master/LICENSE


