import csv

csv_file_path = 'comptech.csv'


# Function to check for duplicate records
def check_for_duplicates(record, records_list):
    tarih, e_posta, ad_soyad, bolum_sinif, telefon, oneri_istek = record
    for existing_record in records_list:
        _, existing_email, existing_name, _, existing_phone, _ = existing_record
        if e_posta == existing_email or ad_soyad == existing_name or telefon == existing_phone:
            return True
    return False


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
        tarih = veri_parcalari[0]
        e_posta = veri_parcalari[1]
        ad_soyad = veri_parcalari[2]
        bolum_sinif = veri_parcalari[3]
        telefon = format_phone_number(veri_parcalari[4])  # Format the phone number
        oneri_istek = veri_parcalari[5]

        # Check for duplicates before adding the record
        if not check_for_duplicates((tarih, e_posta, ad_soyad, bolum_sinif, telefon, oneri_istek), oneri_ve_istekler):
            ad_soyad_telefon.append((ad_soyad, telefon))
        else:
            duplicate_records.append((ad_soyad, telefon, e_posta))

        oneri_ve_istekler.append((tarih, e_posta, ad_soyad, bolum_sinif, telefon, oneri_istek))

    print("\nAd-Soyad ve Telefon Numaraları (Without Duplicates):")
    for ad_soyad, telefon in ad_soyad_telefon:
        print(f"{ad_soyad}: {telefon}")

    print("\nDuplicate Records:")
    for ad_soyad, telefon, e_posta in duplicate_records:
        print(f"Ad-Soyad: {ad_soyad}, Telefon: {telefon}, E-Posta: {e_posta}")

    print("\nÖneri/İstekler (With Minimum 5 Characters):")
    oneri_istek_count = 0
    for tarih, e_posta, ad_soyad, bolum_sinif, telefon, oneri_istek in oneri_ve_istekler:
        if oneri_istek.strip() and len(oneri_istek.strip()) >= 5:
            print(f"Ad-Soyad: {ad_soyad}, Telefon: {telefon}")
            print(f"Öneri/İstek: {oneri_istek}\n")
            oneri_istek_count += 1

    total_records = len(oneri_ve_istekler)
    total_records_without_duplicates = len(ad_soyad_telefon)
    total_duplicates = len(duplicate_records)

    print(f"\nToplam Kayıt: {total_records}")
    print(f"Toplam Kayıt(Çiftler hariç): {total_records_without_duplicates}")
    print(f"Çift Kayıt Sayısı: {total_duplicates}")
    print(f"\nÖneri/İstek Yapan Sayısı: {oneri_istek_count}")
