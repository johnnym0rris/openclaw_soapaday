#!/usr/bin/env python3
"""
SOAPaDay Buffer Social Media Poster
Posts to Instagram and Facebook via Buffer API.
Credentials from .env: BUFFER_ACCESS_TOKEN, BUFFER_*_PROFILE_ID
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[3]
ENV_FILE = WORKSPACE / ".env"


def load_env():
    """Load .env file if present."""
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())


load_env()

PLATFORM_PROFILES = {
    "instagram": os.environ.get("BUFFER_INSTAGRAM_PROFILE_ID", ""),
    "facebook": os.environ.get("BUFFER_FACEBOOK_PROFILE_ID", ""),
}

PLATFORM_METADATA = {
    "facebook": {"facebook": {"type": "post"}},
    "instagram": {"instagram": {"type": "reel", "shouldShareToFeed": True}},
}

PLATFORM_LIMITS = {
    "facebook": {"max_chars": 63206, "max_image_size_mb": 8},
    "instagram": {"max_chars": 2200, "max_image_size_mb": 8},
}


def get_token():
    token = os.environ.get("BUFFER_ACCESS_TOKEN", "")
    if not token:
        raise ValueError(
            "BUFFER_ACCESS_TOKEN not set. Copy .env.example to .env and add your token."
        )
    return token


def get_profile_id(platform):
    platform = platform.lower()
    if platform not in PLATFORM_PROFILES:
        raise ValueError(f"Unknown platform: {platform}. Use: {list(PLATFORM_PROFILES.keys())}")
    profile_id = PLATFORM_PROFILES[platform]
    if not profile_id:
        raise ValueError(
            f"Profile ID for {platform} not set. "
            f"Set BUFFER_{platform.upper()}_PROFILE_ID in .env"
        )
    return profile_id


def validate_post(text, platform, image_path=None):
    errors = []
    platform = platform.lower()

    if platform not in PLATFORM_LIMITS:
        return {"valid": False, "errors": [f"Unknown platform: {platform}"]}

    limits = PLATFORM_LIMITS[platform]

    if len(text) > limits["max_chars"]:
        errors.append(f"Text too long: {len(text)} chars (max: {limits['max_chars']})")

    if image_path and os.path.exists(image_path):
        size_mb = os.path.getsize(image_path) / (1024 * 1024)
        if size_mb > limits["max_image_size_mb"]:
            errors.append(f"Image too large: {size_mb:.1f}MB (max: {limits['max_image_size_mb']}MB)")

    return {"valid": len(errors) == 0, "errors": errors}


def preview_post(text, image_url=None, platform="facebook"):
    profile_id = get_profile_id(platform)
    validation = validate_post(text, platform)

    lines = [
        "=" * 50,
        "POST PREVIEW (Dry Run)",
        "=" * 50,
        f"Platform: {platform.title()}",
        f"Profile ID: {profile_id}",
        f"Image: {image_url or 'None'}",
        f"Character count: {len(text)}",
        "",
        "--- Text ---",
        text[:200] + "..." if len(text) > 200 else text,
        "",
    ]

    if validation["valid"]:
        lines.append("Validation: PASSED")
    else:
        lines.append("Validation: FAILED")
        for error in validation["errors"]:
            lines.append(f"   - {error}")

    lines.append("=" * 50)
    return "\n".join(lines)


def post_to_buffer(
    text,
    image_url=None,
    video_url=None,
    platform="facebook",
    schedule_time=None,
    max_retries=3,
    token=None,
):
    token = token or get_token()
    profile_id = get_profile_id(platform)

    if schedule_time:
        mode = "customScheduled"
    else:
        mode = "shareNow"

    variables = {
        "input": {
            "text": text,
            "channelId": profile_id,
            "schedulingType": "automatic",
            "mode": mode,
            "metadata": PLATFORM_METADATA.get(platform, {}),
        }
    }

    if schedule_time:
        variables["input"]["dueAt"] = schedule_time

    if video_url:
        variables["input"]["assets"] = [{"video": {"url": video_url}}]
    elif image_url:
        variables["input"]["assets"] = [{"image": {"url": image_url}}]

    query = """mutation CreatePost($input: CreatePostInput!) {
  createPost(input: $input) {
    ... on PostActionSuccess {
      post { id text status dueAt }
    }
    ... on MutationError {
      message
    }
  }
}"""

    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")

    req = urllib.request.Request(
        "https://api.buffer.com/graphql",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "User-Agent": "SOAPaDay-Poster/1.0",
        },
        method="POST",
    )

    last_error = None
    for attempt in range(max_retries + 1):
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode("utf-8"))

                if "data" in result and "createPost" in result["data"]:
                    post_data = result["data"]["createPost"]
                    if "post" in post_data:
                        return {
                            "success": True,
                            "post_id": post_data["post"].get("id"),
                            "text": post_data["post"].get("text"),
                            "status": post_data["post"].get("status"),
                            "scheduled_at": post_data["post"].get("dueAt"),
                        }
                    if "message" in post_data:
                        return {"success": False, "error": post_data["message"]}

                return {"success": False, "error": "Unexpected response", "response": result}

        except urllib.error.HTTPError as e:
            last_error = f"HTTP {e.code}: {e.read().decode('utf-8')}"
            if e.code in (429, 500, 502, 503) and attempt < max_retries:
                time.sleep(2**attempt)
                continue
            return {"success": False, "error": last_error}
        except Exception as e:
            last_error = str(e)
            if attempt < max_retries:
                time.sleep(2**attempt)
                continue
            return {"success": False, "error": last_error}

    return {"success": False, "error": f"Max retries exceeded: {last_error}"}


def log_image_performance(post_id, image_style, prompt=None, platform=None, notes=None):
    log_file = WORKSPACE / "memory" / "social-images-performance.md"
    log_file.parent.mkdir(parents=True, exist_ok=True)

    with open(log_file, "a") as f:
        f.write(f"\n## {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"- Post ID: {post_id}\n")
        f.write(f"- Image Style: {image_style}\n")
        if prompt:
            f.write(f"- Prompt: {prompt}\n")
        if platform:
            f.write(f"- Platform: {platform}\n")
        if notes:
            f.write(f"- Notes: {notes}\n")
        f.write("\n")

    return {"success": True, "log_file": str(log_file)}


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Post to Buffer (SOAPaDay)")
    parser.add_argument("text", help="Post text content")
    parser.add_argument("--platform", choices=["instagram", "facebook"], default="facebook")
    parser.add_argument("--image-url", help="Public URL of image to attach")
    parser.add_argument("--video-url", help="Public URL of video to attach")
    parser.add_argument("--schedule", help="ISO 8601 schedule time")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-retry", action="store_true")
    args = parser.parse_args()

    validation = validate_post(args.text, args.platform)
    if not validation["valid"]:
        print("Validation failed:")
        for error in validation["errors"]:
            print(f"   - {error}")
        sys.exit(1)

    if args.dry_run:
        print(preview_post(args.text, args.image_url, args.platform))
        sys.exit(0)

    result = post_to_buffer(
        text=args.text,
        image_url=args.image_url,
        video_url=args.video_url,
        platform=args.platform,
        schedule_time=args.schedule,
        max_retries=0 if args.no_retry else 3,
    )

    if result["success"]:
        print(f"Posted successfully! Post ID: {result['post_id']}")
    else:
        print(f"Error: {result['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
