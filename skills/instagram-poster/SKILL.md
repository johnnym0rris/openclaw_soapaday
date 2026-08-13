---
name: instagram-poster
description: Post content to SOAPaDay's Instagram via Buffer API. Use when creating, scheduling, or publishing Instagram posts, Reels, or Stories. Trigger when the user wants to post to Instagram after explicit approval.
---

# Instagram Poster — SOAPaDay

Post content to SOAPaDay's Instagram through Buffer's API.

## Supported Content Types

| Type | Description | Metadata |
|------|-------------|----------|
| `reel` | Short-form video (up to 90s) | `type: "reel"`, `shouldShareToFeed: true/false` |
| `post` | Feed post (image or carousel) | `type: "post"` |
| `story` | 24-hour ephemeral content | `type: "story"` |

## Workflow

### 1. Prepare Media

Instagram requires media (image or video) for all posts.
- Provide a public URL for the media asset
- Max size: 8MB through Buffer
- Formats: JPG, PNG (images); MP4, MOV (video)

### 2. Format Caption

Instagram captions should be:
- Plain text only (NO markdown)
- Use emojis for emphasis (✨, 📖, 🙏)
- Use ALL CAPS for headings
- Use line breaks for spacing
- Max 2,200 characters
- Max 5 hashtags (quality over quantity — see `brand/hashtags.md`)

**Example:**
```
WHAT IF YOUR MORNING STARTED WITH ONE VERSE?

Most of us want to study the Bible daily.
But between work, family, and life — consistency feels impossible.

That's why we built SOAPaDay.
Scripture. Observation. Application. Prayer.
10 minutes. Every day.

✨ Try your first SOAP study — link in bio

#BibleJournaling #DailyDevotional #SOAPaDay
```

### 3. Post to Instagram

```python
import sys
sys.path.insert(0, 'skills/instagram-poster/scripts')
from post_to_buffer import post_to_buffer

result = post_to_buffer(
    text="Your caption here",
    video_url="https://...",  # For Reels
    platform="instagram",
    schedule_time="2026-07-01T09:00:00-05:00"  # Optional
)
```

### 4. Verify Post

Check Buffer dashboard or Instagram to confirm.

## References

- `references/buffer-api.md` — Buffer GraphQL API details
- `references/instagram-limits.md` — Platform limits and best practices

## Important Notes

- Instagram requires media for all posts
- Reels are the preferred format for video
- `shouldShareToFeed: true` shows Reels in main feed too
- Always strip markdown from captions
- First 3 seconds of video are critical
- NEVER post without explicit user approval
