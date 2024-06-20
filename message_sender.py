import pandas as pd
import os

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

# Load the provided Excel file
file_path = 'DATA/Leads.xlsx'  # Update this path if necessary
data = pd.read_excel(file_path)

# Generate witty messages for each row
data['WittyMessage'] = data.apply(lambda row: generate_witty_message(row['Owner/Manager'], row['Business Name']), axis=1)

# Ensure the output directory exists
output_dir = 'Output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Save the data with messages to a new Excel file
output_file_path = os.path.join(output_dir, 'output_with_messages.xlsx')
data.to_excel(output_file_path, index=False)
