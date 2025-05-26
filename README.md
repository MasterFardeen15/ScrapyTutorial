# ScrapyTutorial: Web & Document Scraping Portfolio
This repository showcases a collection of web and document scraping projects developed using Python. Each project demonstrates proficiency in data extraction, processing, and storage techniques, employing tools such as Scrapy, BeautifulSoup, pdfplumber, RegEx, SQLite3, MySQL, MongoDB, and Elasticsearch.

## Quote Tutorial
### Description:
A foundational project that scrapes quotes from Quotes to Scrape, serving as an introduction to Scrapy's capabilities.
### Skills & Tools:
+ Python
+ Scrapy
+ HTML parsing & Extracting Data with CSS Selectors and XPATH
+ Data export in JSON, CSV, & XML formats
+ Storing in Databases: SQLite3, MySQL, MongoDB
### Key Features:
+ Implements a basic Scrapy spider to navigate and extract data.
+ Demonstrates logging into a website with user and password.
+ Demonstrates handling of pagination and data storage.
+ Demonstrates Web Crawling & Following Links.
+ Bypassing Restrictions using User-Agent and Proxies.

## Amazon Electronics
### Description:
A scraper designed to extract the best selling Amazon Electronics, focusing on product details and ratings.
### Skills & Tools:
+ Python
+ Scrapy
+ HTML parsing & CSS Extractors
+ Data export in CSV format
### Key Features:
+ Scrapes product title, rank, price, number of ratings, rating score out of 5, and image link.
+ Handles pagination to ensure comprehensive data extraction.
+ Processes and structures porduct and rating data into CSV export for analysis.

## PDF to CSV
### Description:
A scraper that converts structured text from a technical PDF into a CSV file, facilitating easier data manipulation and analysis.
### Skills & Tools:
+ Python
+ pdfplumber
+ RegEx
### Key Features:
+ Parsed technical documents containing part catalogs and exploded views.
+ Regex-Based Data Extraction.
+ Section Mapping and Hierarchical Categorization.
+ Cleans and structures data into CSV format.
+ Dynamic Link Generation.
+ Handles multiple pages in PDF and merges data as needed.

## Job Aggregator
### Description:
A scraper that collects job listings from LinkedIn, storing them in both CSV files and Elasticsearch for advanced search capabilities.
### Skills & Tools:
+ Python
+ BeautifulSoup
+ Requests
+ Elasticsearch
### Key Features:
+ Scrapes job titles, companies, locations, and links.
+ Stores data in Elasticsearch for efficient querying.
+ Exports data to CSV for offline analysis.
+ Demonstrates integration between web scraping and search engine indexing.
