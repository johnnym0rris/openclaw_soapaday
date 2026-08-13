#!/usr/bin/env python3
"""
Generate hook-style social media posts for SOAPaDay
DEPRECATED: This script generates hardcoded example posts.

Use the new parameterized workflow instead:
  1. save-hook-post.py       - Save hook content to pending file
  2. generate-hook-post.py   - Generate images from approved pending file
  3. hook-post-automation.py - Full automation (images + upload + post)

This script is kept for backward compatibility and generating example templates.
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
    
    draw.rectangle([PADDING, 60, CANVAS[0]-PADDING, 64], fill=PRIMARY)
    
    hook_font = get_font('display', 72)
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
    
    if subtext:
        sub_font = get_font('ui', 32)
        bbox = draw.textbbox((0, 0), subtext, font=sub_font)
        width = bbox[2] - bbox[0]
        x = (CANVAS[0] - width) // 2
        draw.text((x, start_y + total_height + 40), subtext, font=sub_font, fill=TEXT_MUTED)
    
    brand_font = get_font('ui', 24)
    draw.text((PADDING, CANVAS[1]-60), "SOAPaDay.com", font=brand_font, fill=PRIMARY)
    
    return img


def create_verse_card(reference, text, translation="NIV"):
    """Scripture verse card."""
    img = Image.new('RGB', CANVAS, BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    label_font = get_font('display', 48)
    draw.text((PADDING, PADDING), "S", font=label_font, fill=PRIMARY)
    
    small_font = get_font('ui', 22)
    draw.text((PADDING+60, PADDING+12), "SCRIPTURE", font=small_font, fill=TEXT_MUTED)
    
    verse_font = get_font('body', 40)
    max_chars = 32
    lines = textwrap.wrap(text, width=max_chars)
    
    line_height = 56
    total_height = len(lines) * line_height
    start_y = (CANVAS[1] - total_height) // 2
    
    for i, line in enumerate(lines):
        draw.text((PADDING, start_y + i * line_height), line, font=verse_font, fill=TEXT_DARK)
    
    ref_font = get_font('display', 30)
    draw.text((PADDING, start_y + total_height + 40), reference, font=ref_font, fill=PRIMARY)
    
    trans_font = get_font('ui', 20)
    draw.text((PADDING, start_y + total_height + 80), translation, font=trans_font, fill=TEXT_MUTED)
    
    return img


def create_reflection_card(letter, label, text):
    """Observation/Application/Prayer card."""
    img = Image.new('RGB', CANVAS, BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    label_font = get_font('display', 48)
    draw.text((PADDING, PADDING), letter, font=label_font, fill=PRIMARY)
    
    small_font = get_font('ui', 22)
    draw.text((PADDING+60, PADDING+12), label.upper(), font=small_font, fill=TEXT_MUTED)
    
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
    
    draw.rectangle([PADDING, 60, CANVAS[0]-PADDING, 64], fill=PRIMARY)
    
    cta_font = get_font('display', 56)
    cta_text = "Start journaling today"
    bbox = draw.textbbox((0, 0), cta_text, font=cta_font)
    width = bbox[2] - bbox[0]
    x = (CANVAS[0] - width) // 2
    draw.text((x, 280), cta_text, font=cta_font, fill=TEXT_DARK)
    
    sub_font = get_font('ui', 32)
    sub_text = "Download the SOAPaDay app"
    bbox = draw.textbbox((0, 0), sub_text, font=sub_font)
    width = bbox[2] - bbox[0]
    x = (CANVAS[0] - width) // 2
    draw.text((x, 380), sub_text, font=sub_font, fill=TEXT_MUTED)
    
    url_font = get_font('display', 64)
    url = "SOAPaDay.com"
    bbox = draw.textbbox((0, 0), url, font=url_font)
    width = bbox[2] - bbox[0]
    x = (CANVAS[0] - width) // 2
    draw.text((x, 520), url, font=url_font, fill=PRIMARY)
    
    tag_font = get_font('ui', 24)
    tag = "Free & Ad-Free Bible Journal"
    bbox = draw.textbbox((0, 0), tag, font=tag_font)
    width = bbox[2] - bbox[0]
    x = (CANVAS[0] - width) // 2
    draw.text((x, 640), tag, font=tag_font, fill=TEXT_MUTED)
    
    return img


def create_vs_card(misconception, actual_meaning):
    """What people think vs what it means card."""
    img = Image.new('RGB', CANVAS, BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    title_font = get_font('display', 40)
    title = "What this verse actually means"
    bbox = draw.textbbox((0, 0), title, font=title_font)
    width = bbox[2] - bbox[0]
    x = (CANVAS[0] - width) // 2
    draw.text((x, 80), title, font=title_font, fill=TEXT_DARK)
    
    draw.rectangle([PADDING, 160, CANVAS[0]-PADDING, 164], fill=PRIMARY)
    
    think_font = get_font('ui', 24)
    draw.text((PADDING, 200), "WHAT PEOPLE THINK:", font=think_font, fill=TEXT_MUTED)
    
    think_body = get_font('ui', 32)
    lines = textwrap.wrap(misconception, width=36)
    for i, line in enumerate(lines):
        draw.text((PADDING, 250 + i*44), line, font=think_body, fill=TEXT_DARK)
    
    vs_y = 420
    draw.rectangle([PADDING, vs_y, CANVAS[0]-PADDING, vs_y+2], fill="#E0E0E0")
    vs_font = get_font('display', 28)
    bbox = draw.textbbox((0, 0), "VS", font=vs_font)
    width = bbox[2] - bbox[0]
    x = (CANVAS[0] - width) // 2
    draw.text((x, vs_y-20), "VS", font=vs_font, fill=PRIMARY)
    
    mean_y = 480
    draw.text((PADDING, mean_y), "WHAT IT ACTUALLY MEANS:", font=think_font, fill=PRIMARY)
    
    lines = textwrap.wrap(actual_meaning, width=36)
    for i, line in enumerate(lines):
        draw.text((PADDING, mean_y+50 + i*44), line, font=think_body, fill=TEXT_DARK)
    
    return img


def main():
    print("=" * 60)
    print("DEPRECATED: generate-hook-posts.py")
    print("=" * 60)
    print("This script generates hardcoded example posts.")
    print("")
    print("For production hook posts, use the new workflow:")
    print("  1. save-hook-post.py <date> <type> <json>")
    print("  2. generate-hook-post.py [date]")
    print("  3. hook-post-automation.py [date]")
    print("=" * 60)
    print("")
    print("Generating example templates anyway...")
    print("")
    
    # Example 1: "Read this if you're anxious"
    print("1. 'Read this if you're anxious' post (4 images)")
    
    img1 = create_hook_card("Read this if you're anxious.", "A verse for when worry takes over")
    img1.save(OUTPUT_DIR / "hook-anxious-01.png")
    print("   ✓ 01-hook.png")
    
    img2 = create_verse_card(
        "Philippians 4:6-7",
        "Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God."
    )
    img2.save(OUTPUT_DIR / "hook-anxious-02-verse.png")
    print("   ✓ 02-verse.png")
    
    img3 = create_reflection_card(
        "O",
        "Observation",
        "Anxiety isn't dismissed — it's redirected. Paul doesn't say 'stop worrying because it's bad.' He says bring it to God. The peace that follows isn't based on circumstances changing, but on entrusting them to One who is greater."
    )
    img3.save(OUTPUT_DIR / "hook-anxious-03-observation.png")
    print("   ✓ 03-observation.png")
    
    img4 = create_cta_card()
    img4.save(OUTPUT_DIR / "hook-anxious-04-cta.png")
    print("   ✓ 04-cta.png")
    
    # Example 2: "What this verse actually means"
    print("\n2. 'What this verse actually means' post (4 images)")
    
    img1 = create_hook_card("What Jeremiah 29:11 actually means.")
    img1.save(OUTPUT_DIR / "hook-meaning-01.png")
    print("   ✓ 01-hook.png")
    
    img2 = create_verse_card(
        "Jeremiah 29:11",
        "For I know the plans I have for you, declares the Lord, plans to prosper you and not to harm you, plans to give you hope and a future."
    )
    img2.save(OUTPUT_DIR / "hook-meaning-02-verse.png")
    print("   ✓ 02-verse.png")
    
    img3 = create_vs_card(
        "God promises me a future full of success, wealth, and easy times.",
        "This was written to exiles in Babylon. 'Prosper' (shalom) means wholeness, not wealth. The promise is about God's faithfulness through suffering — not a guarantee of comfort."
    )
    img3.save(OUTPUT_DIR / "hook-meaning-03-vs.png")
    print("   ✓ 03-vs.png")
    
    img4 = create_cta_card()
    img4.save(OUTPUT_DIR / "hook-meaning-04-cta.png")
    print("   ✓ 04-cta.png")
    
    # Example 3: "Three verses when you feel overwhelmed"
    print("\n3. 'Three verses when overwhelmed' post (5 images)")
    
    img1 = create_hook_card("3 verses when you feel overwhelmed.")
    img1.save(OUTPUT_DIR / "hook-3verses-01.png")
    print("   ✓ 01-hook.png")
    
    img2 = create_verse_card("Matthew 11:28", "Come to me, all you who are weary and burdened, and I will give you rest.")
    img2.save(OUTPUT_DIR / "hook-3verses-02.png")
    print("   ✓ 02-verse1.png")
    
    img3 = create_verse_card("Psalm 61:2", "When my heart is overwhelmed, lead me to the rock that is higher than I.")
    img3.save(OUTPUT_DIR / "hook-3verses-03.png")
    print("   ✓ 03-verse2.png")
    
    img4 = create_verse_card("Isaiah 41:10", "Do not fear, for I am with you; do not be dismayed, for I am your God.")
    img4.save(OUTPUT_DIR / "hook-3verses-04.png")
    print("   ✓ 04-verse3.png")
    
    img5 = create_cta_card()
    img5.save(OUTPUT_DIR / "hook-3verses-05-cta.png")
    print("   ✓ 05-cta.png")
    
    # Example 4: "A prayer for today"
    print("\n4. 'A prayer for today' post (3 images)")
    
    img1 = create_hook_card("A prayer for today.", "For when you don't have the words")
    img1.save(OUTPUT_DIR / "hook-prayer-01.png")
    print("   ✓ 01-hook.png")
    
    img2 = create_reflection_card(
        "P",
        "Prayer",
        "Lord, today I surrender what I cannot control. Help me to trust Your timing more than my own understanding. Give me peace that passes understanding, and courage to walk in faith even when the path is unclear. Amen."
    )
    img2.save(OUTPUT_DIR / "hook-prayer-02-prayer.png")
    print("   ✓ 02-prayer.png")
    
    img3 = create_cta_card()
    img3.save(OUTPUT_DIR / "hook-prayer-03-cta.png")
    print("   ✓ 03-cta.png")
    
    print(f"\n✅ All examples saved to: {OUTPUT_DIR}")
    print("\n⚠️  Remember: These are TEMPLATES, not production posts.")
    print("   Use save-hook-post.py for real content.")


if __name__ == "__main__":
    main()
