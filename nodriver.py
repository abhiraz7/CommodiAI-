import requests
from bs4 import BeautifulSoup
import webbrowser
import urllib.parse

# Step 1: Load the webpage
base_url = "https://vtechys.com"
response = requests.get(base_url)
soup = BeautifulSoup(response.text, 'html.parser')

time.sleep(10)
# Step 2: Find matching link
target_keyword = "services"
found = False

for link in soup.find_all("a", href=True):
    link_text = link.get_text(strip=True).lower()
    if target_keyword in link_text:
        full_url = urllib.parse.urljoin(base_url, link['href'])
        print(f"Found matching link: {full_url}")
        time.sleep(10)

        # Step 3: Open in default browser
        webbrowser.open(full_url)
        found = True
        break

if not found:
    print("No matching link found.")

