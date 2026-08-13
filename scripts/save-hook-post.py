#!/usr/bin/env python3
"""
Save hook post content to pending file.
Called by the agent after generating hook post content.

Usage:
  python3 save-hook-post.py <date> <hook_type> <json_content>
  
  hook_type: read_this_if | 3_verses_when | a_prayer_for | what_this_means
  json_content: JSON string with hook-specific content

Examples:
  # "Read this if" hook
  python3 save-hook-post.py 2026-07-25 read_this_if '{"hook_text":"Read this if you\'re anxious.","subtext":"A verse for when worry takes over","verse_reference":"Philippians 4:6-7","verse_text":"Do not be anxious about anything...","reflection":"Anxiety isn\'t dismissed..."}'

  # "A prayer for" hook
  python3 save-hook-post.py 2026-07-25 a_prayer_for '{"hook_text":"A prayer for your family.","subtext":"For those you love most","prayer":"Lord, I lift up my family to You today..."}'

  # "3 verses when" hook
  python3 save-hook-post.py 2026-07-25 3_verses_when '{"hook_text":"3 verses when you feel overwhelmed.","verses":[{"reference":"Matthew 11:28","text":"Come to me..."},{"reference":"Psalm 61:2","text":"When my heart is overwhelmed..."}]}'

  # "What this means" hook
  python3 save-hook-post.py 2026-07-25 what_this_means '{"hook_text":"What Jeremiah 29:11 actually means.","verse_reference":"Jeremiah 29:11","verse_text":"For I know the plans...","misconception":"God promises me wealth...","actual_meaning":"This was written to exiles..."}'
"""

import sys
import json
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[1]

VALID_HOOK_TYPES = ["read_this_if", "3_verses_when", "a_prayer_for", "what_this_means"]


def save_hook_post(date_str, hook_type, content, status="pending"):
    """Save hook post to pending file."""
    if hook_type not in VALID_HOOK_TYPES:
        print(f"Error: Invalid hook type '{hook_type}'. Valid types: {', '.join(VALID_HOOK_TYPES)}")
        return False
    
    pending_dir = WORKSPACE / "daily-soap" / "pending-hooks"
    pending_dir.mkdir(parents=True, exist_ok=True)
    
    pending_file = pending_dir / f"{date_str}.json"
    
    data = {
        "hook_type": hook_type,
        "content": content,
        "status": status,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    with open(pending_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✓ Saved hook post to {pending_file}")
    return True


def main():
    if len(sys.argv) < 4:
        print("Usage: save-hook-post.py <date> <hook_type> <json_content>")
        print("")
        print("Hook types:")
        print("  read_this_if    - 4 images: hook, verse, reflection, cta")
        print("  3_verses_when   - 5 images: hook, verse1, verse2, verse3, cta")
        print("  a_prayer_for    - 3 images: hook, prayer, cta")
        print("  what_this_means - 4 images: hook, verse, vs, cta")
        print("")
        print("Example:")
        print('  python3 save-hook-post.py 2026-07-25 a_prayer_for \'{"hook_text":"A prayer for your family.","prayer":"Lord, I lift up..."}\'')
        sys.exit(1)
    
    date_str = sys.argv[1]
    hook_type = sys.argv[2]
    
    # Parse JSON content
    try:
        content = json.loads(sys.argv[3])
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON content: {e}")
        sys.exit(1)
    
    success = save_hook_post(date_str, hook_type, content)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
