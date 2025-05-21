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
category_dict = {}




with pdfplumber.open("parts.pdf") as pdf:
    for page in pdf.pages:
        if(num == 26): break
        text = page.extract_text()
        if not text:
            continue
        # lines = text.split('\n')

        print("\n--- PAGE " + str(num) + " ---\n")
        
        # Assume lines is a list of strings like:
        # ["2-00 POWER UNIT", "3-00 DRIVE TRAIN", ...]

        if num == 2:
            lines = text.split('\n')
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
            if text.find("ITEM") != -1:
                text = text[text.find("ITEM"):]
                sectionstart = text.find("SECTION") + 8
                sectionend = text.find("Sandvik Underground Mining Flameproof Equipment")
                section = text[sectionstart:sectionend].strip()
                # print(section)
                print(len(section))
                
                lines = text.split('\n')
                lines = text.replace(', ', ' | ').split('\n')

                for line in lines:
                    line = line.strip()
                    # print(line)
                    
                    part_no, description, qty, current_category, current_subcategory, page_link = "", "", "", "", "", ""                    
                    if section[3:5] == "00":
                        # Match part line: PART_NO PAGE QTY? DESCRIPTION
                        # match = re.match(r"^([A-Z0-9\-]+)\s+(\d{2}-\d{2})\s+(.*)", line)
                        match = re.match(r"^([\S]+)\s+(\d{2}-\d{2})\s+(.*)", line)
                        if match:
                            part_no = match.group(1)
                            page_code = match.group(2)
                            description = match.group(3)
                            current_category = category_dict[section[0:2]]
                            current_subcategory = ""
                            qty = ""
                            
                            category_dict[page_code] = description                            
                            # Generate a pseudo page-link (modify as needed)
                            page_link = f"parts_manual_pg_{page_code}.pdf"

                            output_rows.append([
                                part_no,
                                description,
                                qty,
                                current_category,
                                current_subcategory,
                                page_link
                            ])
                    else:
                        # 1 A2U220-211044-2 02-01-04 1 ENGINE, MODIFIED, CAT 3126TA

                        # match = re.match(r"^(\d\d*)\s+([\S]*)\s*([\d\-]*)\s+([\d]*)\s+(.*)", line)
                        # match = re.match(r"^(\d{1,2})?\s*([\S]+)?\s*([\d\-]+)?\s*([\d]*)?\s*(.*)?", line)
                        # match = re.match(r"^(\d{1,2})\s+([\S]+)\s+([\d\-]*)?\s*([\d]*)?\s*(.*)?", line)
                        # match = re.match(r"^(\d{1,2})\s+([A-Z0-9\-]{4,})\s+([\d\-]*)?\s*([\d]*)?\s*(.*)?", line)
                        match = re.match(r"^(\d{1,2})\s+([A-Z0-9\-]{4,})\s+(\d{2}(?:-\d{2}){1,})?\s*(\d{1,4})?\s*(.*)?", line)

                        if match:
                            part_no = match.group(2)
                            page_code = match.group(3)
                            if(match.group(3) == None):
                                page_code = section
                            qty = match.group(4)
                            description = match.group(5)
                            current_category = category_dict[section[0:2]] 
                            current_subcategory = category_dict[section[0:5]] if section[0:5] in category_dict else ""
                            
                            print(f"Part No: {part_no}, Page Code: {page_code}, Description: {description}, Qty: {qty}")
                            # category_dict[page_code] = description                            
                            # Generate a pseudo page-link (modify as needed)
                            page_link = f"parts_manual_pg_{page_code}.pdf"

                            output_rows.append([
                                part_no,
                                description,
                                qty,
                                current_category,
                                current_subcategory,
                                page_link
                            ])                        
                        # print(section)
                            
                            
        num += 1

# print(category_dict)

# # Write to CSV
csv_file = "parts_output.csv"
with open(csv_file, "w", newline="", encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(output_rows)

print(f"✅ CSV file created: {csv_file}")

# with open('cisco.csv', 'w') as csv_file:
#     writer = csv.writer(csv_file)
#     writer.writerows(table)

