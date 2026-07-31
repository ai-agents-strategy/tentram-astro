#!/usr/bin/env python3
"""
Internal Link Validator for tentram.id
Validates all internal links against the live site and builds knowledge graph.
"""

import json
import re
import requests
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, Set
from concurrent.futures import ThreadPoolExecutor, as_completed

# Qdrant config
QDRANT_HOST = "127.0.0.1"
QDRANT_PORT = 6333
QDRANT_API_KEY = "2dmMX0hWfYkZPFLtxNhX2Hsx2zULadmymlpb239y5TQ"
COLLECTION_NAME = "tentram-link-graph"

# Site config
SITE_URL = "https://tentram.id"

@dataclass
class Page:
    url: str
    path: str
    title: str
    type: str  # 'service', 'blog', 'page'
    slug: str
    internal_links: Set[str] = field(default_factory=set)
    incoming_links: Set[str] = field(default_factory=set)
    status: Optional[int] = None
    issues: list = field(default_factory=list)

def get_headers():
    return {"api-key": QDRANT_API_KEY}

def get_sitemap_urls() -> Set[str]:
    """Get all URLs from sitemap."""
    resp = requests.get(f"{SITE_URL}/sitemap.xml", timeout=30)
    urls = re.findall(r'<loc>([^<]+)</loc>', resp.text)
    return {url.rstrip('/') for url in urls}

def check_url(url: str) -> int:
    """Check if URL returns 200."""
    try:
        resp = requests.head(url, timeout=10, allow_redirects=True)
        return resp.status_code
    except:
        return 0

def extract_internal_links(html: str, base_url: str) -> Set[str]:
    """Extract internal links from HTML."""
    links = set()
    # Find all href attributes
    href_pattern = r'href="([^"]*)"'
    for match in re.finditer(href_pattern, html):
        href = match.group(1)
        # Skip external links, anchors, etc.
        if href.startswith(('http', 'mailto:', 'tel:', '#', 'javascript:')):
            continue
        # Normalize path
        if href.startswith('/'):
            full_url = f"{SITE_URL}{href}"
        else:
            full_url = f"{SITE_URL}/{href}"
        # Remove trailing slash for consistency
        links.add(full_url.rstrip('/'))
    return links

def crawl_page(url: str) -> tuple:
    """Crawl a page and return its links."""
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            links = extract_internal_links(resp.text, SITE_URL)
            return (url, resp.status_code, links)
        return (url, resp.status_code, set())
    except Exception as e:
        return (url, 0, set())

def index_to_qdrant(pages: dict):
    """Index all pages into Qdrant."""
    points = []
    for i, (path, page) in enumerate(pages.items()):
        # Create a simple embedding from page metadata
        vector = [0.0] * 128
        # Encode features into vector
        vector[0] = 1.0 if page.type == 'service' else 0.0
        vector[1] = 1.0 if page.type == 'blog' else 0.0
        vector[2] = min(len(page.internal_links) / 10.0, 1.0)
        vector[3] = min(len(page.incoming_links) / 10.0, 1.0)
        vector[4] = 1.0 if page.status == 200 else 0.0
        
        points.append({
            "id": i,
            "vector": vector,
            "payload": {
                "path": page.path,
                "url": page.url,
                "title": page.title,
                "type": page.type,
                "slug": page.slug,
                "internal_links": list(page.internal_links),
                "incoming_links": list(page.incoming_links),
                "status": page.status,
                "issues": page.issues
            }
        })
    
    # Upsert points
    resp = requests.put(
        f"http://{QDRANT_HOST}:{QDRANT_PORT}/collections/{COLLECTION_NAME}/points",
        headers=get_headers(),
        json={"points": points}
    )
    return resp.status_code == 200

def ensure_collection():
    """Ensure Qdrant collection exists."""
    resp = requests.get(
        f"http://{QDRANT_HOST}:{QDRANT_PORT}/collections/{COLLECTION_NAME}",
        headers=get_headers()
    )
    if resp.status_code == 404:
        resp = requests.put(
            f"http://{QDRANT_HOST}:{QDRANT_PORT}/collections/{COLLECTION_NAME}",
            headers=get_headers(),
            json={"vectors": {"size": 128, "distance": "Cosine"}}
        )
        print(f"✅ Created Qdrant collection: {COLLECTION_NAME}")
    return resp.status_code == 200

def classify_page(path: str) -> tuple:
    """Classify page type and slug from path."""
    if path.startswith('/layanan/'):
        slug = path.replace('/layanan/', '').rstrip('/')
        return ('service', slug)
    elif path.startswith('/blog/'):
        slug = path.replace('/blog/', '').rstrip('/')
        return ('blog', slug)
    else:
        return ('page', path.strip('/'))

