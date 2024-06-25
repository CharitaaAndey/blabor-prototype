import pandas as pd
import os
from openpyxl import load_workbook
from openpyxl.styles import Alignment

# Function to generate follow-up message for those who opened the link but didn't register
def generate_follow_up_message_opened(owner_name, business_name):
    message = (f"Hi {owner_name},\n\n"
               f"We noticed you took the first step by clicking on the link for {business_name} 🌟, but haven't registered yet.\n\n"
               f"Let's make your business shine online! ✨\n\n"
               f"Click here to complete your domain registration: [Link]\n\n"
               f"Best regards,\n"
               f"Blabor Team")
    return message

# Function to generate follow-up message for those who didn't open the link
def generate_follow_up_message_not_opened(owner_name, business_name):
    message = (f"Hi {owner_name},\n\n"
               f"We're excited about the potential of {business_name} 🌟, but noticed you haven't clicked the link yet.\n\n"
               f"Don't miss out on the chance to make your business stand out online! ✨\n\n"
               f"Click here to register your custom domain: [Link]\n\n"
               f"Best regards,\n"
               f"Blabor Team")
    return message

# Load the existing Excel file with the messages and events
file_path = 'Output/output_with_messages.xlsx'
data = pd.read_excel(file_path)

# Lists to hold the rows for each group
opened_not_registered = []
not_opened = []

# Analyze the data to determine the follow-up groups
for index, row in data.iterrows():
    if "opened" in row['Event']:
        opened_not_registered.append(row)
    else:
        not_opened.append(row)

# Create DataFrames for each group
df_opened_not_registered = pd.DataFrame(opened_not_registered)
df_not_opened = pd.DataFrame(not_opened)

# Generate follow-up messages for each group
df_opened_not_registered['FollowUpMessage'] = df_opened_not_registered.apply(
    lambda row: generate_follow_up_message_opened(row['Owner/Manager'], row['Business Name']), axis=1)
df_not_opened['FollowUpMessage'] = df_not_opened.apply(
    lambda row: generate_follow_up_message_not_opened(row['Owner/Manager'], row['Business Name']), axis=1)

# Ensure the output directory exists
output_dir = 'Output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Save the new data with follow-up messages to new Excel files
output_file_opened_not_registered = os.path.join(output_dir, 'follow_up_opened_not_registered.xlsx')
output_file_not_opened = os.path.join(output_dir, 'follow_up_not_opened.xlsx')

df_opened_not_registered.to_excel(output_file_opened_not_registered, index=False)
df_not_opened.to_excel(output_file_not_opened, index=False)

# Format the Excel files to wrap text and adjust column widths
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
        adjusted_width = min((max_length + 2), 50)  # Set max width
        ws.column_dimensions[column].width = adjusted_width
        for cell in col:
            cell.alignment = Alignment(wrap_text=True)
    
    wb.save(file_path)

# Format the generated Excel files
format_excel_file(output_file_opened_not_registered)
format_excel_file(output_file_not_opened)

print("Follow-up messages generated and saved successfully.")
