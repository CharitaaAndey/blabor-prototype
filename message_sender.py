import pandas as pd
import os
import plivo
from plivo.exceptions import PlivoRestError

# Plivo configuration
auth_id = 'your_auth_id'
auth_token = 'your_auth_token'
plivo_phone_number = 'your_plivo_phone_number'

# Initialize the Plivo client
client = plivo.RestClient(auth_id, auth_token)

# Function to generate a personalized, witty, and congratulatory message with a hyperlink
def generate_message(owner_name, business_name):
    formatted_business_name = business_name.replace(' ', '+')
    hyperlink = f"https://www.secureserver.net/products/domain-registration/find/?domainToCheck={formatted_business_name}&plid=487856&itc=slp_rstore"
    message = (f"Hi {owner_name},\n\n"
               f"🎉 Congratulations on taking the first step towards an even brighter future for {business_name}! 🎉\n\n"
               f"Imagine your business with its very own domain. It's time to make it official and stand out online! 🌟\n\n"
               f"Click here to register your custom domain: {hyperlink}\n\n"
               f"Don't miss out on this chance to shine! ✨\n\n"
               f"Best regards,\n"
               f"Blabor Team")
    return message

# Function to send SMS using Plivo
def send_sms(phone_number, message):
    try:
        response = client.messages.create(
            src=plivo_phone_number,
            dst=phone_number,
            text=message
        )
        print(f"Message sent to {phone_number}: Message UUID {response.message_uuid}")
    except PlivoRestError as e:
        print(f"Failed to send message to {phone_number}: {str(e)}")

# Load the provided Excel file
file_path = 'DATA/Leads.xlsx'
data = pd.read_excel(file_path)

# Generate messages for each row and send SMS
for index, row in data.iterrows():
    owner_name = row['Owner/Manager']
    business_name = row['Business Name']
    phone_number = row['Phone Number']
    
    message = generate_message(owner_name, business_name)
    
    # Send SMS
    send_sms(phone_number, message)

# Ensure the output directory exists
output_dir = 'Output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Save the data with messages to a new Excel file
output_file_path = os.path.join(output_dir, 'output_with_messages.xlsx')
data['Message'] = data.apply(lambda row: generate_message(row['Owner/Manager'], row['Business Name']), axis=1)
data.to_excel(output_file_path, index=False)
