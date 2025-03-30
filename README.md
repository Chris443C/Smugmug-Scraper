# 📸 SmugMug CLI Scraper

A command-line tool to search public SmugMug user content using fuzzy logic search endpoints. Supports searching **images**, **videos**, **albums**, and **folders**, and can export results to CSV.

---

## 🚀 Features

- 🔍 Fuzzy profile search (based on letters/numbers)
- 🖼️ Content discovery: images, videos, albums, folders
- 📁 CSV export
- 🛑 Throttled to avoid API rate limits / harvesting detection
- ✅ Pure Python (no login required for public content)

---

## 📦 Requirements

- Python 3.7+
- [requests](https://pypi.org/project/requests/)

Install dependencies:

pip install -r requirements.txt

🛠️ Usage
bash
Copy
Edit
python smugmug_scraper.py --keyword iphone --type images --export
Options
Flag	Description	Example
--keyword	Text to search in content	--keyword iphone
--type	Content type: images, videos, albums, folders	--type albums
--delay	Delay in seconds between requests (default: 2)	--delay 5
--export	Export results to CSV	--export
📂 Output
If --export is used, results will be saved as:

php-template
Copy
Edit
smugmug_<type>_<keyword>.csv
Each row includes:

Username
Title
URL (direct to image/album/folder)

🔐 Authentication (Optional)
Public endpoints don’t require an API key, but for higher rate limits or access to private content:

Get a SmugMug API token

Add to HEADERS in smugmug_scraper.py:

python
Copy
Edit
HEADERS = {
    "Accept": "application/json",
    "Authorization": "Bearer YOUR_API_KEY"
}
⚠️ Disclaimer
This tool is for educational and personal use only. Be respectful of SmugMug's API terms of service and avoid aggressive scraping.
