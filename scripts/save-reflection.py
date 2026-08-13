#!/usr/bin/env python3
"""
Save reflection to pending file after generation.
Called by the agent after generating the SOAP reflection.

Usage:
  python3 save-reflection.py 2026-07-13 \"observation text...\" \"application text...\" \"prayer text...\"
"""
import sys
import json
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[1]


def save_reflection(date_str, scripture, observation, application, prayer):
    """Save reflection to pending file."""
    pending_file = WORKSPACE / "daily-soap" / "pending" / f"{date_str}.json"
    
    if not pending_file.exists():
        print(f"No pending file found: {pending_file}")
        return False
    
    with open(pending_file, 'r') as f:
        data = json.load(f)
    
    data["reflection"] = {
        "scripture": scripture,
        "observation": observation,
        "application": application,
        "prayer": prayer
    }
    
    with open(pending_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✓ Saved reflection to {pending_file}")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: save-reflection.py <date> <observation> <application> <prayer>")
        print("Note: scripture is taken from the verse already in the pending file")
        sys.exit(1)
    
    date_str = sys.argv[1]
    observation = sys.argv[2]
    application = sys.argv[3]
    prayer = sys.argv[4]
    
    # Scripture comes from existing verse
    pending_file = WORKSPACE / "daily-soap" / "pending" / f"{date_str}.json"
    with open(pending_file, 'r') as f:
        data = json.load(f)
    scripture = data.get("verse", {}).get("text", "")
    
    success = save_reflection(date_str, scripture, observation, application, prayer)
    sys.exit(0 if success else 1)
