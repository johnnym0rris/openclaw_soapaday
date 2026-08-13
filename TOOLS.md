# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

---

## SOAPaDay Product

| Resource | Value |
|----------|-------|
| **App name** | SOAPaDay |
| **Tagline** | TBD — daily SOAP Bible study, one day at a time |
| **Website** | TBD |
| **App Store** | TBD |
| **Google Play** | TBD |

## Social Accounts

| Platform | Handle | Status |
|----------|--------|--------|
| Facebook | TBD | Connected via Buffer (posting enabled) |
| Instagram | TBD | Connected via Buffer (profile ID in `.env`) |
| TikTok | TBD | Not yet created |
| Pinterest | TBD | Not yet created |

## Buffer Integration

Buffer is used for scheduling approved posts. Credentials go in `.env` (never commit to git).

| Setting | Value |
|---------|-------|
| **API token** | Configured in `.env` |
| **Facebook profile ID** | Configured in `.env` (active) |
| **Instagram profile ID** | Configured in `.env` (active) |
| **LinkedIn profile ID** | Not connected yet |

**Default posting platform:** Both Facebook and Instagram (both Buffer channels connected)

When posting, use `--platform facebook`, `--platform instagram`, or `--platform both` (default).

## OpenClaw Instance

| Setting | Value |
|---------|-------|
| **Config** | `~/.openclaw/openclaw-soapaday.json` (via `OPENCLAW_CONFIG_PATH`) |
| **Workspace** | `~/.openclaw/workspace-soapaday/` |
| **Gateway port** | 18790 |
| **Telegram bot** | @soapaday_bot |
| **Model** | Kimi K2.6 (moonshot/kimi-k2.6) |
| **Service** | `openclaw-soapaday-gateway.service` |

## Persona Commands

| Command | Mode |
|---------|------|
| `/growth` | Growth Marketer (default) |
| `/content` | Creative Director |
| `/scripture` | Devotional Writer |
| `/gm` | Strategic Coordinator |

## Brand Assets

See `brand/` directory:
- `brand/voice.md` — tone and messaging guidelines
- `brand/colors.md` — color palette
- `brand/hashtags.md` — curated hashtag sets

---

*Last updated: 2026-06-28*
