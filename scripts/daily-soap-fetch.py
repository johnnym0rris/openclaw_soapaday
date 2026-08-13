#!/usr/bin/env python3
"""
Daily SOAP Fetch - Step 1
Fetches verse of the day from YouVersion Platform API and saves to pending file for approval

Requires: YOUVERSION_API_KEY in .env or environment
"""
import os
import sys
import json
import re
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[1]
ENV_FILE = WORKSPACE / ".env"

# Load .env if present
if ENV_FILE.exists():
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())

API_KEY = os.environ.get("YOUVERSION_API_KEY", "")
API_BASE = "https://api.youversion.com/v1"

# Default Bible ID for English (BSB - Berean Standard Bible)
# YouVersion uses numeric IDs. Common ones:
# 1 = KJV, 111 = NIV, 59 = ESV, 206 = NLT, 143 = NRT (Russian)
DEFAULT_BIBLE_ID = "111"  # NIV


def _strip_html(html: str) -> str:
    """Strip HTML tags from verse content."""
    text = re.sub(r"<[^>]+>", "", html)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def fetch_verse_of_the_day():
    """Fetch verse of the day from YouVersion Platform API."""
    if not API_KEY:
        print("Error: YOUVERSION_API_KEY not set. Add it to .env")
        return None
    
    # Get day of year (1-366)
    day_of_year = datetime.now().timetuple().tm_yday
    
    try:
        # Step 1: Get the verse reference for today
        votd_url = f"{API_BASE}/verse_of_the_days/{day_of_year}"
        req = urllib.request.Request(
            votd_url,
            headers={
                "X-YVP-App-Key": API_KEY,
                "User-Agent": "SOAPaDay-Bot/1.0",
                "Accept": "application/json"
            }
        )
        
        with urllib.request.urlopen(req, timeout=15) as response:
            votd_data = json.loads(response.read().decode("utf-8"))
        
        passage_id = votd_data.get("passage_id")
        if not passage_id:
            print(f"Error: No passage_id in VOTD response: {votd_data}")
            return None
        
        print(f"   VOTD day {day_of_year} -> passage: {passage_id}")
        
        # Step 2: Fetch the actual verse text
        passage_url = f"{API_BASE}/bibles/{DEFAULT_BIBLE_ID}/passages/{passage_id}"
        req2 = urllib.request.Request(
            passage_url,
            headers={
                "X-YVP-App-Key": API_KEY,
                "User-Agent": "SOAPaDay-Bot/1.0",
                "Accept": "application/json"
            }
        )
        
        with urllib.request.urlopen(req2, timeout=15) as response:
            passage_data = json.loads(response.read().decode("utf-8"))
        
        verse_text = _strip_html(passage_data.get("content", ""))
        reference = passage_data.get("reference", passage_id.replace(".", " "))
        
        # Format reference nicely (e.g., "ISA.12.2" -> "Isaiah 12:2")
        reference = _format_reference(reference)
        
        return {
            "reference": reference,
            "text": verse_text,
            "translation": "NIV",
            "passage_id": passage_id,
            "day_of_year": day_of_year
        }
        
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if hasattr(e, 'read') else ""
        print(f"HTTP Error {e.code}: {error_body}")
        return None
    except Exception as e:
        print(f"Error fetching verse: {e}")
        return None


def _format_reference(ref: str) -> str:
    """Format a USFM reference like 'ISA.12.2' to 'Isaiah 12:2'."""
    # If already formatted (contains spaces), return as-is
    if " " in ref and ":" in ref:
        return ref
    
    # Map book codes to names
    BOOK_NAMES = {
        "GEN": "Genesis", "EXO": "Exodus", "LEV": "Leviticus", "NUM": "Numbers",
        "DEU": "Deuteronomy", "JOS": "Joshua", "JDG": "Judges", "RUT": "Ruth",
        "1SA": "1 Samuel", "2SA": "2 Samuel", "1KI": "1 Kings", "2KI": "2 Kings",
        "1CH": "1 Chronicles", "2CH": "2 Chronicles", "EZR": "Ezra", "NEH": "Nehemiah",
        "EST": "Esther", "JOB": "Job", "PSA": "Psalm", "PRO": "Proverbs",
        "ECC": "Ecclesiastes", "SNG": "Song of Solomon", "ISA": "Isaiah", "JER": "Jeremiah",
        "LAM": "Lamentations", "EZK": "Ezekiel", "DAN": "Daniel", "HOS": "Hosea",
        "JOL": "Joel", "AMO": "Amos", "OBA": "Obadiah", "JON": "Jonah",
        "MIC": "Micah", "NAM": "Nahum", "HAB": "Habakkuk", "ZEP": "Zephaniah",
        "HAG": "Haggai", "ZEC": "Zechariah", "MAL": "Malachi",
        "MAT": "Matthew", "MRK": "Mark", "LUK": "Luke", "JHN": "John",
        "ACT": "Acts", "ROM": "Romans", "1CO": "1 Corinthians", "2CO": "2 Corinthians",
        "GAL": "Galatians", "EPH": "Ephesians", "PHP": "Philippians", "COL": "Colossians",
        "1TH": "1 Thessalonians", "2TH": "2 Thessalonians", "1TI": "1 Timothy", "2TI": "2 Timothy",
        "TIT": "Titus", "PHM": "Philemon", "HEB": "Hebrews", "JAS": "James",
        "1PE": "1 Peter", "2PE": "2 Peter", "1JN": "1 John", "2JN": "2 John",
        "3JN": "3 John", "JUD": "Jude", "REV": "Revelation"
    }
    
    parts = ref.split(".")
    if len(parts) >= 3:
        book = BOOK_NAMES.get(parts[0], parts[0])
        chapter = parts[1]
        verse = parts[2]
        return f"{book} {chapter}:{verse}"
    
    return ref


def save_pending_verse(verse):
    """Save verse to pending file for approval."""
    pending_dir = WORKSPACE / "daily-soap" / "pending"
    pending_dir.mkdir(parents=True, exist_ok=True)
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    pending_file = pending_dir / f"{date_str}.json"
    
    with open(pending_file, 'w') as f:
        json.dump({
            "verse": verse,
            "status": "pending",
            "requested_at": datetime.now().isoformat()
        }, f, indent=2)
    
    return pending_file


def main():
    print("Fetching verse of the day from YouVersion...")
    verse = fetch_verse_of_the_day()
    
    if not verse:
        print("Failed to fetch verse")
        sys.exit(1)
    
    pending_file = save_pending_verse(verse)
    print(f"Saved pending verse to: {pending_file}")
    
    # Output for the cron message
    print(f"\nVerse of the Day: {verse['reference']}")
    print(f"\"{verse['text'][:100]}...\"")
    print(f"\nAwaiting reflection generation and approval.")


if __name__ == "__main__":
    main()
