import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://summonerswar.spokland.com"
IMAGES_DIR = "images"

def update_checker():
    # Create images folder if it doesn't exist
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)

    update_list_url = urljoin(BASE_URL, "/game/update")

    # Load existing update URLs from file (if any)
    urls_file = "update_urls.txt"
    existing_urls = set()
    if os.path.exists(urls_file):
        with open(urls_file, "r") as f:
            for line in f:
                existing_urls.add(line.strip())

    # Fetch the update list page
    response = requests.get(update_list_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract update URLs from the list page (using lowercase "onclick")
    update_divs = soup.find_all("div", class_="update")
    new_updates = []
    for div in update_divs:
        onclick = div.get("onclick")
        if onclick:
            match = re.search(r"window\.location\s*=\s*['\"](.*?)['\"]", onclick)
            if match:
                rel_url = match.group(1)
                full_url = urljoin(BASE_URL, rel_url)
                if full_url not in existing_urls:
                    new_updates.append(full_url)

    # Append new update URLs to the file if any
    if new_updates:
        with open(urls_file, "a") as f:
            for url in new_updates:
                f.write(url + "\n")
        print(f"Added {len(new_updates)} new update URL(s) to {urls_file}.")
    else:
        print("No new update URLs found.")

    # Process each new update
    for update_url in new_updates:
        print(f"Processing update page: {update_url}")
        upd_response = requests.get(update_url)
        upd_soup = BeautifulSoup(upd_response.text, "html.parser")

        # Check if "Skill Balance" appears in the text
        if re.search(r"skill\s*_?\s*balance", upd_response.text, re.IGNORECASE):
            print("Skill Balance update found.")
            # Find an image with "skill_balance" in its src
            skill_img = upd_soup.find("img", src=re.compile(r"skill_?balance", re.IGNORECASE))
            if skill_img and skill_img.get("src"):
                img_src = skill_img.get("src")
                # Build the full image URL relative to the update page URL
                img_url = urljoin(update_url, img_src)

                # Extract update date from the page (using a regex to find a date in YYYY-MM-DD format)
                date_match = re.search(r"(\d{4}-\d{2}-\d{2})", upd_response.text)
                if date_match:
                    update_date = date_match.group(1)
                else:
                    update_date = "unknown_date"

                # Determine the file extension from the URL (default to .jpg)
                ext = os.path.splitext(img_url)[1] or ".jpg"
                # Set output filename (e.g., skill_balance_2025-01-24.jpg)
                img_filename = f"skill_balance_{update_date}{ext}"
                file_path = os.path.join(IMAGES_DIR, img_filename)

                # Check if the file already exists
                if os.path.exists(file_path):
                    print(f"The image {img_filename} already exists in '{IMAGES_DIR}', download skipped.")
                    continue

                # Download and save the image
                img_response = requests.get(img_url)
                if img_response.status_code == 200:
                    with open(file_path, "wb") as img_file:
                        img_file.write(img_response.content)
                    print(f"Saved Skill Balance image as {file_path}.")
                else:
                    print(f"Failed to download image from {img_url}")
            else:
                print("No Skill Balance image found on the page.")
        else:
            print("No Skill Balance update detected on this page.")

if __name__ == "__main__":
    update_checker()
