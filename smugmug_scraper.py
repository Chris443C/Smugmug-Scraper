import argparse
import requests
import time
import csv
import sys
from pathlib import Path

BASE_URL = "https://api.smugmug.com"
HEADERS = {
    "Accept": "application/json",
    # "Authorization": "Bearer YOUR_API_KEY"
}

def search_profiles(letter="M"):
    url = f"{BASE_URL}/api/v2/user!search?q={letter}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    users = response.json().get("Response", {}).get("User", [])
    return [user["NickName"] for user in users]

def get_user_node(username):
    url = f"{BASE_URL}/api/v2/folder/user/{username}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()["Response"]["Node"]["Uri"]

def search_content(usernode, keyword, content_type, start=1, count=100):
    if content_type == "images" or content_type == "videos":
        media_type = "Image" if content_type == "images" else "Video"
        url = (
            f"{BASE_URL}/api/v2/image!search?"
            f"Scope={usernode}&Text={keyword}&Type={media_type}"
            f"&SortDirection=Descending&SortMethod=Popular"
            f"&start={start}&count={count}"
        )
    elif content_type == "albums":
        url = (
            f"{BASE_URL}/api/v2/album!search?"
            f"Scope={usernode}&Text={keyword}&SortDirection=Descending&SortMethod=Rank"
        )
    elif content_type == "folders":
        # Only works with username, not usernode
        return None  # We'll handle it differently in `main`
    else:
        raise ValueError("Unsupported content type")

    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json().get("Response", {}).get("AlbumImage", []) if content_type in ["images", "videos"] else response.json().get("Response", {}).get("Album", [])

def search_folders_by_username(username, keyword):
    url = (
        f"{BASE_URL}/api/v2/folder/user/{username}!search?"
        f"Text={keyword}&SortDirection=Descending&SortMethod=Rank"
    )
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json().get("Response", {}).get("Folder", [])

def export_results_to_csv(results, keyword, content_type):
    output_file = Path(f"smugmug_{content_type}_{keyword}.csv")
    with output_file.open("w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"\n[+] Results exported to: {output_file.absolute()}")

def main(keyword, content_type, delay, export):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    all_results = []

    for letter in alphabet:
        print(f"\n[+] Searching users with '{letter}'...")
        try:
            users = search_profiles(letter)
        except Exception as e:
            print(f"[!] Error searching profiles for {letter}: {e}")
            continue

        for username in users:
            try:
                print(f"    [-] Processing user: {username}")
                if content_type == "folders":
                    results = search_folders_by_username(username, keyword)
                else:
                    usernode = get_user_node(username)
                    results = search_content(usernode, keyword, content_type)

                if results:
                    for item in results:
                        data = {
                            "Username": username,
                            "Title": item.get("Title", ""),
                            "URL": item.get("OriginalUrl") or item.get("Url") or item.get("WebUri"),
                        }
                        print(f"        Found: {data['Title']} — {data['URL']}")
                        all_results.append(data)

                time.sleep(delay)
            except Exception as e:
                print(f"        [!] Error with user {username}: {e}")
                continue
        time.sleep(delay * 2)

    if export and all_results:
        export_results_to_csv(all_results, keyword, content_type)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SmugMug CLI Scraper")
    parser.add_argument("--keyword", type=str, required=True, help="Search keyword")
    parser.add_argument("--type", type=str, choices=["images", "videos", "albums", "folders"], default="images", help="Content type to search")
    parser.add_argument("--delay", type=int, default=2, help="Delay between requests (seconds)")
    parser.add_argument("--export", action="store_true", help="Export results to CSV")
    args = parser.parse_args()

    try:
        main(args.keyword, args.type, args.delay, args.export)
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user.")
        sys.exit(0)
