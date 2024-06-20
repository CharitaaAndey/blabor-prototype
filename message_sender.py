import pandas as pd

# Function to generate a personalized, witty, and congratulatory message with a hyperlink
def generate_witty_message(owner_name, business_name):
    hyperlink = f"http://domainregistration.com/register?business={business_name.replace(' ', '%20')}"
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

# Save the data with messages to a new Excel file
output_file_path = 'output/output_with_messages.xlsx'
data.to_excel(output_file_path, index=False)
