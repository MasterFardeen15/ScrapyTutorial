import pdfplumber
import csv
import re
import os
import logging

# Suppress pdfminer warnings
logging.getLogger("pdfminer").setLevel(logging.ERROR)

# File setup
pdf_file = "parts.pdf"
csv_file = "parts_output.csv"
pdf_path = os.path.abspath(pdf_file).replace("\\", "/")
pdf_link_prefix = f"file:///{pdf_path}#page="

# CSV setup
output_rows = []
header = ["Part Number", "Relevant Part Description", "Part Quantity", "Category", "Sub-Category", "Parts Manual Page Link"]
category_dict = {}

# Extract main categories from page 2
def extract_categories(text):
    lines = text.split('\n')[4:11]  # Adjust based on format
    for line in lines:
        parts = line.strip().split(maxsplit=1)
        if len(parts) == 2:
            key = '0' + parts[0][0]  # e.g., "2-00" → "02"
            category_dict[key] = parts[1]

# Parse and store a row
def store_row(part_no, description, quantity, category, subcategory, page_num):
    # page_link = f'=HYPERLINK("{pdf_link_prefix}{page_num}", "Page {page_num}")'
    page_link = f"{pdf_link_prefix}{page_num}"
    output_rows.append([part_no, description, quantity, category, subcategory, page_link])

# Extract from main category index pages (e.g., 02-00)
def extract_subcategories(line, section_code, page_num):
    match = re.match(r"^([\S]+)\s+(\d{2}-\d{2})\s+(.*)", line)
    if match:
        part_no = match.group(1)
        page_code = match.group(2)
        description = match.group(3)
        category = category_dict.get(section_code[0:2], "")
        category_dict[page_code] = description  # Save as subcategory
        store_row(part_no, description, "", category, "", page_num)

# Extract from standard part list lines
def extract_item(line, section_code, page_num):
    match = re.match(r"^(\d{1,2})\s+([A-Z0-9\-]{4,})\s+(\d{2}(?:-\d{2}){1,})?\s*(\d{1,4})?\s*(.*)?", line)
    if match:
        part_no = match.group(2)
        # page_code = match.group(3) or section_code
        quantity = match.group(4) or ""
        description = (match.group(5) or "").strip()
        category = category_dict.get(section_code[0:2], "")
        subcategory = category_dict.get(section_code[0:5], "")
        store_row(part_no, description, quantity, category, subcategory, page_num)

# Start processing PDF
with pdfplumber.open(pdf_file) as pdf:
    for page_num, page in enumerate(pdf.pages, start=1):
        # if page_num > 26:
        #     break

        text = page.extract_text()
        if not text:
            continue
        # print(f"\n--- PAGE {page_num} ---\n")

        # Page 2 = main category index
        if page_num == 2:
            extract_categories(text)
            continue

        # Only process pages with part listings
        if "ITEM" not in text:
            continue

        section_start = text.find("SECTION") + 8
        section_end = text.find("Sandvik Underground Mining Flameproof Equipment")
        section_code = text[section_start:section_end].strip()

        # Clean up and standardize lines
        lines = text[text.find("ITEM"):].replace(', ', ' | ').split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue
            if section_code[3:5] == "00":
                extract_subcategories(line, section_code, page_num)
            else:
                extract_item(line, section_code, page_num)

# Write CSV
with open(csv_file, "w", newline="", encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(output_rows)

# print(f"CSV file created: {csv_file}")