def print_report(pages: dict):
    """Print comprehensive report."""
    print("\n" + "="*80)
    print("TENTRAM.ID INTERNAL LINK ANALYSIS")
    print("="*80)
    
    # Summary
    total_pages = len(pages)
    total_links = sum(len(p.internal_links) for p in pages.values())
    broken_pages = sum(1 for p in pages.values() if p.status != 200)
    pages_with_issues = sum(1 for p in pages.values() if p.issues)
    
    print(f"\n📊 SUMMARY")
    print(f"   Total pages crawled: {total_pages}")
    print(f"   Total internal links found: {total_links}")
    print(f"   Pages with broken status: {broken_pages}")
    print(f"   Pages with link issues: {pages_with_issues}")
    
    # Pages by type
    print(f"\n📄 PAGES BY TYPE")
    types = {}
    for page in pages.values():
        types[page.type] = types.get(page.type, 0) + 1
    for t, count in sorted(types.items()):
        print(f"   {t}: {count}")
    
    # Pages with issues
    problem_pages = [(p, page) for p, page in pages.items() if page.issues or page.status != 200]
    if problem_pages:
        print(f"\n⚠️  PAGES WITH ISSUES ({len(problem_pages)})")
        for path, page in problem_pages:
            status_icon = "✅" if page.status == 200 else "❌"
            print(f"\n   {status_icon} {path} (HTTP {page.status})")
            for issue in page.issues:
                print(f"      - {issue}")
    
    # Top pages by incoming links (most linked to)
    print(f"\n🔗 TOP PAGES BY INCOMING LINKS (Most Important)")
    top_incoming = sorted(pages.items(), key=lambda x: len(x[1].incoming_links), reverse=True)[:10]
    for path, page in top_incoming:
        if page.incoming_links:
            print(f"\n   {path} ({page.title})")
            print(f"      Incoming links: {len(page.incoming_links)}")
    
    # Pages with most outgoing links
    print(f"\n📤 TOP PAGES BY OUTGOING LINKS")
    top_outgoing = sorted(pages.items(), key=lambda x: len(x[1].internal_links), reverse=True)[:10]
    for path, page in top_outgoing:
        if page.internal_links:
            print(f"\n   {path} ({page.title})")
            print(f"      Outgoing links: {len(page.internal_links)}")
    
    # Orphan pages (no incoming links)
    orphans = [(p, page) for p, page in pages.items() if not page.incoming_links and page.path != '/']
    if orphans:
        print(f"\n🏝️  ORPHAN PAGES (No Incoming Links) - {len(orphans)}")
        for path, page in orphans[:10]:
            print(f"   {path}")
    
    # Missing internal links suggestion
    print(f"\n💡 RECOMMENDED INTERNAL LINKS")
    services = {p: page for p, page in pages.items() if page.type == "service"}
    blogs = {p: page for p, page in pages.items() if page.type == "blog"}
    
    suggestions = []
    for svc_path, svc in services.items():
        # Find related blogs
        for blog_path, blog in blogs.items():
            if blog_path not in svc.internal_links:
                # Check relevance
                svc_words = set(svc.slug.split('-'))
                blog_words = set(blog.slug.split('-'))
                if svc_words & blog_words:  # Common words
                    suggestions.append((svc_path, blog_path, blog.title))
    
    # Group by source
    by_source = {}
    for src, tgt, title in suggestions:
        if src not in by_source:
            by_source[src] = []
        by_source[src].append((tgt, title))
    
    for src, targets in list(by_source.items())[:5]:
        print(f"\n   From {src}:")
        for tgt, title in targets[:3]:
            print(f"      → {tgt} ({title})")

def main():
    print("🔍 Tentram Internal Link Validator")
    print("="*50)
    
    # Get all URLs from sitemap
    print("\n📡 Fetching sitemap...")
    sitemap_urls = get_sitemap_urls()
    print(f"   Found {len(sitemap_urls)} URLs in sitemap")
    
    # Initialize pages dict
    pages = {}
    for url in sitemap_urls:
        path = url.replace(SITE_URL, '')
        page_type, slug = classify_page(path)
        pages[path] = Page(
            url=url,
            path=path,
            title=slug.replace('-', ' ').title() if slug else 'Home',
            type=page_type,
            slug=slug
        )
    
    # Crawl all pages in parallel
    print("\n🕷️  Crawling pages...")
    urls_to_crawl = [f"{SITE_URL}{path}" for path in pages.keys()]
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(crawl_page, url): url for url in urls_to_crawl}
        completed = 0
        for future in as_completed(futures):
            url, status, links = future.result()
            path = url.replace(SITE_URL, '')
            if path in pages:
                pages[path].status = status
                pages[path].internal_links = {link.replace(SITE_URL, '') for link in links}
            completed += 1
            if completed % 5 == 0:
                print(f"   Crawled {completed}/{len(urls_to_crawl)} pages...")
    
    print(f"   ✅ Crawled {len(pages)} pages")
    
    # Build incoming links
    print("\n🔗 Building link graph...")
    for path, page in pages.items():
        for link in page.internal_links:
            if link in pages:
                pages[link].incoming_links.add(path)
    
    # Validate links
    print("\n✅ Validating links...")
    valid_paths = set(pages.keys())
    for path, page in pages.items():
        for link in page.internal_links:
            if link not in valid_paths:
                page.issues.append(f"Link points to non-existent page: {link}")
    
    # Index to Qdrant
    print("\n📤 Indexing to Qdrant...")
    if ensure_collection():
        if index_to_qdrant(pages):
            print("   ✅ Indexed successfully to Qdrant")
        else:
            print("   ❌ Failed to index to Qdrant")
    
    # Print report
    print_report(pages)
    
    # Save detailed report
    report_path = Path("./scripts/link_report.json")
    report_data = {
        "summary": {
            "total_pages": len(pages),
            "total_links": sum(len(p.internal_links) for p in pages.values()),
            "broken_status": sum(1 for p in pages.values() if p.status != 200),
            "pages_with_issues": sum(1 for p in pages.values() if p.issues)
        },
        "pages": {
            path: {
                "url": page.url,
                "title": page.title,
                "type": page.type,
                "status": page.status,
                "internal_links": list(page.internal_links),
                "incoming_links": list(page.incoming_links),
                "issues": page.issues
            }
            for path, page in pages.items()
        }
    }
    report_path.write_text(json.dumps(report_data, indent=2))
    print(f"\n📄 Detailed report saved to: {report_path}")

if __name__ == "__main__":
    main()
