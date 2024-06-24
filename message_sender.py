import pandas as pd
import os
import requests
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment

# Google Analytics configuration
measurement_id = 'G-GLBJ67ORKI'  # Replace with your actual Measurement ID
api_secret = '3yO19NeRTWF7UJZ--oCVA'  # Replace with your actual API Secret

# Bitly configuration
bitly_access_token = 'YOUR_BITLY_ACCESS_TOKEN'  # Replace with your Bitly access token

# Function to shorten a URL using Bitly
def shorten_url(long_url):
    headers = {
        'Authorization': f'Bearer {bitly_access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'long_url': long_url
    }
    response = requests.post('https://api-ssl.bitly.com/v4/shorten', json=data, headers=headers)
    if response.status_code == 200:
        return response.json().get('link')
    else:
        print(f"Failed to shorten URL: {response.text}")
        return long_url  # Return the original URL if shortening fails

# Function to generate a personalized, witty, and congratulatory message with a shortened hyperlink
def generate_message(owner_name, business_name):
    formatted_business_name = business_name.replace(' ', '+')
    long_url = f"https://www.secureserver.net/products/domain-registration/find/?domainToCheck={formatted_business_name}&plid=487856&itc=slp_rstore"
    short_url = shorten_url(long_url)
    message = (f"Hi {owner_name},\n\n"
               f"🎉 Congratulations on taking the first step towards an even brighter future for {business_name}! 🎉\n\n"
               f"Imagine your business with its very own domain. It's time to make it official and stand out online! 🌟\n\n"
               f"Click here to register your custom domain: {short_url}\n\n"
               f"Don't miss out on this chance to shine! ✨\n\n"
               f"Best regards,\n"
               f"Blabor Team")
    return message, short_url

# Function to send event data to Google Analytics
def send_event_to_ga(client_id, event_name, params):
    url = f"https://www.google-analytics.com/mp/collect?measurement_id={measurement_id}&api_secret={api_secret}"
    payload = {
        "client_id": client_id,
        "events": [{
            "name": event_name,
            "params": params
        }]
    }
    response = requests.post(url, json=payload)
    print(f"Response from GA for event '{event_name}': Status {response.status_code}, Text {response.text}")
    return response.status_code, response.text

# Load the provided Excel file
file_path = 'DATA/Leads.xlsx'
data = pd.read_excel(file_path)

# Generate messages and track data
events = []
for index, row in data.iterrows():
    owner_name = row['Owner/Manager']
    business_name = row['Business Name']
    phone_number = row['Phone Number']
    
    message, short_url = generate_message(owner_name, business_name)
    client_id = f"client_{index}"
    
    # Track message generated event in Google Analytics
    event_name = "message_generated"
    params = {
        "owner_name": owner_name,
        "business_name": business_name,
        "phone_number": phone_number,
        "hyperlink": short_url
    }
    
    status_code, response_text = send_event_to_ga(client_id, event_name, params)
    if status_code == 204:
        print(f"Event for {owner_name} tracked successfully.")
    else:
        print(f"Failed to track event for {owner_name}: {response_text}")
    
    # Simulate link click event
    event_name = "link_click"
    params = {
        "owner_name": owner_name,
        "business_name": business_name,
        "phone_number": phone_number,
        "hyperlink": short_url
    }
    
    status_code, response_text = send_event_to_ga(client_id, event_name, params)
    if status_code == 204:
        print(f"Link click for {owner_name} tracked successfully.")
    else:
        print(f"Failed to track link click for {owner_name}: {response_text}")
    
    events.append(params)

# Ensure the output directory exists
output_dir = 'Output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Save the data with messages and events to a new Excel file
output_file_path = os.path.join(output_dir, 'output_with_messages.xlsx')
data['Message'] = data.apply(lambda row: generate_message(row['Owner/Manager'], row['Business Name'])[0], axis=1)
data['Event'] = events
data.to_excel(output_file_path, index=False)

# Format the Excel file to wrap text and adjust column widths
def format_excel_file(file_path):
    wb = load_workbook(file_path)
    ws = wb.active
    
    # Adjust column widths and wrap text
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

# Format the generated Excel file
format_excel_file(output_file_path)
