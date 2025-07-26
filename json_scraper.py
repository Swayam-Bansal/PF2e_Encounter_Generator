import os
import requests
from bs4 import BeautifulSoup
from constants import (download_directory,  
                       raw_json_base, 
                       api_url)

# Create a directory to store downloaded JSON files
if not os.path.exists(download_directory):
    os.makedirs(download_directory)
    print(f"Created directory: {download_directory}")
else:
    print(f"Directory '{download_directory}' already exists.")

# Scrape HTML content of the Github source directory
response = requests.get(api_url)
if response.status_code != 200:
    print(f"Failed to retrieve data from {api_url}. Status code: {response.status_code}")
    exit()

json_files = [item['name'] for item in response.json() if item['name'].endswith('.json')] # List comprehension to filter JSON files
print(f"Found {len(json_files)} JSON files from the Github API response.")

# Download each JSON file
for filename in json_files:
    raw_url = raw_json_base + filename
    print(f"Downloading {filename} from {raw_url}...")
    try:
        file_response = requests.get(raw_url)
        file_response.raise_for_status() # Raise an error for bad responses
        with open(os.path.join(download_directory, filename), 'wb') as file: # Write mode, binary mode
            file.write(file_response.content)
        print(f"Downloaded {filename} successfully.")
    except requests.RequestException as e:
        print(f"Failed to download {filename}: {e}")

print("All JSON files downloaded successfully.") # If no errors, all downloads worked