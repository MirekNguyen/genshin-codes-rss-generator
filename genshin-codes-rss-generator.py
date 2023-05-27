import requests
from bs4 import BeautifulSoup
import json

# Send a GET request to the website
url = 'https://genshin-impact.fandom.com/wiki/Promotional_Code'  # Replace with the actual URL of the website
response = requests.get(url)

# Create a BeautifulSoup object
soup = BeautifulSoup(response.content, 'html.parser')

# Find the tbody element
tbody = soup.find('tbody')

# Do something with the tbody element
# For example, you can print its contents
# print(tbody)

# Extract data from tbody and convert it to a JSON object
data = []
for row in tbody.find_all('tr'):
    row_data = []
    if not "expired" in row.text.lower():
        for cell in row.find_all('td'):
            row_data.append(cell.text.strip())
        data.append(row_data)
# Convert data to JSON
json_data = json.dumps(data)

# Print the JSON object
print(json_data)
