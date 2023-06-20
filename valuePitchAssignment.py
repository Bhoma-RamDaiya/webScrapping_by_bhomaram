import requests
from bs4 import BeautifulSoup
import pandas as pd

# Send a GET request to the website
url = "https://citizen.mahapolice.gov.in/Citizen/MH/PublishedFIRs.aspx"
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find the total number of pages
page_count_element = soup.find("span", id="ctl00_ContentPlaceHolder1_GridViewPublishedFIR_ctl01_lblPageCount")
total_pages = int(page_count_element.text) if page_count_element else 1

# Define the base URL for pagination
base_url = "https://citizen.mahapolice.gov.in/Citizen/MH/PublishedFIRs.aspx?PageNo="

# Create empty lists to store rows and headers
rows = []
headers = []

# Loop through each page
for page in range(1, total_pages + 1):
    page_url = base_url + str(page)
    page_response = requests.get(page_url)
    page_soup = BeautifulSoup(page_response.content, "html.parser")

    # Find the table element on the page
    table = page_soup.find("table")

    # Extract the table headers if not already extracted
    if not headers:
        headers = [th.text.strip() for th in table.find_all("th")]

    # Extract the table rows within the specified date range
    for tr in table.find_all("tr"):
        row = [td.text.strip() for td in tr.find_all("td")]
        if len(row) == len(headers):
            registration_date = row[6]  # Assuming the 7th column contains the registration date
            if "01/01/2023" <= registration_date <= "01/02/2023":
                rows.append(row)

# Create a pandas DataFrame from the extracted data
df = pd.DataFrame(rows, columns=headers)

# Save the DataFrame to a CSV file
df.to_csv("data.csv", index=False)
