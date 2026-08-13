---
name: social-image-generator
description: Generate branded social media images for SOAPaDay posts using AI (Gemini). Use when creating images for Instagram, Pinterest, or TikTok content. Trigger when the user needs a social media image, verse graphic, or journaling aesthetic visual.
---

# Social Image Generator — SOAPaDay

Generate warm, aesthetic social media images for SOAPaDay posts.

## Brand Reference

- Colors: see `brand/colors.md` (warm cream, deep navy, soft sage, warm gold)
- Voice: see `brand/voice.md`
- Aesthetic: warm, reflective, Bible journaling, soft natural light

## Image Generation (Gemini AI)

Use `image_generate` with prompts matching SOAPaDay's aesthetic.

**Prompt pattern:**
```
Create a [STYLE] image for a Bible journaling app called SOAPaDay.
Theme: [TOPIC]
Colors: warm cream (#FAF7F2) background, deep navy (#2C3E50) text, soft sage (#8BA888) accents, warm gold (#D4A574) highlights
Style: warm, reflective, aesthetic Bible journaling, soft natural lighting, minimalist
Text overlay: "[MAIN MESSAGE]" in clean readable font
Background: [DESCRIPTION — morning light, open journal, coffee, plants]
No fake brand names. Professional, mobile-friendly composition.
```

**Example prompts:**

**Daily Devotional:**
```
Create a warm aesthetic image of an open journal with handwritten notes beside a cup of coffee, soft morning light through a window.
Colors: warm cream background, deep navy text, sage green plant accent.
Minimal text overlay: "Today's SOAP" in elegant serif font.
Style: Pinterest-worthy Bible journaling aesthetic. No people.
```

**Verse Graphic:**
```
Create a beautiful scripture verse graphic with warm cream textured background.
Verse text: "Your word is a lamp to my feet" — Psalm 119:105
Typography: elegant serif, deep navy text, warm gold accent line.
Style: clean, shareable, Instagram-ready square format.
```

**Habit Formation:**
```
Create a flat illustration showing a phone with a Bible study app interface, next to an open physical journal.
Colors: warm cream, deep navy, soft sage accents.
Style: modern but warm, inviting, not corporate.
Text: "10 minutes. One verse. Every day."
```

## Video Generation (Instagram Reels)

**Gemini max video length: 5 seconds.** Request seamless looping.

**Prompt pattern:**
```
A warm, aesthetic scene of [SETTING — morning desk, cozy reading nook].
Soft natural lighting, Bible journaling aesthetic.
Text overlay or voiceover delivering: "[SCRIPT — max 15-20 words]"
IMPORTANT: Video must loop seamlessly. Smooth, subtle motion only.
```

**Settings:**
- `durationSeconds: 5`
- `aspectRatio: "9:16"` (Reels/TikTok)
- `filename: "reel-topic-date.mp4"`

## Complete Workflow

### 1. Draft Post First
Always draft the post text BEFORE generating the image. Get user approval on text first.

**Platform formatting:** NO markdown in social posts. Use plain text, ALL CAPS for emphasis, emojis, line breaks.

### 2. Generate Image
```python
image_generate(
    prompt="Your detailed SOAPaDay prompt...",
    outputFormat="jpeg",
    quality="high",
    timeoutMs=300000
)
```

### 3. Verify Before Using
- Spelling correct?
- Brand name "SOAPaDay" spelled correctly?
- No fake competitor names or logos?
- Readable at mobile size?

### 4. Show for Approval
Present the generated image. Wait for explicit approval.

### 5. Post (After Approval)
Use social-posting or instagram-poster skill with the image URL.

## Image Size Guide

| Platform | Size | Aspect Ratio |
|----------|------|--------------|
| Instagram feed | 1080x1080 | 1:1 |
| Instagram Reels/Stories | 1080x1920 | 9:16 |
| Pinterest pin | 1000x1500 | 2:3 |
| TikTok | 1080x1920 | 9:16 |

## Best Practices

- Always draft post BEFORE generating image
- Image should magnify the post's main point
- Keep text concise (2–3 lines max on images)
- Save with descriptive filenames: `theme-topic-date.jpg`
- Always get explicit approval before posting
- Log experiments in `memory/social-images-performance.md`
