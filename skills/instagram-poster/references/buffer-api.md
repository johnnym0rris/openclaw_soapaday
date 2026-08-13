# Buffer API Reference for SOAPaDay Instagram

## Profile ID

Set in `.env`:
```
BUFFER_INSTAGRAM_PROFILE_ID=your_profile_id_here
```

Get profile IDs from Buffer dashboard or API after connecting Instagram.

## Required Metadata

Instagram posts require specific metadata:

```json
{
  "instagram": {
    "type": "reel",
    "shouldShareToFeed": true
  }
}
```

### Types
- `reel` — Short-form video (up to 90 seconds)
- `post` — Static image or carousel feed post
- `story` — 24-hour ephemeral content

### shouldShareToFeed
- `true` — Reel appears in both Reels tab and main feed
- `false` — Reel appears only in Reels tab

## GraphQL Mutation

```graphql
mutation CreatePost($input: CreatePostInput!) {
  createPost(input: $input) {
    ... on PostActionSuccess {
      post { id text status dueAt }
    }
    ... on MutationError {
      message
    }
  }
}
```

## Variables Structure

```json
{
  "input": {
    "text": "Caption text here",
    "channelId": "YOUR_INSTAGRAM_PROFILE_ID",
    "schedulingType": "automatic",
    "mode": "shareNow",
    "metadata": {
      "instagram": {
        "type": "reel",
        "shouldShareToFeed": true
      }
    },
    "assets": [
      {"video": {"url": "https://public-url-to-video.mp4"}}
    ]
  }
}
```

## Error Handling

Common errors:
- `Instagram posts require a type` — Missing metadata.type
- `Instagram posts require at least one image or video` — Missing assets
- `401 Unauthorized` — Token expired, update BUFFER_ACCESS_TOKEN in .env
- Profile ID not set — Configure BUFFER_INSTAGRAM_PROFILE_ID in .env
