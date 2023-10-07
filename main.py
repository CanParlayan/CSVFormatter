import csv
import matplotlib.pyplot as plt

csv_file_path = 'comptech.csv'
new_csv_file_path = 'comptech_new.csv'
duplicate_found = False

# List to store all existing records
records_list = []

# Function to check for duplicate records (case-insensitive)
def check_for_duplicates(record, records_list):
    ad_soyad, bolum, okul_no, telefon, oneri_istek = record
    duplicate_messages = []

    for existing_record in records_list:
        # Check if the existing record has enough values
        if len(existing_record) == 5:
            existing_name, _, existing_no, existing_phone, _ = existing_record
            if okul_no.lower() == existing_no.lower() and okul_no != '-':
                duplicate_messages.append(f"Duplicate: Okul No. {okul_no} already exists.")
            elif ad_soyad.lower() == existing_name.lower():
                duplicate_messages.append(f"Duplicate: Ad-Soyad '{ad_soyad}' already exists.")
            elif telefon == existing_phone:
                duplicate_messages.append(f"Duplicate: Telefon '{telefon}' already exists.")

    return duplicate_messages

# Function to format phone numbers
def format_phone_number(phone):
    # Remove '+' and whitespace
    phone = phone.replace('+90', '').replace(' ', '')

    # Add '0' if the number starts with '5'
    if phone.startswith('5'):
        phone = '0' + phone

    # If the number is still not 10 digits, pad with '0's
    if len(phone) < 10:
        phone = phone.zfill(10)

    return phone

with open(csv_file_path, 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file, delimiter=',')

    # Skip the header row
    next(csv_reader)

    oneri_ve_istekler = []
    ad_soyad_telefon = []
    duplicate_records = []

    for veri_parcalari in csv_reader:
        ad_soyad = veri_parcalari[0]
        bolum = veri_parcalari[1]
        okul_no = veri_parcalari[2]
        telefon = format_phone_number(veri_parcalari[3])  # Format the phone number
        oneri_istek = veri_parcalari[4]

        # List to store duplicate reasons
        duplicate_reasons = check_for_duplicates((ad_soyad, bolum, okul_no, telefon, oneri_istek), records_list)

        # Check if any duplicate reasons were found
        if duplicate_reasons:
            duplicate_found = True
            duplicate_records.append((ad_soyad, telefon, bolum, okul_no, duplicate_reasons))
            print(
                f"Duplicate Record: Ad-Soyad: {ad_soyad}, Telefon: {telefon}, Bölüm: {bolum}, Okul No: {okul_no}, Reasons: {', '.join(duplicate_reasons)}")

        ad_soyad_telefon.append((ad_soyad, telefon))
        oneri_ve_istekler.append((ad_soyad, bolum, okul_no, telefon, oneri_istek))

        # Add the current record to the records_list
        records_list.append((ad_soyad, bolum, okul_no, telefon, oneri_istek))

    # Print "No duplicates found" if duplicate_found is still False after processing all records
    if not duplicate_found:
        print("No duplicates found in the entire CSV file.")

    # Write the corrected data to a new CSV file
    with open(new_csv_file_path, 'w', newline='', encoding='utf-8') as new_csv_file:
        csv_writer = csv.writer(new_csv_file, delimiter=',')

        # Write the header row
        csv_writer.writerow(['Ad-Soyad', 'Bölüm', 'Okul No', 'Telefon', 'Öneri/İstek'])

        for ad_soyad, telefon in ad_soyad_telefon:
            # Find the corresponding record in the original data
            original_record = next(
                record for record in oneri_ve_istekler if record[0] == ad_soyad and record[3] == telefon)
            ad_soyad, bolum, okul_no, telefon, oneri_istek = original_record
            # Write the corrected data to the new CSV file
            csv_writer.writerow([ad_soyad, bolum, okul_no, telefon, oneri_istek])

    # Dictionary to store the count of individuals per department
    department_counts = {}

    for ad_soyad, bolum, okul_no, telefon, oneri_istek in oneri_ve_istekler:
        # Check if the department is already in the dictionary, if not, initialize it to 0
        if bolum not in department_counts:
            department_counts[bolum] = 0

        # Increment the count for the department
        department_counts[bolum] += 1

    # Sort departments and counts in descending order
    sorted_departments = sorted(department_counts.keys(), key=lambda x: department_counts[x], reverse=True)
    sorted_counts = [department_counts[dept] for dept in sorted_departments]

    # Create a bar chart to visualize department-wise distribution
    fig, ax = plt.subplots(figsize=(10, 6))  # Set the figure size
    bars = plt.barh(sorted_departments, sorted_counts, color='skyblue')
    plt.xlabel('İnsan Sayısı')  # X-axis label
    plt.ylabel('Bölüm')  # Y-axis label
    plt.title('Bölüm Bazında Dağılım')  # Title

    # Add exact number values to the bars
    # Add exact number values to the bars using a loop
    for bar, count in zip(bars, sorted_counts):
        width = bar.get_width()
        ax.annotate(f'{count}', xy=(width, bar.get_y() + bar.get_height() / 2), xytext=(5, 0),
                    textcoords='offset points', fontsize=10, color='black', weight='bold')

    # Display the bar chart
    plt.gca().invert_yaxis()  # Invert Y-axis to show the highest count at the top
    plt.tight_layout()
    plt.savefig('department_distribution.png', dpi=300, bbox_inches='tight')

    print("\nÖneri/İstekler (With Minimum 5 Characters):")
    oneri_istek_count = 0
    for ad_soyad, bolum, okul_no, telefon, oneri_istek in oneri_ve_istekler:
        if oneri_istek.strip() and len(oneri_istek.strip()) >= 5:
            print(f"Ad-Soyad: {ad_soyad}, Telefon: {telefon}")
            print(f"Öneri/İstek: {oneri_istek}\n")
            oneri_istek_count += 1

    total_records = len(oneri_ve_istekler)
    total_records_without_duplicates = len(ad_soyad_telefon)
    total_duplicates = len(duplicate_records)

    print(f"\nToplam Kayıt: {total_records}")
    print("\nBölüm Bazında İnsan Sayısı:")
    for department, count in department_counts.items():
        print(f"{department}: {count} kişi")
    print(f"Toplam Kayıt(Çiftler hariç): {total_records_without_duplicates}")
    print(f"Çift Kayıt Sayısı: {total_duplicates}")
    print(f"\nÖneri/İstek Yapan Sayısı: {oneri_istek_count}")
