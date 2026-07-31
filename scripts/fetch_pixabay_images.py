#!/usr/bin/env python3
"""
Fetch images from Pixabay for blog posts and add alt-text.
"""

import os
import re
import json
import requests
from pathlib import Path

PIXABAY_API_KEY = "4059780-4dc1a0a78263c310cc475bd25"
BLOG_DIR = Path("./src/content/blog")
PUBLIC_DIR = Path("./public/blog-images")

# Search queries for each blog post
BLOG_SEARCH_QUERIES = {
    "apa-itu-deep-cleaning": {
        "query": "deep cleaning house",
        "alt": "Ilustrasi deep cleaning rumah membersihkan area yang jarang terjangkau"
    },
    "dampak-rumah-kotor-untuk-kesehatan": {
        "query": "dirty house health dust",
        "alt": "Dampak rumah kotor terhadap kesehatan keluarga akibat debu dan kotoran"
    },
    "deep-cleaning-jakarta-proses-dan-harga": {
        "query": "cleaning service jakarta",
        "alt": "Layanan deep cleaning profesional di Jakarta"
    },
    "home-cleaning-service-jakarta-apa-yang-dapat": {
        "query": "home cleaning service",
        "alt": "Tim home cleaning service membersihkan rumah"
    },
    "kenapa-harus-pakai-home-cleaning-service": {
        "query": "professional cleaning service home",
        "alt": "Manfaat menggunakan jasa home cleaning service profesional"
    },
    "tanda-rumah-butuh-deep-cleaning": {
        "query": "house needs deep cleaning dirty",
        "alt": "Tanda-tanda rumah membutuhkan deep cleaning"
    }
}

def search_pixabay(query: str, per_page: int = 5) -> list:
    """Search Pixabay for images."""
    url = "https://pixabay.com/api/"
    params = {
        "key": PIXABAY_API_KEY,
        "q": query,
        "image_type": "photo",
        "orientation": "horizontal",
        "per_page": per_page,
        "safesearch": "true",
        "min_width": 800,
        "min_height": 450
    }
    
    try:
        resp = requests.get(url, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("hits", [])
    except Exception as e:
        print(f"   Error searching Pixabay: {e}")
        return []

def download_image(url: str, save_path: Path) -> bool:
    """Download image from URL."""
    try:
        resp = requests.get(url, timeout=60, stream=True)
        resp.raise_for_status()
        
        with open(save_path, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"   Error downloading: {e}")
        return False

def update_blog_post(slug: str, image_path: str, alt_text: str):
    """Update blog post frontmatter with image and alt."""
    post_path = BLOG_DIR / f"{slug}.md"
    
    if not post_path.exists():
        print(f"   Post not found: {post_path}")
        return False
    
    content = post_path.read_text(encoding='utf-8')
    
    # Check if image already exists
    if "image:" in content:
        # Update existing image line
        content = re.sub(
            r"image:\s*['\"][^'\"]+['\"]",
            f"image: '{image_path}'",
            content
        )
        # Add alt if not present
        if "imageAlt:" not in content:
            # Add after image line
            content = re.sub(
                r"(image:\s*['\"][^'\"]+['\"])",
                r"\1\nimageAlt: '" + alt_text + "'",
                content
            )
    else:
        # Add image to frontmatter
        # Find the end of frontmatter (second ---)
        parts = content.split("---")
        if len(parts) >= 3:
            frontmatter = parts[1]
            # Add image after title
            frontmatter = re.sub(
                r"(title:\s*['\"][^'\"]+['\"])",
                r"\1\nimage: '" + image_path + "'\nimageAlt: '" + alt_text + "'",
                frontmatter
            )
            parts[1] = frontmatter
            content = "---".join(parts)
    
    post_path.write_text(content, encoding='utf-8')
    return True

def main():
    print("🖼️  Pixabay Image Fetcher for Blog Posts")
    print("="*50)
    
    # Create public directory for images
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    
    results = []
    
    for slug, config in BLOG_SEARCH_QUERIES.items():
        print(f"\n📝 Processing: {slug}")
        print(f"   Search query: {config['query']}")
        
        # Search Pixabay
        hits = search_pixabay(config["query"])
        
        if not hits:
            print(f"   ⚠️  No images found for query: {config['query']}")
            results.append({"slug": slug, "status": "no_images"})
            continue
        
        # Get first image
        image = hits[0]
        image_url = image.get("webformatURL")
        image_tags = image.get("tags", "")
        
        if not image_url:
            print(f"   ⚠️  No image URL found")
            results.append({"slug": slug, "status": "no_url"})
            continue
        
        print(f"   Found image: {image_url[:60]}...")
        print(f"   Tags: {image_tags}")
        
        # Download image
        filename = f"{slug}.jpg"
        save_path = PUBLIC_DIR / filename
        
        if download_image(image_url, save_path):
            image_path = f"/blog-images/{filename}"
            alt_text = config["alt"]
            
            print(f"   ✅ Downloaded to: {image_path}")
            print(f"   Alt text: {alt_text}")
            
            # Update blog post
            if update_blog_post(slug, image_path, alt_text):
                print(f"   ✅ Updated blog post")
                results.append({
                    "slug": slug,
                    "status": "success",
                    "image": image_path,
                    "alt": alt_text
                })
            else:
                print(f"   ❌ Failed to update blog post")
                results.append({"slug": slug, "status": "update_failed"})
        else:
            print(f"   ❌ Failed to download image")
            results.append({"slug": slug, "status": "download_failed"})
    
    # Print summary
    print("\n" + "="*50)
    print("📊 SUMMARY")
    print("="*50)
    
    success = sum(1 for r in results if r["status"] == "success")
    failed = sum(1 for r in results if r["status"] != "success")
    
    print(f"✅ Successfully processed: {success}")
    print(f"❌ Failed: {failed}")
    
    print("\n📋 Details:")
    for r in results:
        status_icon = "✅" if r["status"] == "success" else "❌"
        print(f"   {status_icon} {r['slug']}: {r['status']}")
        if r["status"] == "success":
            print(f"      Image: {r['image']}")
            print(f"      Alt: {r['alt']}")
    
    # Save results
    results_path = Path("./scripts/pixabay_results.json")
    results_path.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"\n📄 Results saved to: {results_path}")

if __name__ == "__main__":
    main()
