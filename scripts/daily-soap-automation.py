#!/usr/bin/env python3
"""
Daily SOAP Automation for SOAPaDay
- Reads approved verse + reflection from pending file
- Creates 4 share images with vertical centering
- Uploads to CDN
- Posts to Facebook via Buffer

Usage:
  python3 daily-soap-automation.py           # Process today's pending file
  python3 daily-soap-automation.py 2026-07-02 # Process specific date
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

# Import post_to_buffer from social-posting (must be after to avoid conflict)
sys.path.insert(0, str(WORKSPACE / "skills" / "social-posting" / "scripts"))
from post_to_buffer import post_to_buffer

# Image generation
from PIL import Image, ImageDraw, ImageFont
import textwrap


def load_pending_data(date_str=None):
    """Load the approved verse and reflection from pending file."""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    pending_file = WORKSPACE / "daily-soap" / "pending" / f"{date_str}.json"
    
    if not pending_file.exists():
        print(f"No pending file found: {pending_file}")
        return None
    
    with open(pending_file, 'r') as f:
        data = json.load(f)
    
    if data.get("status") not in ["approved", "posted"]:
        print(f"Reflection not approved yet. Status: {data.get('status')}")
        return None
    
    return data


def create_share_images(data):
    """Create 4 share images matching SOAPaDay design with vertical centering."""
    CANVAS_WIDTH = 1080
    CANVAS_HEIGHT = 1350
    PADDING_H = 72
    PADDING_TOP = 72
    PADDING_BOTTOM = 96
    
    BACKGROUND_COLOR = "#FAFAFA"
    PRIMARY_COLOR = "#1A5F4A"
    ON_SURFACE_COLOR = "#1C1B1F"
    ON_SURFACE_VARIANT = "#49454F"
    
    font_paths = {
        'display': ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'],
        'body': ['/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'],
        'body_italic': ['/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf'],
        'ui': ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'],
        'ui_semi': ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'],
    }
    
    def get_font(style, size):
        for path in font_paths.get(style, font_paths['ui']):
            if os.path.exists(path):
                try:
                    return ImageFont.truetype(path, size)
                except:
                    continue
        return ImageFont.load_default()
    
    def create_slide(letter, label, body_text, reference=None, translation=None, 
                     is_scripture=False, is_empty=False):
        img = Image.new('RGB', (CANVAS_WIDTH, CANVAS_HEIGHT), BACKGROUND_COLOR)
        draw = ImageDraw.Draw(img)
        
        scale = 1.0
        content_x = PADDING_H
        content_y = PADDING_TOP
        content_width = CANVAS_WIDTH - (PADDING_H * 2)
        content_height = CANVAS_HEIGHT - PADDING_TOP - PADDING_BOTTOM
        
        letter_font = get_font('display', int(44 * scale))
        label_font = get_font('ui_semi', int(24 * scale))
        
        draw.text((content_x, content_y), letter, font=letter_font, fill=PRIMARY_COLOR)
        letter_bbox = draw.textbbox((0, 0), letter, font=letter_font)
        letter_width = letter_bbox[2] - letter_bbox[0]
        
        label_x = content_x + letter_width + int(16 * scale)
        draw.text((label_x, content_y + 4), label.upper(), font=label_font, fill=ON_SURFACE_VARIANT)
        
        header_height = int(48 * scale) + int(28 * scale)
        
        if is_empty:
            body_font = get_font('body_italic', int(42 * scale))
            body_color = ON_SURFACE_VARIANT
        else:
            body_font = get_font('body' if is_scripture else 'ui', int(42 * scale))
            body_color = ON_SURFACE_COLOR
        
        char_width = int(22 * scale)
        max_chars = content_width // char_width
        wrapped_lines = textwrap.wrap(body_text, width=max_chars)
        
        # Vertical centering
        line_height = int(58 * scale)
        total_text_height = len(wrapped_lines) * line_height
        available_height = content_height - header_height
        body_y = content_y + header_height + (available_height - total_text_height) // 2
        body_y = max(body_y, content_y + header_height)
        
        current_y = body_y
        for line in wrapped_lines:
            if current_y + line_height > content_y + content_height:
                break
            draw.text((content_x, current_y), line, font=body_font, fill=body_color)
            current_y += line_height
        
        if reference and is_scripture:
            ref_y = current_y + int(40 * scale)
            ref_font = get_font('display', int(30 * scale))
            draw.text((content_x, ref_y), reference, font=ref_font, fill=PRIMARY_COLOR)
            
            if translation:
                trans_y = ref_y + int(38 * scale) + int(8 * scale)
                trans_font = get_font('ui', int(22 * scale))
                draw.text((content_x, trans_y), translation, font=trans_font, fill=ON_SURFACE_VARIANT)
        
        watermark_y = CANVAS_HEIGHT - PADDING_BOTTOM + int(32 * scale)
        watermark_font = get_font('ui_semi', int(20 * scale))
        url_font = get_font('ui', int(18 * scale))
        
        tagline = "Journaled on SOAPaDay (Free & Ad-Free Bible Journal)"
        url = "SOAPaDay.com"
        
        tag_bbox = draw.textbbox((0, 0), tagline, font=watermark_font)
        tag_width = tag_bbox[2] - tag_bbox[0]
        tag_x = (CANVAS_WIDTH - tag_width) // 2
        draw.text((tag_x, watermark_y), tagline, font=watermark_font, fill=ON_SURFACE_VARIANT)
        
        url_bbox = draw.textbbox((0, 0), url, font=url_font)
        url_width = url_bbox[2] - url_bbox[0]
        url_x = (CANVAS_WIDTH - url_width) // 2
        draw.text((url_x, watermark_y + int(26 * scale)), url, font=url_font, fill=PRIMARY_COLOR)
        
        return img
    
    output_dir = WORKSPACE / "daily-soap" / "images"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    verse = data.get("verse", {})
    reflection = data.get("reflection", {})
    
    scripture_text = reflection.get("scripture", verse.get("text", ""))
    reference = verse.get("reference", "")
    translation = verse.get("translation", "NIV")
    
    images = []
    
    # 1. Scripture
    img1 = create_slide(
        letter="S",
        label="Scripture",
        body_text=scripture_text,
        reference=reference,
        translation=translation,
        is_scripture=True
    )
    img1_path = output_dir / "01-scripture.png"
    img1.save(img1_path)
    images.append(img1_path)
    print("✓ Generated 01-scripture.png")
    
    # 2. Observation
    img2 = create_slide(
        letter="O",
        label="Observation",
        body_text=reflection.get("observation", "")
    )
    img2_path = output_dir / "02-observation.png"
    img2.save(img2_path)
    images.append(img2_path)
    print("✓ Generated 02-observation.png")
    
    # 3. Application
    img3 = create_slide(
        letter="A",
        label="Application",
        body_text=reflection.get("application", "")
    )
    img3_path = output_dir / "03-application.png"
    img3.save(img3_path)
    images.append(img3_path)
    print("✓ Generated 03-application.png")
    
    # 4. Prayer
    img4 = create_slide(
        letter="P",
        label="Prayer",
        body_text=reflection.get("prayer", "")
    )
    img4_path = output_dir / "04-prayer.png"
    img4.save(img4_path)
    images.append(img4_path)
    print("✓ Generated 04-prayer.png")
    
    return images


def upload_images(image_paths):
    """Upload images to CDN and return URLs."""
    urls = []
    for path in image_paths:
        try:
            result = upload_media(str(path))
            if result.get("success"):
                urls.append(result["url"])
                print(f"✓ Uploaded: {result['url']}")
            else:
                print(f"✗ Failed to upload {path}: {result}")
        except Exception as e:
            print(f"✗ Error uploading {path}: {e}")
    return urls


def build_caption(data, platform="facebook"):
    """Build caption for a given platform."""
    verse = data.get("verse", {})
    reference = verse.get('reference', '')
    text_snippet = verse.get('text', '')[:150]
    
    # Clean text — no emojis per brand guidelines
    lines = [
        f"Verse of the Day: {reference}",
        "",
        f'"{text_snippet}..."',
        "",
        "SOAP Reflection — swipe through the images for the full study!",
        "",
        "Which part of today's reflection resonates with you?",
        "",
        "Start journaling today! Download the SOAPaDay app and build your daily Bible study habit.",
        "",
        "https://SOAPaDay.com",
        "",
        f"#SOAPaDay #BibleStudy #DailyDevotional #{reference.replace(' ', '')} #FaithJournaling #ScriptureStudy"
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


def mark_posted(date_str=None):
    """Mark the pending verse as posted."""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    pending_file = WORKSPACE / "daily-soap" / "pending" / f"{date_str}.json"
    
    if pending_file.exists():
        with open(pending_file, 'r') as f:
            data = json.load(f)
        
        data["status"] = "posted"
        data["posted_at"] = datetime.now().isoformat()
        
        with open(pending_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ Marked {date_str} as posted")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="SOAPaDay Daily Automation")
    parser.add_argument("date", nargs="?", help="Date string YYYY-MM-DD (default: today)")
    args = parser.parse_args()
    
    date_str = args.date or datetime.now().strftime("%Y-%m-%d")
    
    print("=" * 50)
    print(f"SOAPaDay Daily Automation — {date_str}")
    print("=" * 50)
    
    # 1. Load approved reflection
    print("\n1. Loading approved reflection...")
    data = load_pending_data(date_str)
    if not data:
        print("   No approved reflection found. Exiting.")
        sys.exit(1)
    
    verse = data.get("verse", {})
    print(f"   Verse: {verse.get('reference', 'N/A')}")
    
    # Validate reflection content exists
    reflection = data.get("reflection", {})
    required_fields = ["observation", "application", "prayer"]
    missing = [f for f in required_fields if not reflection.get(f, "").strip()]
    if missing:
        print(f"   ❌ Missing reflection content: {', '.join(missing)}")
        print("   Aborting to prevent empty images.")
        sys.exit(1)
    print("   ✓ Reflection content validated")
    
    # 2. Create images
    print("\n2. Creating share images...")
    image_paths = create_share_images(data)
    print(f"   Created {len(image_paths)} images")
    
    # 3. Upload images
    print("\n3. Uploading images...")
    image_urls = upload_images(image_paths)
    print(f"   Uploaded {len(image_urls)} images")
    
    if len(image_urls) != 4:
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
