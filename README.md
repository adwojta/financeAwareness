# financeAwareness
Praca inżynierska

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
This project is a home budget application written mostly in Python with Django Framework. 
In this appliaction user can track its expenses and incomes, describe them using categories, subcategories, tags, images and text. 
User can also track its account balance and define financial goals. Application uses Chart.js to graphically present to user datas.
This project is an application written for engineer's thesis.

## Technologies
This project is created using many frameworks and libraries:
- Django 3.2
- Selenium 4.1
- Bootstrap 5.1
- Chart.js 
- jQuery 3.6
- jQuery-ui 1.13.1
- ReportLab 3.6.6
- Psycopg2 2.9.3
- Python-dateutil 2.8.1
- Waitress 2.1.1

## Setup
Before you run this, you need to download jQuery, jQuery-ui, Bootstrap files and move them to financeAwareness/static folders. The js files to js folder, rest to css folder.

To start application you need to use run.py file. Application uses port 8080 by default. To properly serve static files it required web server such as nginx.


