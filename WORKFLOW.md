# SOAPaDay Content Workflow

## Daily Content Posting Workflow

### Step 1: Review Calendar
Check `marketing/calendar-2026-07.md` for today's post type:
- **Mon/Wed/Fri:** Daily SOAP (S-O-A-P study)
- **Tue/Thu/Sat/Sun:** Hook Post (engagement/discovery)

### Step 2: Generate Content
**For Daily SOAP:**
1. Run `scripts/daily-soap-fetch.py` to get verse
2. Generate reflection (Observation, Application, Prayer)
3. Save with `scripts/save-reflection.py`
4. Present to Johnny for approval

**For Hook Posts:**
1. Check calendar for topic
2. Generate hook text, verse, reflection
3. Present to Johnny for approval

### Step 3: Get Approval
Wait for explicit "yes" or "approve" from Johnny.

**Approval options:**
- **"yes"** → Proceed with posting
- **"skip"** → Cancel today's post
- **"edit: [new text]"** → Replace section and re-approve

### Step 4: Generate Images (Python/PIL)
**For Hook Posts:**
```bash
cd ~/.openclaw/workspace-soapaday
python3 scripts/generate-hook-posts.py
```

**For Daily SOAP:**
```bash
cd ~/.openclaw/workspace-soapaday
python3 scripts/daily-soap-automation.py
```

Images are saved to:
- Hook posts: `daily-soap/hook-examples/`
- Daily SOAP: `daily-soap/images/`

### Step 5: Upload Images to myChelper CDN
Buffer requires publicly accessible URLs. Use the myChelper image upload service:

```bash
cd ~/.openclaw/workspace-soapaday
python3 skills/instagram-poster/scripts/upload_media.py daily-soap/hook-examples/hook-xxx-01.png
python3 skills/instagram-poster/scripts/upload_media.py daily-soap/hook-examples/hook-xxx-02-verse.png
python3 skills/instagram-poster/scripts/upload_media.py daily-soap/hook-examples/hook-xxx-03-observation.png
python3 skills/instagram-poster/scripts/upload_media.py daily-soap/hook-examples/hook-xxx-04-cta.png
```

**Returns:** Public URL like `https://images.mychelper.com/api/images/get/marketing/social-media/posts/UUID.png`

### Step 6: Post to Facebook via Buffer
```bash
cd ~/.openclaw/workspace-soapaday
source .env

python3 skills/social-posting/scripts/post_to_buffer.py "Caption text" \
  --image-url "https://images.mychelper.com/api/images/get/.../01.png" \
  --image-url "https://images.mychelper.com/api/images/get/.../02.png" \
  --image-url "https://images.mychelper.com/api/images/get/.../03.png" \
  --image-url "https://images.mychelper.com/api/images/get/.../04.png" \
  --platform facebook
```

### Step 7: Confirm & Log
- Report Post ID back to Johnny
- Update calendar status to "posted"
- Log performance in `memory/social-images-performance.md`

---

## Quick Reference

### Scripts
| Script | Purpose |
|--------|---------|
| `scripts/daily-soap-fetch.py` | Fetch daily verse |
| `scripts/save-reflection.py` | Save SOAP reflection |
| `scripts/generate-hook-posts.py` | Generate hook post images |
| `scripts/daily-soap-automation.py` | Full Daily SOAP automation |
| `scripts/post-hook-to-facebook.py` | One-command hook post (experimental) |

### Upload
| Service | Command |
|---------|---------|
| myChelper CDN | `python3 skills/instagram-poster/scripts/upload_media.py <file>` |

### Post
| Platform | Command |
|----------|---------|
| Facebook | `python3 skills/social-posting/scripts/post_to_buffer.py "text" --image-url "url" --platform facebook` |

---

## Important Notes

1. **Always upload images first** — Buffer cannot access local files
2. **Never post without approval** — Wait for explicit "yes"
3. **Use Python/PIL for images** — No AI image generation needed
4. **Images are branded** — Warm cream background, deep navy text, sage accents

---

*Last updated: July 14, 2026*
