import requests
from bs4 import BeautifulSoup
import os
import time
import itertools
from alive import alive
alive()
def scrape_webpage(url, timeout=40):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        url = url.strip()
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        print(f"Successfully jobs: {url}")
        print(soup.get_text(strip=True)[:500] + "..\n")
        return True
    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return False

def process_urls_continuously(filename):
    if not os.path.exists(filename):
        print(f"Error: File {filename} not found!")
        return
    try:
        with open(filename, 'r') as file:
            urls = [url.strip() for url in file.readlines() if url.strip()]
    except IOError:
        print(f"Error reading file {filename}")
        return
    if not urls:
        print("No URLs found in the file!")
        return
    total_attempts = 0
    successful_scrapes = 0
    failed_scrapes = 0
    print(f"\nStarting of {len(urls)} URLs")
    url_cycle = itertools.cycle(urls)
    try:
        while True:
            current_url = next(url_cycle)
            total_attempts += 1
            if scrape_webpage(current_url):
                successful_scrapes += 1
            else:
                failed_scrapes += 1
            if total_attempts % len(urls) == 0:
                print(f"Total Attempts: {total_attempts}")
                print(f"Successful jobs: {successful_scrapes}")
                print(f"Failed jobs: {failed_scrapes}")
            time.sleep(33)
    except KeyboardInterrupt:
        print("\n\njobs stopped by user")
        print(f"Total Attempts: {total_attempts}")
        print(f"Successful jobs: {successful_scrapes}")
        print(f"Failed jobs: {failed_scrapes}")

if __name__ == "__main__":
    urls_file = "urls.txt"
    process_urls_continuously(urls_file)
