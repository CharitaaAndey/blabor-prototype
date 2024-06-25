import pandas as pd
import os
from openpyxl import load_workbook
from openpyxl.styles import Alignment

# Function to generate a new domain link
def generate_new_domain_link(business_name, index):
    formatted_business_name = business_name.replace(' ', '+')
    new_hyperlink = f"https://www.secureserver.net/products/domain-registration/find/?domainToCheck={formatted_business_name}&plid=487856&itc=slp_rstore&uid={index}"
    return new_hyperlink

# Function to generate a follow-up message for those who opened the link but didn't register
def generate_follow_up_message_opened(owner_name, business_name, index):
    new_hyperlink = generate_new_domain_link(business_name, index)
    message = (f"Hi {owner_name},\n\n"
               f"We noticed you took the first step by clicking on the link for {business_name}, but you haven't completed your domain registration yet. 🌟\n\n"
               f"Let's make it official and secure your domain today!\n\n"
               f"Click here to register your custom domain: {new_hyperlink}\n\n"
               f"Best regards,\n"
               f"Blabor Team")
    return message, new_hyperlink

# Function to generate a follow-up message for those who didn't open the link
def generate_follow_up_message_not_opened(owner_name, business_name, index):
    new_hyperlink = generate_new_domain_link(business_name, index)
    message = (f"Hi {owner_name},\n\n"
               f"We missed you! It looks like you haven't checked the link we sent for {business_name}. 🌟\n\n"
               f"Don't miss out on registering your custom domain. Click the link and make your business shine!\n\n"
               f"Click here to register your custom domain: {new_hyperlink}\n\n"
               f"Best regards,\n"
               f"Blabor Team")
    return message, new_hyperlink

# Load the output Excel file from message_sender.py
file_path = 'Output/output_with_messages.xlsx'
data = pd.read_excel(file_path)

# Separate the data into those who opened the link and those who didn't
opened_links = data[data['Event'] == 'Opened']
not_opened_links = data[data['Event'] == 'Not Opened']

# Generate follow-up messages
if not opened_links.empty:
    opened_links['FollowUpMessage'], opened_links['NewHyperlink'] = zip(*opened_links.apply(
        lambda row: generate_follow_up_message_opened(row['Owner/Manager'], row['Business Name'], row.name), axis=1))

if not not_opened_links.empty:
    not_opened_links['FollowUpMessage'], not_opened_links['NewHyperlink'] = zip(*not_opened_links.apply(
        lambda row: generate_follow_up_message_not_opened(row['Owner/Manager'], row['Business Name'], row.name), axis=1))

# Ensure the output directory exists
output_dir = 'Output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Save the follow-up messages to new Excel files
output_file_path_opened = os.path.join(output_dir, 'follow_up_opened.xlsx')
output_file_path_not_opened = os.path.join(output_dir, 'follow_up_not_opened.xlsx')

if not opened_links.empty:
    opened_links.to_excel(output_file_path_opened, index=False)
if not not_opened_links.empty:
    not_opened_links.to_excel(output_file_path_not_opened, index=False)

# Adjust column widths and text wrapping for follow-up files
def adjust_excel_formatting(file_path):
    wb = load_workbook(file_path)
    ws = wb.active

    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter  # Get the column name
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column].width = adjusted_width
        for cell in col:
            cell.alignment = Alignment(wrap_text=True)

    wb.save(file_path)

if not opened_links.empty:
    adjust_excel_formatting(output_file_path_opened)
if not not_opened_links.empty:
    adjust_excel_formatting(output_file_path_not_opened)

print("Follow-up messages generated and saved.")
