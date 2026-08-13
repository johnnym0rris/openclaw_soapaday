---
name: content-calendar
description: Generate and manage 30-day content calendars for SOAPaDay social media. Use when the user needs a content plan, posting schedule, content matrix, hashtag strategy, or monthly campaign outline for the Bible journaling app.
---

# Content Calendar — SOAPaDay

Generate structured content calendars and content matrices for SOAPaDay's social media growth.

## When to Use

- "Create a 30-day content calendar"
- "Plan next week's Instagram posts"
- "Build a content matrix for launch"
- "What should we post this month?"

## Content Pillars

Rotate through these pillars across the calendar:

| Pillar | % of Content | Examples |
|--------|-------------|----------|
| **Habit Formation** | 30% | "Why 10 minutes beats an hour", morning routine posts |
| **SOAP Framework** | 25% | Daily prompts, framework explainer, example studies |
| **Aesthetic Inspiration** | 25% | Journaling setups, verse graphics, Pinterest templates |
| **Community & Stories** | 10% | User journeys (real only!), faith community content |
| **Product/CTA** | 10% | App features, download prompts, launch announcements |

## 30-Day Calendar Template

Save generated calendars to `marketing/calendar-YYYY-MM.md`.

```markdown
# SOAPaDay Content Calendar — [Month Year]

## Week 1: [Theme]

| Day | Platform | Pillar | Format | Hook/Topic | Status |
|-----|----------|--------|--------|------------|--------|
| Mon | Instagram | Habit | Reel | "What 30 days of SOAP looks like" | draft |
| Tue | Instagram | SOAP | Carousel | "S is for Scripture — here's how" | draft |
| Wed | Pinterest | Aesthetic | Pin | Verse graphic — Psalm 119:105 | draft |
| Thu | Instagram | Community | Reel | "Morning routines that changed my faith" | draft |
| Fri | Instagram | Habit | Story | Poll — "What's your biggest Bible study challenge?" | draft |
| Sat | TikTok | Aesthetic | Video | Trending journaling aesthetic + SOAP overlay | draft |
| Sun | Instagram | SOAP | Feed | Weekly SOAP prompt with scripture | draft |

## Week 2: [Theme]
...

## Hashtag Rotation
- Week 1: Primary set (see brand/hashtags.md)
- Week 2: Journaling set
- Week 3: SOAP framework set
- Week 4: Wellness + faith set
```

## Workflow

### 1. Research Trends

Before building the calendar, search for current trends:
```
web_search: "trending Bible journaling aesthetics TikTok 2026"
web_search: "Christian faith content Instagram trends"
```

Review `brand/hashtags.md` for curated tags.

### 2. Generate Calendar

1. Ask Johnny for the month/theme focus (or infer from context)
2. Fill the 30-day template with specific hooks and formats
3. Balance pillars according to the percentages above
4. Include scripture references for `/scripture` content days
5. Save to `marketing/calendar-YYYY-MM.md`

### 3. Generate Daily Drafts

For each calendar entry marked "draft":
1. Write full post copy (platform-appropriate)
2. Suggest image/video direction
3. Save to `social-posts/YYYY-MM-DD-platform-topic.md`
4. Present batch to Johnny for review

### 4. Track Status

Update calendar status column:
- `draft` → content written, awaiting review
- `approved` → Johnny approved, ready to schedule
- `scheduled` → sent to Buffer with date
- `posted` → live on platform
- `skipped` → replaced or cancelled

## Content Matrix (Quick Reference)

For rapid brainstorming, use this matrix:

|  | Reel | Carousel | Static | Story |
|--|------|----------|--------|-------|
| **Habit** | Morning routine timelapse | "5 reasons you skip devotions" | Quote card | Poll/quiz |
| **SOAP** | Framework explainer | Step-by-step guide | Daily prompt | Behind-the-scenes |
| **Aesthetic** | Journaling setup tour | Template showcase | Verse graphic | Aesthetic mood board |
| **Community** | Testimonial (real!) | User journey | Encouragement post | Q&A |
| **Product** | App demo | Feature highlight | Download CTA | Countdown/launch |

## Seasonal Opportunities

| Period | Theme Ideas |
|--------|------------|
| January | New Year habits, fresh start with God |
| Lent | Reflection, sacrifice, deeper study |
| Easter | Resurrection, renewal, hope |
| Back to School | New routines, family faith |
| Thanksgiving | Gratitude journaling |
| Advent/Christmas | Anticipation, daily devotion series |

## Best Practices

- Never schedule more than 1 post per day per platform initially
- Batch-create content weekly, not daily (more efficient)
- Leave 2–3 slots open per week for trend-reactive content
- Review and adjust calendar mid-month based on performance
- All content must pass brand voice checklist (`brand/voice.md`)

## Templates

See `templates/30-day-calendar.md` for a blank template to copy.
