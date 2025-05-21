import pdfplumber
import csv
import re

import logging
logging.getLogger("pdfminer").setLevel(logging.ERROR)


# Initialize CSV output
output_rows = []
header = ["Part Number", "Relevant Part Description", "Part Quantity", "Category", "Sub-Category", "Parts Manual Page Link"]

current_category = ""
current_subcategory = ""
num = 1


with pdfplumber.open("parts.pdf") as pdf:
    for page in pdf.pages:
        if(num == 4): break
        text = page.extract_text()
        if not text:
            continue
        lines = text.split('\n')

        print("PAGE " + str(num) + "\n")
        
        # Assume lines is a list of strings like:
        # ["2-00 POWER UNIT", "3-00 DRIVE TRAIN", ...]
        category_dict = {}

        if num == 2:
            lines = lines[4:11]  # Adjust based on actual content
            for line in lines:
                line = line.strip()
                parts = line.split(maxsplit=1)
                if len(parts) == 2:
                    key = '0' + parts[0][0]  # e.g., "02"
                    value = parts[1]  # e.g., "POWER UNIT"
                    category_dict[key] = value
            # print(category_dict)
        else:
            for line in lines:
                line = line.strip()
                # print(line)
        num += 1

