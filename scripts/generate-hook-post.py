#!/usr/bin/env python3
"""
Generate hook post images for SOAPaDay
Reads approved hook post data from pending file and creates branded images

Uses the same design system as daily-soap-automation.py for consistency:
- 1080x1350 canvas (same as VOTD images)
- Proper vertical centering
- Consistent fonts and spacing
- Watermark at bottom

Usage:
  python3 generate-hook-post.py                    # Process today's pending hook
  python3 generate-hook-post.py 2026-07-25         # Process specific date

Hook Types Supported:
  - "read_this_if"     : 4 images (hook, verse, reflection, cta)
  - "3_verses_when"    : 5 images (hook, verse1, verse2, verse3, cta)
  - "a_prayer_for"     : 3 images (hook, prayer, cta)
  - "what_this_means"  : 4 images (hook, verse, vs, cta)
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap

WORKSPACE = Path(__file__).resolve().parents[1]

# Same design constants as daily-soap-automation.py
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
    'body_italic': ['/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'],  # No italic available, use regular
    'ui': ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'],
    'ui_semi': ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'],
}


def get_font(style, size):
    """Load font with fallback."""
    for path in font_paths.get(style, font_paths['ui']):
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
    return ImageFont.load_default()


def add_watermark(draw):
    """Add SOAPaDay watermark at bottom of image."""
    scale = 1.0
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


def create_header(draw, letter, label, content_x=PADDING_H, content_y=PADDING_TOP):
    """Create S/O/A/P header with letter and label."""
    scale = 1.0
    letter_font = get_font('display', int(44 * scale))
    label_font = get_font('ui_semi', int(24 * scale))
    
    draw.text((content_x, content_y), letter, font=letter_font, fill=PRIMARY_COLOR)
    letter_bbox = draw.textbbox((0, 0), letter, font=letter_font)
    letter_width = letter_bbox[2] - letter_bbox[0]
    
    label_x = content_x + letter_width + int(16 * scale)
    draw.text((label_x, content_y + 4), label.upper(), font=label_font, fill=ON_SURFACE_VARIANT)
    
    header_height = int(48 * scale) + int(28 * scale)
    return header_height


def create_content_slide(letter, label, body_text, is_scripture=False, 
                         reference=None, translation=None, is_italic=False):
    """Create a standard content slide with vertical centering."""
    img = Image.new('RGB', (CANVAS_WIDTH, CANVAS_HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)
    scale = 1.0
    
    content_x = PADDING_H
    content_y = PADDING_TOP
    content_width = CANVAS_WIDTH - (PADDING_H * 2)
    content_height = CANVAS_HEIGHT - PADDING_TOP - PADDING_BOTTOM
    
    # Header
    header_height = create_header(draw, letter, label, content_x, content_y)
    
    # Body font selection
    if is_italic:
        body_font = get_font('body_italic', int(48 * scale))
    elif is_scripture:
        body_font = get_font('body', int(48 * scale))
    else:
        body_font = get_font('ui', int(48 * scale))
    
    body_color = ON_SURFACE_COLOR
    
    # Wrap text
    char_width = int(24 * scale)
    max_chars = content_width // char_width
    wrapped_lines = textwrap.wrap(body_text, width=max_chars)
    
    # Vertical centering with tighter line height
    line_height = int(62 * scale)
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
    
    # Reference for scripture
    if reference and is_scripture:
        ref_y = current_y + int(40 * scale)
        ref_font = get_font('display', int(30 * scale))
        draw.text((content_x, ref_y), reference, font=ref_font, fill=PRIMARY_COLOR)
        
        if translation:
            trans_y = ref_y + int(38 * scale) + int(8 * scale)
            trans_font = get_font('ui', int(22 * scale))
            draw.text((content_x, trans_y), translation, font=trans_font, fill=ON_SURFACE_VARIANT)
    
    # Watermark
    add_watermark(draw)
    
    return img


def create_hook_card(hook_text, subtext=None):
    """Bold hook statement card with centered text."""
    img = Image.new('RGB', (CANVAS_WIDTH, CANVAS_HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)
    scale = 1.0
    
    # Decorative line at top
    draw.rectangle([PADDING_H, 60, CANVAS_WIDTH - PADDING_H, 64], fill=PRIMARY_COLOR)
    
    # Main hook text - large and centered
    hook_font = get_font('display', int(72 * scale))
    
    # Wrap text to fit
    max_chars = 20
    lines = textwrap.wrap(hook_text, width=max_chars)
    
    line_height = int(90 * scale)
    total_height = len(lines) * line_height
    start_y = (CANVAS_HEIGHT - total_height) // 2 - 50
    
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=hook_font)
        width = bbox[2] - bbox[0]
        x = (CANVAS_WIDTH - width) // 2
        draw.text((x, start_y + i * line_height), line, font=hook_font, fill=ON_SURFACE_COLOR)
    
    # Subtext if provided
    if subtext:
        sub_font = get_font('ui', int(32 * scale))
        bbox = draw.textbbox((0, 0), subtext, font=sub_font)
        width = bbox[2] - bbox[0]
        x = (CANVAS_WIDTH - width) // 2
        draw.text((x, start_y + total_height + 40), subtext, font=sub_font, fill=ON_SURFACE_VARIANT)
    
    # Watermark
    add_watermark(draw)
    
    return img


def create_verse_card(reference, text, translation="NIV"):
    """Scripture verse card using standard content slide."""
    return create_content_slide(
        letter="S",
        label="Scripture",
        body_text=text,
        is_scripture=True,
        reference=reference,
        translation=translation
    )


def create_reflection_card(letter, label, text):
    """Observation/Application/Prayer card using standard content slide."""
    return create_content_slide(letter=letter, label=label, body_text=text)


def create_prayer_card(prayer_text):
    """Prayer card with italic styling."""
    return create_content_slide(
        letter="P",
        label="Prayer",
        body_text=prayer_text,
        is_italic=True
    )


def create_cta_card(cta_text="Start journaling today", subtext="Download the SOAPaDay app"):
    """Call-to-action card with centered layout."""
    img = Image.new('RGB', (CANVAS_WIDTH, CANVAS_HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)
    scale = 1.0
    
    # Calculate safe drawing area (above watermark)
    watermark_zone = 120
    safe_bottom = CANVAS_HEIGHT - PADDING_BOTTOM - watermark_zone
    center_y = (PADDING_TOP + safe_bottom) // 2
    max_text_width = CANVAS_WIDTH - (PADDING_H * 2)
    
    # Decorative line
    draw.rectangle([PADDING_H, 60, CANVAS_WIDTH - PADDING_H, 64], fill=PRIMARY_COLOR)
    
    # Helper: get font that fits text within max width
    def fit_font(text, style, start_size, min_size=24):
        font = get_font(style, start_size)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        while text_width > max_text_width and start_size > min_size:
            start_size -= 4
            font = get_font(style, start_size)
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
        return font, bbox[3] - bbox[1]
    
    # Measure all elements first (no drawing)
    cta_font, cta_height = fit_font(cta_text, 'display', 56)
    sub_font, sub_height = fit_font(subtext, 'ui', 32)
    url_font, url_height = fit_font("SOAPaDay.com", 'display', 64)
    tag_font, tag_height = fit_font("Free & Ad-Free Bible Journal", 'ui', 24)
    
    # Calculate total block height and center it
    gap = 24
    total_block = cta_height + gap + sub_height + gap + url_height + gap + tag_height
    start_y = center_y - total_block // 2
    
    # Draw elements centered
    bbox = draw.textbbox((0, 0), cta_text, font=cta_font)
    width = bbox[2] - bbox[0]
    x = (CANVAS_WIDTH - width) // 2
    draw.text((x, start_y), cta_text, font=cta_font, fill=ON_SURFACE_COLOR)
    
    bbox = draw.textbbox((0, 0), subtext, font=sub_font)
    width = bbox[2] - bbox[0]
    x = (CANVAS_WIDTH - width) // 2
    draw.text((x, start_y + cta_height + gap), subtext, font=sub_font, fill=ON_SURFACE_VARIANT)
    
    url = "SOAPaDay.com"
    bbox = draw.textbbox((0, 0), url, font=url_font)
    width = bbox[2] - bbox[0]
    x = (CANVAS_WIDTH - width) // 2
    draw.text((x, start_y + cta_height + gap + sub_height + gap), url, font=url_font, fill=PRIMARY_COLOR)
    
    tag = "Free & Ad-Free Bible Journal"
    bbox = draw.textbbox((0, 0), tag, font=tag_font)
    width = bbox[2] - bbox[0]
    x = (CANVAS_WIDTH - width) // 2
    draw.text((x, start_y + cta_height + gap + sub_height + gap + url_height + gap), tag, font=tag_font, fill=ON_SURFACE_VARIANT)
    
    # Watermark
    add_watermark(draw)
    
    return img


def create_vs_card(misconception, actual_meaning):
    """What people think vs what it means card."""
    img = Image.new('RGB', (CANVAS_WIDTH, CANVAS_HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)
    scale = 1.0
    
    # Title
    title_font = get_font('display', int(40 * scale))
    title = "What this verse actually means"
    bbox = draw.textbbox((0, 0), title, font=title_font)
    width = bbox[2] - bbox[0]
    x = (CANVAS_WIDTH - width) // 2
    draw.text((x, 80), title, font=title_font, fill=ON_SURFACE_COLOR)
    
    # Divider
    draw.rectangle([PADDING_H, 160, CANVAS_WIDTH - PADDING_H, 164], fill=PRIMARY_COLOR)
    
    # "What people think" section
    think_font = get_font('ui', int(24 * scale))
    draw.text((PADDING_H, 200), "WHAT PEOPLE THINK:", font=think_font, fill=ON_SURFACE_VARIANT)
    
    think_body = get_font('ui', int(32 * scale))
    lines = textwrap.wrap(misconception, width=36)
    for i, line in enumerate(lines):
        draw.text((PADDING_H, 250 + i*44), line, font=think_body, fill=ON_SURFACE_COLOR)
    
    # VS divider
    vs_y = 420
    draw.rectangle([PADDING_H, vs_y, CANVAS_WIDTH - PADDING_H, vs_y+2], fill="#E0E0E0")
    vs_font = get_font('display', int(28 * scale))
    bbox = draw.textbbox((0, 0), "VS", font=vs_font)
    width = bbox[2] - bbox[0]
    x = (CANVAS_WIDTH - width) // 2
    draw.text((x, vs_y-20), "VS", font=vs_font, fill=PRIMARY_COLOR)
    
    # "What it means" section
    mean_y = 480
    draw.text((PADDING_H, mean_y), "WHAT IT ACTUALLY MEANS:", font=think_font, fill=PRIMARY_COLOR)
    
    lines = textwrap.wrap(actual_meaning, width=36)
    for i, line in enumerate(lines):
        draw.text((PADDING_H, mean_y+50 + i*44), line, font=think_body, fill=ON_SURFACE_COLOR)
    
    # Watermark
    add_watermark(draw)
    
    return img


def load_hook_data(date_str=None):
    """Load approved hook post data from pending file."""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    pending_file = WORKSPACE / "daily-soap" / "pending-hooks" / f"{date_str}.json"
    
    if not pending_file.exists():
        print(f"No pending hook file found: {pending_file}")
        return None
    
    with open(pending_file, 'r') as f:
        data = json.load(f)
    
    if data.get("status") not in ["approved", "posted"]:
        print(f"Hook post not approved yet. Status: {data.get('status')}")
        return None
    
    return data


def generate_images(data):
    """Generate images based on hook type and content."""
    hook_type = data.get("hook_type", "")
    content = data.get("content", {})
    
    output_dir = WORKSPACE / "daily-soap" / "hook-images"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    images = []
    
    if hook_type == "read_this_if":
        # 4 images: hook, verse, reflection, cta
        img1 = create_hook_card(content["hook_text"], content.get("subtext"))
        img1_path = output_dir / "01-hook.png"
        img1.save(img1_path)
        images.append(img1_path)
        print("   ✓ 01-hook.png")
        
        img2 = create_verse_card(
            content["verse_reference"],
            content["verse_text"],
            content.get("translation", "NIV")
        )
        img2_path = output_dir / "02-verse.png"
        img2.save(img2_path)
        images.append(img2_path)
        print("   ✓ 02-verse.png")
        
        img3 = create_reflection_card("O", "Observation", content["reflection"])
        img3_path = output_dir / "03-observation.png"
        img3.save(img3_path)
        images.append(img3_path)
        print("   ✓ 03-observation.png")
        
        img4 = create_cta_card()
        img4_path = output_dir / "04-cta.png"
        img4.save(img4_path)
        images.append(img4_path)
        print("   ✓ 04-cta.png")
    
    elif hook_type == "3_verses_when":
        # 5 images: hook, verse1, verse2, verse3, cta
        img1 = create_hook_card(content["hook_text"])
        img1_path = output_dir / "01-hook.png"
        img1.save(img1_path)
        images.append(img1_path)
        print("   ✓ 01-hook.png")
        
        verses = content.get("verses", [])
        for i, verse in enumerate(verses[:3], start=2):
            img = create_verse_card(
                verse["reference"],
                verse["text"],
                verse.get("translation", "NIV")
            )
            img_path = output_dir / f"0{i}-verse{i-1}.png"
            img.save(img_path)
            images.append(img_path)
            print(f"   ✓ 0{i}-verse{i-1}.png")
        
        img5 = create_cta_card("Study these in SOAPaDay", "Download the app")
        img5_path = output_dir / "05-cta.png"
        img5.save(img5_path)
        images.append(img5_path)
        print("   ✓ 05-cta.png")
    
    elif hook_type == "a_prayer_for":
        # 3 images: hook, prayer, cta
        img1 = create_hook_card(content["hook_text"], content.get("subtext"))
        img1_path = output_dir / "01-hook.png"
        img1.save(img1_path)
        images.append(img1_path)
        print("   ✓ 01-hook.png")
        
        img2 = create_prayer_card(content["prayer"])
        img2_path = output_dir / "02-prayer.png"
        img2.save(img2_path)
        images.append(img2_path)
        print("   ✓ 02-prayer.png")
        
        img3 = create_cta_card("Write your own prayers in SOAPaDay", "Download the app")
        img3_path = output_dir / "03-cta.png"
        img3.save(img3_path)
        images.append(img3_path)
        print("   ✓ 03-cta.png")
    
    elif hook_type == "what_this_means":
        # 4 images: hook, verse, vs, cta
        img1 = create_hook_card(content["hook_text"])
        img1_path = output_dir / "01-hook.png"
        img1.save(img1_path)
        images.append(img1_path)
        print("   ✓ 01-hook.png")
        
        img2 = create_verse_card(
            content["verse_reference"],
            content["verse_text"],
            content.get("translation", "NIV")
        )
        img2_path = output_dir / "02-verse.png"
        img2.save(img2_path)
        images.append(img2_path)
        print("   ✓ 02-verse.png")
        
        img3 = create_vs_card(content["misconception"], content["actual_meaning"])
        img3_path = output_dir / "03-vs.png"
        img3.save(img3_path)
        images.append(img3_path)
        print("   ✓ 03-vs.png")
        
        img4 = create_cta_card("Study with context in SOAPaDay", "Download the app")
        img4_path = output_dir / "04-cta.png"
        img4.save(img4_path)
        images.append(img4_path)
        print("   ✓ 04-cta.png")
    
    else:
        print(f"Unknown hook type: {hook_type}")
        return []
    
    return images


def mark_posted(date_str=None):
    """Mark the pending hook as posted."""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    pending_file = WORKSPACE / "daily-soap" / "pending-hooks" / f"{date_str}.json"
    
    if pending_file.exists():
        with open(pending_file, 'r') as f:
            data = json.load(f)
        
        data["status"] = "posted"
        data["posted_at"] = datetime.now().isoformat()
        
        with open(pending_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ Marked {date_str} hook as posted")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="SOAPaDay Hook Post Image Generator")
    parser.add_argument("date", nargs="?", help="Date string YYYY-MM-DD (default: today)")
    args = parser.parse_args()
    
    date_str = args.date or datetime.now().strftime("%Y-%m-%d")
    
    print("=" * 50)
    print(f"SOAPaDay Hook Post Generator — {date_str}")
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
    print(f"   Output: {WORKSPACE / 'daily-soap' / 'hook-images'}")
    
    # Return image paths for automation script
    return image_paths


if __name__ == "__main__":
    main()
