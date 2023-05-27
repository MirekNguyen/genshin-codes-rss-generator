import re
import sys
from datetime import datetime

import pytz
import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

timezone = pytz.timezone("Europe/Prague")

# Send a GET request to the website
url = "https://genshin-impact.fandom.com/wiki/Promotional_Code"
response = requests.get(url)

# Find the tbody element
soup = BeautifulSoup(response.content, "html.parser")
tbody = soup.find("tbody")

# Extract data from tbody and convert it to a JSON object
data = []
for row in tbody.find_all("tr"):
    row_data = []
    if "expired" not in row.text.lower():
        for cell in row.find_all("td"):
            row_data.append(cell.text.strip())
        if row_data:
            data.append(row_data)

# Generate feed
fg = FeedGenerator()
fg.id("https://mirekng.com/rss/genshin-codes.xml")
fg.title("Genshin codes")
fg.subtitle("Genshin codes")
fg.link(href="https://mirekng.com", rel="self")
fg.language("en")
for item in reversed(data):
    fe = fg.add_entry()
    fe.id(item[0])
    fe.title(item[3])
    fe.link(href="https://genshin.hoyoverse.com/en/gift?code=" +
            item[0], replace=True)
    match = re.search(r"Discovered: ([A-Za-z]+ \d{1,2}, \d{4})", item[3])
    if match:
        date_string = match.group(1)
        pubDate = datetime.strptime(date_string, "%B %d, %Y")
    else:
        pubDate = datetime.now()
    fe.pubDate(timezone.localize(pubDate))
rssfeed = fg.rss_str(pretty=True)
fg.rss_file(sys.argv[len(sys.argv) - 1])
