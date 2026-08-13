#!/usr/bin/env python3
"""
Hook Post Automation for SOAPaDay
- Reads approved hook post from pending file
- Generates branded images
- Uploads to CDN
- Posts to Facebook + Instagram via Buffer

Usage:
  python3 hook-post-automation.py           # Process today's pending hook
  python3 hook-post-automation.py 2026-07-25 # Process specific date
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Add workspace to path
WORKSPACE = Path(__file__).resolve().parents[1]

# Import upload_media first (from instagram-poster)
sys.path.insert(0, str(WORKSPACE / "skills" / "instagram-poster" / "scripts"))
from upload_media import upload_media

# Import post_to_buffer from social-posting
sys.path.insert(0, str(WORKSPACE / "skills" / "social-posting" / "scripts"))
from post_to_buffer import post_to_buffer

# Import image generator functions directly
import importlib.util
spec = importlib.util.spec_from_file_location("generate_hook_post", str(WORKSPACE / "scripts" / "generate-hook-post.py"))
generate_hook_post = importlib.util.module_from_spec(spec)
sys.modules["generate_hook_post"] = generate_hook_post
spec.loader.exec_module(generate_hook_post)

load_hook_data = generate_hook_post.load_hook_data
generate_images = generate_hook_post.generate_images
mark_posted = generate_hook_post.mark_posted


def upload_images(image_paths):
    """Upload images to CDN and return URLs."""
    urls = []
    for path in image_paths:
        try:
            result = upload_media(str(path))
            if result.get("success"):
                urls.append(result["url"])
                print(f"   ✓ Uploaded: {result['url']}")
            else:
                print(f"   ✗ Failed to upload {path}: {result}")
        except Exception as e:
            print(f"   ✗ Error uploading {path}: {e}")
    return urls


def build_caption(data, platform="facebook"):
    """Build caption for a given platform."""
    content = data.get("content", {})
    hook_type = data.get("hook_type", "")
    
    # Get the hook text (main headline)
    hook_text = content.get("hook_text", "")
    # Remove trailing period for cleaner caption
    hook_text = hook_text.rstrip(".")
    
    lines = []
    
    if hook_type == "read_this_if":
        verse_ref = content.get("verse_reference", "")
        lines = [
            f"{hook_text}",
            "",
            f'"{content.get("verse_text", "")[:120]}..."',
            "",
            "Which part of this resonates with you?",
            "",
            "Start journaling today! Download the SOAPaDay app and build your daily Bible study habit.",
            "",
            "https://SOAPaDay.com",
            "",
            f"#SOAPaDay #BibleStudy #DailyDevotional #{verse_ref.replace(' ', '')} #FaithJournaling #ScriptureStudy"
        ]
    
    elif hook_type == "3_verses_when":
        verses = content.get("verses", [])
        verse_refs = [v.get("reference", "") for v in verses[:3]]
        lines = [
            f"{hook_text}",
            "",
            "Save these for when you need them.",
            "",
            "Which verse speaks to you today?",
            "",
            "Study these in SOAPaDay — write your own reflections, prayers, and applications.",
            "",
            "https://SOAPaDay.com",
            "",
            f"#SOAPaDay #BibleStudy #DailyDevotional #FaithJournaling #ScriptureStudy"
        ]
    
    elif hook_type == "a_prayer_for":
        lines = [
            f"{hook_text}",
            "",
            "Whether near or far, our families are on our hearts. Take a moment to lift them up.",
            "",
            '"And whatever you ask in prayer, you will receive, if you have faith." — Matthew 21:22',
            "",
            "What is one thing you are praying for your family this week?",
            "",
            "Write your own prayers in SOAPaDay.",
            "",
            "https://SOAPaDay.com",
            "",
            "#SOAPaDay #BibleJournaling #DailyBible #FaithDaily #Scripture #ChristianApp #MorningDevotional #BibleReflection"
        ]
    
    elif hook_type == "what_this_means":
        verse_ref = content.get("verse_reference", "")
        lines = [
            f"{hook_text}",
            "",
            "Context changes everything.",
            "",
            f'"{content.get("verse_text", "")[:120]}..."',
            "",
            "Study with context in SOAPaDay — understand the who, what, when, and why before you apply.",
            "",
            "https://SOAPaDay.com",
            "",
            f"#SOAPaDay #BibleStudy #DailyDevotional #{verse_ref.replace(' ', '')} #FaithJournaling #ScriptureStudy"
        ]
    
    else:
        lines = [
            f"{hook_text}",
            "",
            "Start journaling today! Download the SOAPaDay app.",
            "",
            "https://SOAPaDay.com",
            "",
            "#SOAPaDay #BibleStudy #DailyDevotional #FaithJournaling"
        ]
    
    return "\n".join(lines)


def post_to_platforms(data, image_urls):
    """Post to Facebook and Instagram via Buffer."""
    results = {}
    
    # Post to Facebook
    print("\n4a. Posting to Facebook...")
    fb_caption = build_caption(data, "facebook")
    fb_result = post_to_buffer(
        text=fb_caption,
        image_urls=image_urls,
        platform="facebook"
    )
    results["facebook"] = fb_result
    
    if fb_result.get("success"):
        print(f"   ✅ Facebook posted! Post ID: {fb_result['post_id']}")
    else:
        print(f"   ❌ Facebook failed: {fb_result.get('error')}")
    
    # Post to Instagram
    print("\n4b. Posting to Instagram...")
    ig_caption = build_caption(data, "instagram")
    ig_result = post_to_buffer(
        text=ig_caption,
        image_urls=image_urls,
        platform="instagram"
    )
    results["instagram"] = ig_result
    
    if ig_result.get("success"):
        print(f"   ✅ Instagram posted! Post ID: {ig_result['post_id']}")
    else:
        print(f"   ❌ Instagram failed: {ig_result.get('error')}")
    
    return results


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="SOAPaDay Hook Post Automation")
    parser.add_argument("date", nargs="?", help="Date string YYYY-MM-DD (default: today)")
    args = parser.parse_args()
    
    date_str = args.date or datetime.now().strftime("%Y-%m-%d")
    
    print("=" * 50)
    print(f"SOAPaDay Hook Post Automation — {date_str}")
    print("=" * 50)
    
    # 1. Load approved hook data
    print("\n1. Loading approved hook post...")
    data = load_hook_data(date_str)
    if not data:
        print("   No approved hook post found. Exiting.")
        sys.exit(1)
    
    hook_type = data.get("hook_type", "unknown")
    print(f"   Hook type: {hook_type}")
    
    # 2. Generate images
    print("\n2. Generating images...")
    image_paths = generate_images(data)
    
    if not image_paths:
        print("   Failed to generate images.")
        sys.exit(1)
    
    print(f"\n   Generated {len(image_paths)} images")
    
    # 3. Upload images
    print("\n3. Uploading images...")
    image_urls = upload_images(image_paths)
    print(f"   Uploaded {len(image_urls)} images")
    
    if len(image_urls) != len(image_paths):
        print("   Warning: Not all images uploaded successfully")
    
    # 4. Post to Facebook and Instagram
    results = post_to_platforms(data, image_urls)
    
    # Mark as posted if at least one platform succeeded
    if any(r.get("success") for r in results.values()):
        mark_posted(date_str)
    else:
        print("\n   ❌ All platforms failed. Not marking as posted.")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("Done!")
    print("=" * 50)


if __name__ == "__main__":
    main()
