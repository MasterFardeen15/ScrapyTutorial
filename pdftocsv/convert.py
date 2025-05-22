import pdfplumber
import csv
import re
import os

import logging
logging.getLogger("pdfminer").setLevel(logging.ERROR)

pdf_file = "parts.pdf"
csv_file = "parts_output.csv"

pdf_path = os.path.abspath(pdf_file).replace("\\", "/")
pdf_link_prefix = f"file:///{pdf_path}#page="

# Initialize CSV output
output_rows = []
header = ["Part Number", "Relevant Part Description", "Part Quantity", "Category", "Sub-Category", "Parts Manual Page Link"]
num = 0
category_dict = {}



with pdfplumber.open("parts.pdf") as pdf:
    for page in pdf.pages:
        if(num == 26): break
        num += 1
        
        text = page.extract_text()
        if not text:
            continue
        print("\n--- PAGE " + str(num) + " ---\n")

        if num == 2: # Secong page, extract main categories
            lines = text.split('\n')
            lines = lines[4:11]  # Adjust based on actual content
            for line in lines:
                line = line.strip()
                parts = line.split(maxsplit=1)
                if len(parts) == 2:
                    key = '0' + parts[0][0]  # e.g., "02"
                    value = parts[1]  # e.g., "POWER UNIT"
                    category_dict[key] = value
        else:
            if text.find("ITEM") != -1:
                text = text[text.find("ITEM"):]
                sectionstart = text.find("SECTION") + 8
                sectionend = text.find("Sandvik Underground Mining Flameproof Equipment")
                section = text[sectionstart:sectionend].strip()
                lines = text.split('\n')
                lines = text.replace(', ', ' | ').split('\n')

                for line in lines:
                    line = line.strip()
                                        
                    part_no, description, quantity, category, subcategory, page_link = "", "", "", "", "", ""                    
                    if section[3:5] == "00": # Main category page extract subcategories
                        match = re.match(r"^([\S]+)\s+(\d{2}-\d{2})\s+(.*)", line)
                        if match:
                            part_no = match.group(1)
                            page_code = match.group(2)
                            description = match.group(3)
                            category = category_dict[section[0:2]]
                            subcategory = ""
                            quantity = ""
                            
                            category_dict[page_code] = description                            
                            # Generate a pseudo page-link (modify as needed)
                            # page_link = f"parts_manual_pg_{page_code}.pdf"
                            page_link = f"{pdf_link_prefix}{num}"
                            
                            # Create Excel-friendly HYPERLINK formula
                            # page_display_name = f"Page {num}"
                            # page_link = f'=HYPERLINK("{pdf_link_prefix}#page={num}", "{page_display_name}")'


                            output_rows.append([
                                part_no,
                                description,
                                quantity,
                                category,
                                subcategory,
                                page_link
                            ])
                    else:
                        # EX: 1 A2U220-211044-2 02-01-04 1 ENGINE, MODIFIED, CAT 3126TA
                        match = re.match(r"^(\d{1,2})\s+([A-Z0-9\-]{4,})\s+(\d{2}(?:-\d{2}){1,})?\s*(\d{1,4})?\s*(.*)?", line)

                        if match:
                            part_no = match.group(2)
                            page_code = match.group(3)
                            if(match.group(3) == None):
                                page_code = section
                            quantity = match.group(4)
                            description = match.group(5)
                            category = category_dict[section[0:2]] 
                            subcategory = category_dict[section[0:5]] if section[0:5] in category_dict else ""
                            
                            # Generate a pseudo page-link (modify as needed)
                            # page_link = f"parts_manual_pg_{page_code}.pdf"
                            page_link = f"{pdf_link_prefix}{num}"
                            
                            # Create Excel-friendly HYPERLINK formula
                            # page_display_name = f"Page {num}"
                            # page_link = f'=HYPERLINK("{pdf_link_prefix}#page={num}", "{page_display_name}")'

                            output_rows.append([
                                part_no,
                                description,
                                quantity,
                                category,
                                subcategory,
                                page_link
                            ])                                                    

# # Write to CSV
csv_file = "parts_output.csv"
with open(csv_file, "w", newline="", encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(output_rows)

print(f"✅ CSV file created: {csv_file}")


