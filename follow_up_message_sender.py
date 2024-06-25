import pandas as pd

# Function to generate a follow-up message for those who opened the link but didn't register
def generate_follow_up_message_opened(owner_name, business_name):
    message = (f"Hi {owner_name},\n\n"
               f"We noticed you took the first step by clicking on the link for {business_name}, but you haven't completed your domain registration yet. 🌟\n\n"
               f"Let's make it official and secure your domain today!\n\n"
               f"Best regards,\n"
               f"Blabor Team")
    return message

# Function to generate a follow-up message for those who didn't open the link
def generate_follow_up_message_not_opened(owner_name, business_name):
    message = (f"Hi {owner_name},\n\n"
               f"We missed you! It looks like you haven't checked the link we sent for {business_name}. 🌟\n\n"
               f"Don't miss out on registering your custom domain. Click the link and make your business shine!\n\n"
               f"Best regards,\n"
               f"Blabor Team")
    return message

# Load the output Excel file from message_sender.py
file_path = 'Output/output_with_messages.xlsx'
data = pd.read_excel(file_path)

# Separate the data into those who opened the link and those who didn't
opened_links = []
not_opened_links = []

for index, row in data.iterrows():
    if row['Event']['link_click'] == 'Opened':
        opened_links.append(row)
    else:
        not_opened_links.append(row)

df_opened = pd.DataFrame(opened_links)
df_not_opened = pd.DataFrame(not_opened_links)

# Generate follow-up messages
if not df_opened.empty:
    df_opened['FollowUpMessage'] = df_opened.apply(
        lambda row: generate_follow_up_message_opened(row['Owner/Manager'], row['Business Name']), axis=1)

if not df_not_opened.empty:
    df_not_opened['FollowUpMessage'] = df_not_opened.apply(
        lambda row: generate_follow_up_message_not_opened(row['Owner/Manager'], row['Business Name']), axis=1)

# Save the follow-up messages to new Excel files
output_dir = 'Output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_file_path_opened = os.path.join(output_dir, 'follow_up_opened.xlsx')
output_file_path_not_opened = os.path.join(output_dir, 'follow_up_not_opened.xlsx')

if not df_opened.empty:
    df_opened.to_excel(output_file_path_opened, index=False)
if not df_not_opened.empty:
    df_not_opened.to_excel(output_file_path_not_opened, index=False)

print("Follow-up messages generated and saved.")
