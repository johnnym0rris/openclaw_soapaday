# SOAPaDay scheduled jobs

Live copies of the gateway automations, saved so the prompt changes are not only in the local scheduler.

## SOAPaDay Daily SOAP (Every Day 7AM)

- Enabled: True
- Schedule: `0 7 * * *` America/Chicago
- Session: `isolated`

```
📖 [SOAPaDay] Daily verse-of-the-day SOAP

Every day at 7:00 AM America/Chicago is a verse-of-the-day SOAP, including Tuesday, Thursday, Saturday, and Sunday. Those days also get a separate noon hook post. Do not skip this SOAP, and do not turn it into a hook post.

Do this once, then stop:

1. Run:
   python3 /home/openclaw/.openclaw/workspace-soapaday/scripts/daily-soap-fetch.py
   Use the date in the pending filename it prints. That file is the verse. Do not look up a content calendar.
2. Write one Observation, one Application, and one Prayer for that verse.
3. Save them with the date from step 1:
   python3 /home/openclaw/.openclaw/workspace-soapaday/scripts/save-reflection.py YYYY-MM-DD "observation" "application" "prayer"
4. Send Johnny this draft and wait:

📖 Verse of the Day: [Reference]
"[Verse text]"

📝 SOAP Reflection:
Observation: [observation]
Application: [application]
Prayer: [prayer]

Approval options:
• "yes" or "approve" → run python3 /home/openclaw/.openclaw/workspace-soapaday/scripts/daily-soap-automation.py YYYY-MM-DD
• "skip" → cancel today's post
• "edit: [new text]" → replace that section, save again, and show the draft again

Do not post, generate images, or run daily-soap-automation.py in this run. That happens only after an explicit yes.

If a script prints an error, send that error and stop. Do not search the filesystem, retry with a different command, or hunt for files.
```

## SOAPaDay Hook Post (Tue/Thu/Sat/Sun)

- Enabled: True
- Schedule: `0 12 * * 0,2,4,6` America/Chicago
- Session: `session:agent:soapaday:telegram:direct:8357925729`

```
📖 **[SOAPaDay] Hook Post - Step 1: Review**

Today is a **Hook Post day** (Tue/Thu/Sat/Sun).

1. Check the content calendar at `~/.openclaw/workspace-soapaday/marketing/calendar-2026-10.md` for today's hook topic
2. Generate the hook post content based on the topic and hook type:
   - **"Read this if..."** (4 images): hook_text, subtext, verse_reference, verse_text, reflection
   - **"3 verses when..."** (5 images): hook_text, verses[3] with reference+text
   - **"A prayer for..."** (3 images): hook_text, subtext, prayer
   - **"What this means"** (4 images): hook_text, verse_reference, verse_text, misconception, actual_meaning
3. Save hook content using: `python3 scripts/save-hook-post.py YYYY-MM-DD <hook_type> '<json_content>'`
4. Present to Johnny for approval in this format:

**Hook Post Draft — [Topic]**

**Format:** [N]-card carousel

**Card 1 — Hook:**
[hook text]

**Card 2 — [Content]:**
[content]

**Card 3 — CTA:**
[cta text]

**Caption:**
[caption text]

**Approval options:**
• **"yes"** or **"approve"** → Run `python3 scripts/hook-post-automation.py YYYY-MM-DD` to generate images, upload, and post to Facebook + Instagram
• **"skip"** → Cancel today's post
• **"edit: [new text]"** → Replace a section

Do NOT post without explicit approval.

Current time: Check calendar for today's date and post type.
```

## Removed or stopped

- Friday Instagram resurface was removed.
- Wednesday Instagram Reel Reminder is disabled. It spent $8.24 on 2026-09-30 by searching the disk for an mp4 in a loop.
