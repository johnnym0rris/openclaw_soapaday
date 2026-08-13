#!/usr/bin/env python3
"""
Generate custom hook-style social media posts for SOAPaDay
"""
import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap

WORKSPACE = Path(__file__).resolve().parents[1]
OUTPUT_DIR = WORKSPACE / "daily-soap" / "hook-examples"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Brand colors
BG_COLOR = "#FAFAFA"
PRIMARY = "#1A5F4A"
TEXT_DARK = "#1C1B1F"
TEXT_MUTED = "#49454F"

CANVAS = (1080, 1080)
PADDING = 80


def get_font(style, size):
    """Load font with fallback."""
    paths = {
        'display': ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'],
        'body': ['/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'],
        'ui': ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'],
    }
    for path in paths.get(style, paths['ui']):
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
    return ImageFont.load_default()


def create_hook_card(hook_text, subtext=None):
    """Bold hook statement card."""
    img = Image.new('RGB', CANVAS, BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Decorative line at top
    draw.rectangle([PADDING, 60, CANVAS[0]-PADDING, 64], fill=PRIMARY)
    
    # Main hook text - large and centered
    hook_font = get_font('display', 72)
    
    # Wrap text to fit
    max_chars = 20
    lines = textwrap.wrap(hook_text, width=max_chars)
    
    line_height = 90
    total_height = len(lines) * line_height
    start_y = (CANVAS[1] - total_height) // 2 - 50
    
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=hook_font)
        width = bbox[2] - bbox[0]
        x = (CANVAS[0] - width) // 2
        draw.text((x, start_y + i * line_height), line, font=hook_font, fill=TEXT_DARK)
    
    # Subtext if provided
    if subtext:
        sub_font = get_font('ui', 32)
        bbox = draw.textbbox((0, 0), subtext, font=sub_font)
        width = bbox[2] - bbox[0]
        x = (CANVAS[0] - width) // 2
        draw.text((x, start_y + total_height + 40), subtext, font=sub_font, fill=TEXT_MUTED)
    
    # Branding at bottom
    brand_font = get_font('ui', 24)
    draw.text((PADDING, CANVAS[1]-60), "SOAPaDay.com", font=brand_font, fill=PRIMARY)
    
    return img


