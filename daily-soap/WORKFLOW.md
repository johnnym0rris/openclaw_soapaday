# Daily SOAP Post Workflow

## Step 1: Fetch Verse (Cron)
- Cron runs `daily-soap-fetch.py` at scheduled time
- Saves verse to `pending/YYYY-MM-DD.json` with status `"pending"`
- Agent receives notification to generate reflection

## Step 2: Generate Reflection (Agent)
- Agent reads verse from pending file
- Agent generates SOAP reflection (Observation, Application, Prayer)
- **CRITICAL: Agent must save reflection using:**
  ```bash
  python3 scripts/save-reflection.py YYYY-MM-DD "observation text" "application text" "prayer text"
  ```
- Agent presents reflection to Johnny for approval

## Step 3: Approve & Post (Johnny + Automation)
- Johnny replies "yes" or "approve"
- Agent sets status to `"approved"` in pending file
- Agent runs `daily-soap-automation.py`

### What automation does:
1. ✅ Validates reflection content exists (observation, application, prayer)
2. Creates 4 branded images (S, O, A, P)
3. Uploads to CDN
4. Posts to Facebook via Buffer
5. Marks as `"posted"`

## Safety Checks
- **Validation gate**: Automation aborts if any reflection field is missing/empty
- **No auto-post**: Always requires explicit approval
- **Status tracking**: pending → approved → posted
