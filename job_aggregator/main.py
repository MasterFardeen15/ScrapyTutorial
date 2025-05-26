from bs4 import BeautifulSoup
import requests
import csv
import hashlib
from elasticsearch import Elasticsearch

# Setup
# Scraping job listings from LinkedIn and TimesJobs for Software Engineer positions in the USA from the past week.
csv_file = "SFE_USA_1Week_jobs.csv"
header = ["Job Title", "Company", "Location", "Link"]
output_rows = []
seen_jobs = set()  # For duplicate detection

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")


# Check Elasticsearch storage
# View sample documents in 'linkedin_jobs' index
import json
response = es.search(index="linkedin_jobs", query={"match_all": {}}, size=5) # Print first 5 documents
count = es.count(index="linkedin_jobs")["count"]
print(f"Total documents in ES: {count}")
print("\n Sample documents:")
for hit in response["hits"]["hits"]:
    print(json.dumps(hit["_source"], indent=2))


def clean_text(text):
    # Trim and normalize whitespace + replace commas (,) with bar (|) symbols
    return ' '.join(text.strip().replace(', ', ' | ').split()) if text else ""

def index_job(job_dict):
    # Store job in Elasticsearch.
    es.index(index="linkedin_jobs", document=job_dict)

def find_linkedin_jobs():
    print("Scraping LinkedIn jobs...")
    # url = "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=United%20States&geoId=103644278&f_TPR=r86400&f_WT=2&position=1&pageNum=0"
    url = "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=United%20States&geoId=103644278&f_TPR=r604800&position=1&pageNum=0"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36'
    }
    html_text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html_text, 'lxml')
    job_listings = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')

    for job in job_listings:
        title = clean_text(job.find('h3').text)
        company = clean_text(job.find('a', class_='hidden-nested-link').text if job.find('a', class_='hidden-nested-link') else 'Unknown Company')
        location = clean_text(job.find('span', class_='job-search-card__location').text)
        link = job.a['href']
        insert_jobs(title, company, location, link)


def find_timesjobs_jobs():
    print("Scraping Times Jobs jobs...")
    url = "https://m.timesjobs.com/mobile/jobs-search-result.html?txtKeywords=Software+Engineer%2C&cboWorkExp1=-1&txtLocation=United+States"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36'
    }
    html_text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html_text, 'lxml')
    job_listings = soup.find_all('div', class_= 'srp-job-bx')

    for index, job in enumerate(job_listings):
        posted_date = clean_text(job.find('span', class_='posting-time').text).split()[0]
        if int(posted_date) < 8:
            title = clean_text(job.find('h3').text)
            company = clean_text(job.find('span', class_='srp-comp-name').text)
            location = clean_text(job.find('div', class_='srp-loc').text)
            link = job.a['href']
            # print(f"Processing job {index + 1}: {title} at {company} in {location} on {posted_date}. Link: {link}")
            insert_jobs(title, company, location, link)


def insert_jobs(title, company, location, link):
    # Deduplication using a hash
    unique_key = f"{title}_{company}_{location}"
    job_hash = hashlib.md5(unique_key.encode()).hexdigest()
    if job_hash in seen_jobs:
        # print(f"Duplicate job found: {title} at {company}, skipping.")
        return
    seen_jobs.add(job_hash)

    # Store row for CSV
    output_rows.append([title, company, location, link])

    # Index into Elasticsearch
    job_doc = {
        "title": title,
        "company": company,
        "location": location,
        "link": link
    }
    index_job(job_doc)


# Run all scrapers
find_linkedin_jobs()
find_timesjobs_jobs()


# Save to CSV
with open(csv_file, "w", newline="", encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(output_rows)

print(f"Saved {len(output_rows)} jobs to {csv_file} and Elasticsearch.")
