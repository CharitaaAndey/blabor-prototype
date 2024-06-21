import pandas as pd
import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

# Twilio configuration
account_sid = 'AC37222357fd3567ea96149c9ee23c00e0'
auth_token = '92ec2b4cd1fd9a3a828f1a3a7b7eb0c1'
twilio_phone_number = '+18442422961'

# Initialize the Twilio client
client = Client(account_sid, auth_token)

# Function to generate a personalized, witty, and congratulatory message with a hyperlink
def generate_witty_message(owner_name, business_name):
    # Format the business name for the URL
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

# Function to send SMS using Twilio
def send_sms(phone_number, message):
    try:
        message = client.messages.create(
            body=message,
            from_=twilio_phone_number,
            to=phone_number
        )
        print(f"Message sent to {phone_number}: SID {message.sid}")
    except TwilioRestException as e:
        if e.code == 21408:
            print(f"Failed to send message to {phone_number}: Permission to send an SMS has not been enabled for this region.")
        else:
            print(f"Failed to send message to {phone_number}: {str(e)}")

# Load the provided Excel file
file_path = 'DATA/Leads.xlsx'  # Update this path if necessary
data = pd.read_excel(file_path)

# Generate witty messages for each row and send SMS
for index, row in data.iterrows():
    owner_name = row['Owner/Manager']
    business_name = row['Business Name']
    phone_number = row['Phone Number']
    
    message = generate_witty_message(owner_name, business_name)
    
    # Send SMS
    send_sms(phone_number, message)

# Ensure the output directory exists
output_dir = 'Output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Save the data with messages to a new Excel file
output_file_path = os.path.join(output_dir, 'output_with_messages.xlsx')
data['WittyMessage'] = data.apply(lambda row: generate_witty_message(row['Owner/Manager'], row['Business Name']), axis=1)
data.to_excel(output_file_path, index=False)
