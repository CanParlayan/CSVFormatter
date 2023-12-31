import csv

csv_file_path = 'comptech_no_duplicates.csv'
new_csv_file_path = 'comptech_phone.csv'

# Function to format phone numbers
def format_phone_number(phone):
    # Remove '+' and whitespace
    phone = phone.replace('+90', '').replace(' ', '')

    # Add '0' if the number starts with '5'
    if phone.startswith('5'):
        phone = '0' + phone

    return phone

# Create a new list to store the reformatted data
new_data = []

# Read the original CSV file
with open(csv_file_path, 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file, delimiter=',')

    # Skip the header row
    next(csv_reader)

    for veri_parcalari in csv_reader:
        ad_soyad = "Comptech " + veri_parcalari[0]# Format the name
        telefon = format_phone_number(veri_parcalari[3])  # Format the phone number

        # Create a new record in the desired format
        new_record = [
            ad_soyad,  # Name
            'Comptech',  # Group Membership
            'Mobile',  # Phone 1 - Type
            telefon  # Phone 1 - Value
        ]

        # Append the new record to the list
        new_data.append(new_record)

# Write the reformatted data to a new CSV file
with open(new_csv_file_path, 'w', newline='', encoding='utf-8') as new_csv_file:
    csv_writer = csv.writer(new_csv_file, delimiter=',')
    # Write the header row
    csv_writer.writerow([
        'Name',
        'Group Membership',
        'Phone 1 - Type',
        'Phone 1 - Value'
    ])

    # Write the reformatted data
    csv_writer.writerows(new_data)

print(f"CSV data has been reformatted and saved to '{new_csv_file_path}'.")