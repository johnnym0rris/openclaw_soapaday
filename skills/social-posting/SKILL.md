---
name: social-posting
description: Post approved SOAPaDay content to Facebook via Buffer API. Use when posting approved content to social media. Trigger ONLY after user explicitly approves a draft post. Instagram posting available once connected to Buffer.
---

# Social Posting — SOAPaDay

Post approved content to SOAPaDay's **Facebook** page via Buffer.

**Note:** Only Facebook is connected in Buffer for now. Draft Instagram/TikTok content separately; add `BUFFER_INSTAGRAM_PROFILE_ID` when ready.

## CRITICAL RULE

**NEVER post without explicit user approval.**
- Show the exact post content first
- Wait for explicit "yes, post it" or similar approval
- No assumptions, no "I thought you meant..."

## Prerequisites

Before posting, ensure Buffer is configured:
1. Copy `.env.example` to `.env` in workspace root
2. Set `BUFFER_ACCESS_TOKEN` and profile IDs (see `TOOLS.md`)
3. Profile IDs are read from environment variables

## Complete Workflow

### 1. Get Approval (Already Done)

Before using this skill, the user must have explicitly approved:
- Post text
- Image or video (if applicable)
- Platform (Facebook — only Buffer channel connected; Instagram when added)
- Schedule time (optional — defaults to immediate)

**Standard 3-step process:**
1. Draft post text → Get approval
2. Generate image/video → Get approval
3. Post to Buffer (this skill)

### 2. Generate Images (Python Script)

**For Hook Posts:** Use `scripts/generate-hook-posts.py`
- Generates branded carousel images using PIL (no AI needed)
- Saves to `daily-soap/hook-examples/`

**For Daily SOAP:** Use `scripts/daily-soap-automation.py`
- Generates S-O-A-P carousel images
- Fetches verse, creates reflection, generates images

### 3. Upload Images to myChelper Server

Buffer requires publicly accessible image URLs. Use the myChelper image upload service:

```bash
cd ~/.openclaw/workspace-soapaday
python3 skills/instagram-poster/scripts/upload_media.py <path-to-image>
```

**Returns:** Public URL like `https://images.mychelper.com/api/images/get/marketing/social-media/posts/UUID.png`

**Upload all carousel images and collect their URLs.**

### 4. Post to Buffer with Images

```python
from post_to_buffer import post_to_buffer

result = post_to_buffer(
    text="Your caption",
    image_urls=[
        "https://images.mychelper.com/api/images/get/.../image1.png",
        "https://images.mychelper.com/api/images/get/.../image2.png",
        "https://images.mychelper.com/api/images/get/.../image3.png",
        "https://images.mychelper.com/api/images/get/.../image4.png"
    ],
    platform="facebook"
)
```

**Command line:**
```bash
cd ~/.openclaw/workspace-soapaday
source .env

# Preview first
python3 skills/social-posting/scripts/post_to_buffer.py "Caption text" \
  --image-url "https://images.mychelper.com/.../image1.png" \
  --image-url "https://images.mychelper.com/.../image2.png" \
  --platform facebook --dry-run

# Post with multiple images
python3 skills/social-posting/scripts/post_to_buffer.py "Caption text" \
  --image-url "https://images.mychelper.com/.../image1.png" \
  --image-url "https://images.mychelper.com/.../image2.png" \
  --platform facebook
```

### 5. Validate Post

```python
from post_to_buffer import validate_post

validation = validate_post(text="Your post text", platform="facebook")
```

**Platform limits:**
- Instagram: 2,200 characters, images/videos < 8MB
- Facebook: 63,206 characters, images < 8MB

### 6. Report Back

Confirm the post was published:
- Post ID
- Platform
- Media used (if any)
- Scheduled time (if scheduled)

### 7. Log Performance

Review performance in `memory/social-images-performance.md` after 7 days.

## Complete Example: Hook Post

```bash
# 1. Generate images
cd ~/.openclaw/workspace-soapaday
python3 scripts/generate-hook-posts.py

# 2. Upload images
python3 skills/instagram-poster/scripts/upload_media.py daily-soap/hook-examples/hook-anxious-01.png
python3 skills/instagram-poster/scripts/upload_media.py daily-soap/hook-examples/hook-anxious-02-verse.png
python3 skills/instagram-poster/scripts/upload_media.py daily-soap/hook-examples/hook-anxious-03-observation.png
python3 skills/instagram-poster/scripts/upload_media.py daily-soap/hook-examples/hook-anxious-04-cta.png

# 3. Post to Buffer (with uploaded URLs)
python3 skills/social-posting/scripts/post_to_buffer.py "Your caption here" \
  --image-url "https://images.mychelper.com/api/images/get/.../01.png" \
  --image-url "https://images.mychelper.com/api/images/get/.../02.png" \
  --image-url "https://images.mychelper.com/api/images/get/.../03.png" \
  --image-url "https://images.mychelper.com/api/images/get/.../04.png" \
  --platform facebook
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Token expired | Refresh token in Buffer settings, update `.env` |
| Missing profile ID | Not configured | Set `BUFFER_FACEBOOK_PROFILE_ID` in `.env` |
| Validation failed | Text too long / media too big | Check platform limits |
| Image URL not accessible | Local file or private URL | Upload to myChelper server first |
| Upload failed | API key issue | Check `MYCHELPER-API-KEY` in upload_media.py |

## Integration

Works after content is approved:
1. **Draft post** → Get approval
2. **Generate images** (Python/PIL script) → Get approval
3. **Upload images** (myChelper server)
4. **Post to Buffer** (this skill)

**Never skip the approval step.**
