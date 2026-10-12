# CSV Formatter & Contact Export Utilities

A collection of three small Python utilities originally built to work with tabular event/club records. These scripts are **not a generalized CSV conversion library**: file names, column order, and some text labels are hard-coded for the original workflow.

## Scripts

| File | Purpose |
| --- | --- |
| `main.py` | Reads `comptech.csv`, checks for duplicate student/contact records, normalizes phone numbers, saves `comptech_no_duplicates.csv`, and generates `department_distribution.png`. |
| `google_contacts_phone_numberformatter.py` | Converts `comptech_no_duplicates.csv` into a Google Contacts-style CSV named `comptech_phone.csv`. |
| `webscraper.py` | Opens a Tkinter interface and uses Selenium/Chrome to export rows from a specified club-management page to CSV. |

## Requirements

- Python 3
- `matplotlib` for `main.py`
- `selenium`, Chrome, and compatible browser driver for `webscraper.py`
- Tkinter available in your Python installation for the scraper UI

```bash
python -m pip install matplotlib selenium
```

## Basic workflow

The input CSV and expected column layout are specific to the original data:

```text
Ad-Soyad, Bölüm, Okul No, Telefon, Öneri/İstek
```

Place `comptech.csv` in the current working directory and run:

```bash
python main.py
python google_contacts_phone_numberformatter.py
```

The first script prepares data, and the second creates a Google Contacts import file. Inspect the output before importing: duplicate reporting does not guarantee all duplicate records have been removed.

For the optional scraper UI:

```bash
python webscraper.py
```

The scraper is tailored to a particular page structure, may require authorized access, and can break if that site changes.

## Privacy note

Input and output files may contain personal information (names, student numbers, phone numbers, or messages). Only process data you are authorized to use, and **do not commit real contact exports or other private records to GitHub**.
