# Scripts

Automation scripts for marketing workflows.

## Current Scripts

### Buffer Posting
- `post_to_buffer.py` — Post text + images to Buffer
- `buffer-post.py` — Text-only fallback (more reliable when image issues occur)

### Image Generation
- `image_compositor_linkedin.py` — Generate branded LinkedIn images
- `image_compositor_facebook.py` — Generate branded Facebook images

## Setup Notes
- Buffer token in `~/.bashrc` — must `source ~/.bashrc` or export manually before posting
- Image duplicate detection: Buffer flags reused images. Rotate banners or post text-only if recently used
