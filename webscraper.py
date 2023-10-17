import csv
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Function to scrape and save data to a CSV file
def scrape_and_save():
    url = "https://club.ieu.edu.tr/panel/manage-clubs-approval"

    # Create a WebDriver
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Display a message to instruct the user
    messagebox.showinfo("Web Scraper", "Please press OK when the webpage is ready...")

    # Find the table containing the data by using alternative methods
    table = None
    try:
        table = driver.find_element("id", "DataTables_Table_0")
    except NoSuchElementException:
        pass

    if table:
        # Ask the user if they want to overwrite or append to an existing CSV file
        dialog_result = simpledialog.askstring("CSV File Action",
                                               "Do you want to (O)verwrite or (A)ppend to the CSV file?")

        if dialog_result and dialog_result.strip().lower() == "o":
            write_mode = 'w'  # Overwrite mode
        else:
            write_mode = 'a'  # Append mode

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            with open(file_path, write_mode, encoding='utf-8', newline='') as csv_file:
                writer = csv.writer(csv_file)
                if write_mode == 'w':
                    header_row = table.find_element("tag name", "thead").find_element("tag name", "tr")
                    header = [th.text.strip() for th in header_row.find_elements("tag name", "th")]
                    writer.writerow(header)

                while True:
                    rows = table.find_element("tag name", "tbody").find_elements("tag name", "tr")
                    for row in rows:
                        data = [td.text.strip() for td in row.find_elements("tag name", "td")]
                        data = [item if item else '-' for item in data]  # Replace missing data with a hyphen
                        writer.writerow(data)

                    # Check if there is a "Next" button to move to the next page
                    try:
                        next_button = driver.find_element("link text", "Next")
                        next_button.click()
                        WebDriverWait(driver, 10).until(EC.staleness_of(table))
                        table = driver.find_element("id", "DataTables_Table_0")
                    except NoSuchElementException:
                        break
                    except TimeoutException:
                        print("Timed out waiting for the next page to load")

                print(f"Data has been saved to the CSV file in {write_mode} mode.")
    else:
        print("No table data found on the webpage.")

    driver.quit()


# Create the main application window
root = tk.Tk()
root.title("Web Scraper")

# Create a button to start the scraping process
scrape_button = tk.Button(root, text="Start Scraping", command=scrape_and_save)
scrape_button.pack()

root.mainloop()
