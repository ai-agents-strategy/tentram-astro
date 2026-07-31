#!/usr/bin/env python3
"""Retry failed Pixabay downloads."""

import re
import time
import requests
from pathlib import Path

PIXABAY_API_KEY = "4059780-4dc1a0a78263c310cc475bd25"
PUBLIC_DIR = Path("./public/blog-images")
BLOG_DIR = Path("./src/content/blog")

failed = [
    {"slug": "dampak-rumah-kotor-untuk-kesehatan", "query": "dust mites allergy home", "alt": "Dampak debu dan kotoran rumah terhadap kesehatan"},
    {"slug": "tanda-rumah-butuh-deep-cleaning", "query": "dirty bathroom mold cleaning", "alt": "Tanda rumah kotor dan butuh deep cleaning"}
]

for item in failed:
    print(f"Retrying: {item['slug']}")
    time.sleep(5)
    
    resp = requests.get("https://pixabay.com/api/", params={
        "key": PIXABAY_API_KEY,
        "q": item["query"],
        "image_type": "photo",
        "orientation": "horizontal",
        "per_page": 5,
        "safesearch": "true"
    }, timeout=30)
    
    hits = resp.json().get("hits", [])
    if not hits:
        print("  No images found")
        continue
    
    image_url = hits[0]["webformatURL"]
    print(f"  Found: {image_url[:50]}...")
    
    time.sleep(3)
    img_resp = requests.get(image_url, timeout=60)
    if img_resp.status_code != 200:
        print(f"  Download failed: {img_resp.status_code}")
        continue
    
    filename = f"{item['slug']}.jpg"
    with open(PUBLIC_DIR / filename, "wb") as f:
        f.write(img_resp.content)
    print(f"  Downloaded: {filename}")
    
    post_path = BLOG_DIR / f"{item['slug']}.md"
    content = post_path.read_text(encoding="utf-8")
    
    if "image:" in content:
        content = re.sub(r"image:\s*['\"][^'\"]+['\"]", f"image: '/blog-images/{filename}'", content)
        if "imageAlt:" not in content:
            content = re.sub(
                r"(image:\s*['\"][^'\"]+['\"])",
                f"\\1\nimageAlt: '{item['alt']}'",
                content
            )
    else:
        parts = content.split("---")
        if len(parts) >= 3:
            parts[1] = re.sub(
                r"(title:\s*['\"][^'\"]+['\"])",
                f"\\1\nimage: '/blog-images/{filename}'\nimageAlt: '{item['alt']}'",
                parts[1]
            )
            content = "---".join(parts)
    
    post_path.write_text(content, encoding="utf-8")
    print(f"  Updated: {post_path}")

print("\nDone!")
