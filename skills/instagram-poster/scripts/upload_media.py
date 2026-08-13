#!/usr/bin/env python3
"""
Upload media (images or videos) to the myChelper image server.
Supports: png, jpg, webp, gif, mp4, mov, avi, mkv, webm
"""

import os
import json
import urllib.request

BASE_URL = "https://images.mychelper.com"
API_KEY = "karfen-mubruc-qYnga1"
UPLOAD_PATH = "marketing/social-media/posts"


def upload_media(file_path):
    """
    Upload an image or video to the myChelper image server.
    
    Args:
        file_path: Local path to the media file
    
    Returns:
        dict: API response with url and image_path
    """
    
    upload_url = f"{BASE_URL}/api/images/upload/{UPLOAD_PATH}"
    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
    
    with open(file_path, 'rb') as f:
        file_data = f.read()
    
    filename = os.path.basename(file_path)
    ext = filename.lower().split('.')[-1] if '.' in filename else ''
    
    # Determine content type
    content_types = {
        'png': 'image/png',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'webp': 'image/webp',
        'gif': 'image/gif',
        'mp4': 'video/mp4',
        'm4v': 'video/mp4',
        'mov': 'video/quicktime',
        'qt': 'video/quicktime',
        'avi': 'video/x-msvideo',
        'mkv': 'video/x-matroska',
        'webm': 'video/webm',
    }
    content_type = content_types.get(ext, 'application/octet-stream')
    
    # Build multipart body
    body = []
    body.append(f'--{boundary}'.encode())
    body.append(f'Content-Disposition: form-data; name="image"; filename="{filename}"'.encode())
    body.append(f'Content-Type: {content_type}'.encode())
    body.append(b'')
    body.append(file_data)
    body.append(f'--{boundary}--'.encode())
    
    body = b'\r\n'.join(body)
    
    req = urllib.request.Request(
        upload_url,
        data=body,
        headers={
            'MYCHELPER-API-KEY': API_KEY,
            'Content-Type': f'multipart/form-data; boundary={boundary}'
        },
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        raise Exception(f"Upload failed: HTTP {e.code} - {error_body}")


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 upload_media.py <file_path>")
        sys.exit(1)
    
    result = upload_media(sys.argv[1])
    print(json.dumps(result, indent=2))
