import os
import re
import time
from dotenv import load_dotenv
import requests
from markdownify import markdownify as md

load_dotenv()

BASE_URL = "https://platform.quip.com/1"
QUIP_TOKEN = os.getenv("QUIP_TOKEN")
EXPORT_FORMAT = os.getenv("EXPORT_FORMAT", "markdown")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./quip_all_exports")

if not QUIP_TOKEN:
    raise ValueError("QUIP_TOKEN environment variable is required. See .env.example")

HEADERS = {"Authorization": f"Bearer {QUIP_TOKEN}"}

def sanitize_filename(name):
    """Removes invalid Mac/Windows/Linux characters from document titles."""
    return re.sub(r'[\\/*?:"<>|]', "", name).strip() or "Untitled_Document"

def get_all_root_folder_ids():
    """Fetches the main desktop, private, and archive folder IDs for your account."""
    print("Connecting to Quip profile to locate your master directories...")
    try:
        response = requests.get(f"{BASE_URL}/users/current", headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        
        # Collect all structural entry points into a single set to avoid duplicates
        folder_ids = set()
        for key in ["desktop_folder_id", "private_folder_id", "archive_folder_id"]:
            f_id = data.get(key)
            if f_id:
                folder_ids.add(f_id)
                
        # Also grab any shared or group folder roots attached to your account
        for f_id in data.get("group_folder_ids", []):
            folder_ids.add(f_id)
            
        return list(folder_ids)
    except Exception as e:
        print(f"❌ Failed to read account structure: {e}")
        return []

def crawl_and_download_everything():
    root_folders = get_all_root_folder_ids()
    if not root_folders:
        print("No master folders found. Exiting.")
        return

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Track downloaded threads to prevent downloading the same file twice
    downloaded_threads = set()
    saved_count = 0
    
    # We use a queue to handle nested subfolders (Breadth-First Search)
    folder_queue = root_folders.copy()
    print(f"Starting sweep of {len(folder_queue)} master areas. This will scan all subfolders...\n")

    while folder_queue:
        current_folder = folder_queue.pop(0)
        
        try:
            folder_resp = requests.get(f"{BASE_URL}/folders/{current_folder}", headers=HEADERS)
            # If a specific subfolder throws a 403/404, we skip it and keep moving
            if folder_resp.status_code in [403, 404]:
                continue
            folder_resp.raise_for_status()
            children = folder_resp.json().get("children", [])
        except Exception:
            continue

        for item in children:
            # If it's a subfolder, add it to our queue to scan later
            if "folder_id" in item:
                subfolder_id = item["folder_id"]
                if subfolder_id not in root_folders: 
                    folder_queue.append(subfolder_id)
                    
            # If it's a document file, download it
            elif "thread_id" in item:
                thread_id = item["thread_id"]
                if thread_id in downloaded_threads:
                    continue
                    
                downloaded_threads.add(thread_id)
                
                try:
                    thread_resp = requests.get(f"{BASE_URL}/threads/{thread_id}", headers=HEADERS)
                    thread_resp.raise_for_status()
                    thread_data = thread_resp.json()
                except Exception:
                    continue

                thread_info = thread_data.get("thread", {})
                title = thread_info.get("title", f"Document_{thread_id}")
                clean_title = sanitize_filename(title)
                
                html_content = thread_data.get("html", "")
                if not html_content:
                    continue

                if EXPORT_FORMAT.lower() == "markdown":
                    converted_content = md(html_content, heading_style="ATX")
                    file_extension = "md"
                else:
                    converted_content = html_content
                    file_extension = "html"

                file_path = os.path.join(OUTPUT_DIR, f"{clean_title}.{file_extension}")
                
                # If file already exists, append timestamp or ID to prevent overwriting
                if os.path.exists(file_path):
                    file_path = os.path.join(OUTPUT_DIR, f"{clean_title}_{thread_id}.{file_extension}")

                try:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(converted_content)
                    print(f"Downloaded: {clean_title}.{file_extension}")
                    saved_count += 1
                except IOError as e:
                    print(f"Could not save {clean_title}: {e}")
                
                # Respect rate limits so Quip doesn't choke
                time.sleep(0.4)

    print(f"\nCompleted! Saved a total of {saved_count} files into: {OUTPUT_DIR}")

if __name__ == "__main__":
    crawl_and_download_everything()