def create_verse_card(reference, text, translation="NIV"):
    """Scripture verse card."""
    img = Image.new('RGB', CANVAS, BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # S label
    label_font = get_font('display', 48)
    draw.text((PADDING, PADDING), "S", font=label_font, fill=PRIMARY)
    
    # Scripture label
    small_font = get_font('ui', 22)
    draw.text((PADDING+60, PADDING+12), "SCRIPTURE", font=small_font, fill=TEXT_MUTED)
    
    # Verse text
    verse_font = get_font('body', 40)
    max_chars = 32
    lines = textwrap.wrap(text, width=max_chars)
    
    line_height = 56
    total_height = len(lines) * line_height
    start_y = (CANVAS[1] - total_height) // 2
    
    for i, line in enumerate(lines):
        draw.text((PADDING, start_y + i * line_height), line, font=verse_font, fill=TEXT_DARK)
    
    # Reference
    ref_font = get_font('display', 30)
    draw.text((PADDING, start_y + total_height + 40), reference, font=ref_font, fill=PRIMARY)
    
    # Translation
    trans_font = get_font('ui', 20)
    draw.text((PADDING, start_y + total_height + 80), translation, font=trans_font, fill=TEXT_MUTED)
    
    return img


def create_reflection_card(letter, label, text):
    """Observation/Application/Prayer card."""
    img = Image.new('RGB', CANVAS, BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Letter label
    label_font = get_font('display', 48)
    draw.text((PADDING, PADDING), letter, font=label_font, fill=PRIMARY)
    
    small_font = get_font('ui', 22)
    draw.text((PADDING+60, PADDING+12), label.upper(), font=small_font, fill=TEXT_MUTED)
    
    # Body text
    body_font = get_font('ui', 36)
    max_chars = 34
    lines = textwrap.wrap(text, width=max_chars)
    
    line_height = 52
    total_height = len(lines) * line_height
    start_y = (CANVAS[1] - total_height) // 2
    
    for i, line in enumerate(lines):
        draw.text((PADDING, start_y + i * line_height), line, font=body_font, fill=TEXT_DARK)
    
    return img


def create_cta_card():
    """Call-to-action card."""
    img = Image.new('RGB', CANVAS, BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Decorative line
    draw.rectangle([PADDING, 60, CANVAS[0]-PADDING, 64], fill=PRIMARY)
    
    # Main text
    cta_font = get_font('display', 56)
    cta_text = "Start journaling today"
    bbox = draw.textbbox((0, 0), cta_text, font=cta_font)
    width = bbox[2] - bbox[0]
    x = (CANVAS[0] - width) // 2
    draw.text((x, 280), cta_text, font=cta_font, fill=TEXT_DARK)
    
    # Subtext
    sub_font = get_font('ui', 32)
    sub_text = "Download the SOAPaDay app"
    bbox = draw.textbbox((0, 0), sub_text, font=sub_font)
    width = bbox[2] - bbox[0]
    x = (CANVAS[0] - width) // 2
    draw.text((x, 380), sub_text, font=sub_font, fill=TEXT_MUTED)
    
    # URL - big and bold
    url_font = get_font('display', 64)
    url = "SOAPaDay.com"
    bbox = draw.textbbox((0, 0), url, font=url_font)
    width = bbox[2] - bbox[0]
    x = (CANVAS[0] - width) // 2
    draw.text((x, 520), url, font=url_font, fill=PRIMARY)
    
    # Tagline
    tag_font = get_font('ui', 24)
    tag = "Free & Ad-Free Bible Journal"
    bbox = draw.textbbox((0, 0), tag, font=tag_font)
    width = bbox[2] - bbox[0]
    x = (CANVAS[0] - width) // 2
    draw.text((x, 640), tag, font=tag_font, fill=TEXT_MUTED)
    
    return img


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 generate-custom-hook.py <topic> [hook_text] [verse_ref] [verse_text] [reflection] [cta_text]")
        sys.exit(1)
    
    topic = sys.argv[1]
    hook_text = sys.argv[2] if len(sys.argv) > 2 else f"Read this if you feel {topic}."
    verse_ref = sys.argv[3] if len(sys.argv) > 3 else ""
    verse_text = sys.argv[4] if len(sys.argv) > 4 else ""
    reflection = sys.argv[5] if len(sys.argv) > 5 else ""
    cta_text = sys.argv[6] if len(sys.argv) > 6 else "Start journaling today"
    
    print(f"Generating '{topic}' hook post...")
    
    # Card 1: Hook
    img1 = create_hook_card(hook_text, "A verse for when you feel invisible")
    img1.save(OUTPUT_DIR / f"hook-{topic}-01.png")
    print(f"   ✓ hook-{topic}-01.png")
    
    # Card 2: Verse
    if verse_ref and verse_text:
        img2 = create_verse_card(verse_ref, verse_text)
        img2.save(OUTPUT_DIR / f"hook-{topic}-02-verse.png")
        print(f"   ✓ hook-{topic}-02-verse.png")
    
    # Card 3: Reflection
    if reflection:
        img3 = create_reflection_card("O", "Observation", reflection)
        img3.save(OUTPUT_DIR / f"hook-{topic}-03-observation.png")
        print(f"   ✓ hook-{topic}-03-observation.png")
    
    # Card 4: CTA
    img4 = create_cta_card()
    img4.save(OUTPUT_DIR / f"hook-{topic}-04-cta.png")
    print(f"   ✓ hook-{topic}-04-cta.png")
    
    print(f"\n✅ Saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
