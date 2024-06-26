import pandas as pd
import os
import requests
from openpyxl import load_workbook
from openpyxl.styles import Alignment

# Google Analytics configuration
measurement_id = 'G-GLBJ67ORKI'  # Replace with your actual Measurement ID
api_secret = '3yO19NeRTWF7UJZ--oCVA'  # Replace with your actual API Secret

# Function to generate a personalized message
def generate_message(owner_name, business_name, domain_name):
    message = (f"Hi {owner_name}! ,\n\n"
               f"This message is in regards to your recent business registration of {business_name}. "
               f"Your domain name, {domain_name} is currently available. "
               f"Click the following link to register your domain name.\n\n"
               f"{domain_name}\n\n"
               f"Best regards,\n"
               f"Blabor Team")
    return message

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
    return response.status_code, response.text

# Load the provided Excel file
file_path = 'DATA/Leads.xlsx'
print("Loading Excel file...")
data = pd.read_excel(file_path)
print("Excel file loaded successfully.")

# Generate messages and track data
events = []
total_successful_events = 0
total_failed_events = 0

for index, row in data.iterrows():
    owner_name = row['Owner/Manager']
    business_name = row['Business Name']
    phone_number = row['Phone Number']
    domain_name = f"https://www.secureserver.net/products/domain-registration/find/?domainToCheck={business_name.replace(' ', '+')}&plid=487856&itc=slp_rstore"

    message = generate_message(owner_name, business_name, domain_name)
    client_id = f"client_{index}"

    # Track message generated event in Google Analytics
    event_name = "message_generated"
    params = {
        "owner_name": owner_name,
        "business_name": business_name,
        "phone_number": phone_number,
        "hyperlink": domain_name
    }

    status_code, response_text = send_event_to_ga(client_id, event_name, params)
    if status_code == 204:
        total_successful_events += 1
    else:
        total_failed_events += 1

    # Simulate link click event
    event_name = "link_click"
    params = {
        "owner_name": owner_name,
        "business_name": business_name,
        "phone_number": phone_number,
        "hyperlink": domain_name
    }

    status_code, response_text = send_event_to_ga(client_id, event_name, params)
    if status_code == 204:
        total_successful_events += 1
    else:
        total_failed_events += 1

    events.append(params)

# Ensure the output directory exists
output_dir = 'Output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Save the data with messages and events to a new Excel file
output_file_path = os.path.join(output_dir, 'output_with_messages.xlsx')
data['Message'] = data.apply(lambda row: generate_message(row['Owner/Manager'], row['Business Name'], f"https://www.secureserver.net/products/domain-registration/find/?domainToCheck={row['Business Name'].replace(' ', '+')}&plid=487856&itc=slp_rstore"), axis=1)
data['Event'] = events
data.to_excel(output_file_path, index=False)

# Adjust column widths and text wrapping
print("Adjusting column widths and text wrapping...")
wb = load_workbook(output_file_path)
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

wb.save(output_file_path)

print(f"Total successful events: {total_successful_events // 2}")
print(f"Total failed events: {total_failed_events // 2}")
