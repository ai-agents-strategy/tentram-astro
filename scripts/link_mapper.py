#!/usr/bin/env python3
"""
Internal Link Mapper for tentram.id
Maps all pages, validates links, and creates a knowledge graph in Qdrant.
"""

import json
import re
import requests
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

# Qdrant config
QDRANT_HOST = "127.0.0.1"
QDRANT_PORT = 6333
QDRANT_API_KEY = "2dmMX0hWfYkZPFLtxNhX2Hsx2zULadmymlpb239y5TQ"
COLLECTION_NAME = "tentram-link-graph"

# Site config
SITE_URL = "https://tentram.id"

@dataclass
class Page:
    path: str
    title: str
    type: str  # 'service', 'blog', 'page'
    slug: str
    internal_links: list = field(default_factory=list)
    incoming_links: list = field(default_factory=list)
    status: Optional[int] = None
    issues: list = field(default_factory=list)

def get_headers():
    return {"api-key": QDRANT_API_KEY}

def check_collection_exists():
    """Check if collection exists, create if not."""
    resp = requests.get(
        f"http://{QDRANT_HOST}:{QDRANT_PORT}/collections/{COLLECTION_NAME}",
        headers=get_headers()
    )
    if resp.status_code == 404:
        # Create collection
        resp = requests.put(
            f"http://{QDRANT_HOST}:{QDRANT_PORT}/collections/{COLLECTION_NAME}",
            headers=get_headers(),
            json={
                "vectors": {
                    "size": 128,
                    "distance": "Cosine"
                }
            }
        )
        print(f"Created collection: {COLLECTION_NAME}")
    return resp.status_code == 200

def index_to_qdrant(pages: dict):
    """Index all pages into Qdrant."""
    points = []
    for i, (path, page) in enumerate(pages.items()):
        # Create a simple embedding from page metadata
        # (In production, you'd use a real embedding model)
        vector = [0.0] * 128
        # Encode basic features into vector
        vector[0] = 1.0 if page.type == 'service' else 0.0
        vector[1] = 1.0 if page.type == 'blog' else 0.0
        vector[2] = len(page.internal_links) / 10.0
        vector[3] = len(page.incoming_links) / 10.0
        vector[4] = 1.0 if page.status == 200 else 0.0
        
        points.append({
            "id": i,
            "vector": vector,
            "payload": {
                "path": page.path,
                "title": page.title,
                "type": page.type,
                "slug": page.slug,
                "internal_links": page.internal_links,
                "incoming_links": page.incoming_links,
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

def load_services():
    """Load services from content.ts."""
    services = []
    # Parse the services from content.ts
    content_path = Path("./src/data/content.ts")
    content = content_path.read_text()
    
    # Extract slugs using simple parsing
    import re
    slug_pattern = r"slug:\s*'([^']+)'"
    slugs = re.findall(slug_pattern, content)
    
    for slug in slugs:
        services.append({
            "slug": slug,
            "path": f"/layanan/{slug}/",
            "title": slug.replace("-", " ").title(),
            "type": "service"
        })
    
    return services

def load_blog_posts():
    """Load blog posts from content directory."""
    blog_posts = []
    blog_dir = Path("./src/content/blog")
    
    if blog_dir.exists():
        for post_file in blog_dir.glob("*.md"):
            slug = post_file.stem
            # Read frontmatter for title
            content = post_file.read_text()
            title_match = re.search(r"title:\s*['\"]([^'\"]+)['\"]", content)
            title = title_match.group(1) if title_match else slug.replace("-", " ").title()
            
            blog_posts.append({
                "slug": slug,
                "path": f"/blog/{slug}/",
                "title": title,
                "type": "blog"
            })
    
    return blog_posts

def load_static_pages():
    """Load static pages."""
    return [
        {"slug": "", "path": "/", "title": "Tentram - Home", "type": "page"},
        {"slug": "blog", "path": "/blog/", "title": "Blog", "type": "page"},
        {"slug": "layanan", "path": "/layanan/", "title": "Layanan", "type": "page"},
    ]

def validate_links(pages: dict):
    """Validate all internal links."""
    all_paths = set(pages.keys())
    
    for path, page in pages.items():
        for link in page.internal_links:
            # Normalize link
            link_path = link.rstrip("/")
            if link_path and link_path not in all_paths:
                page.issues.append(f"Broken link: {link}")
    
    return pages

def find_link_opportunities(pages: dict):
    """Find pages that should link to each other."""
    services = {p: page for p, page in pages.items() if page.type == "service"}
    blogs = {p: page for p, page in pages.items() if page.type == "blog"}
    
    opportunities = []
    
    # Services should link to related blogs
    for svc_path, svc in services.items():
        for blog_path, blog in blogs.items():
            if blog_path not in svc.internal_links:
                # Check if blog is related
                if any(word in blog.slug for word in svc.slug.split("-")):
                    opportunities.append({
                        "source": svc_path,
                        "target": blog_path,
                        "reason": f"Service '{svc.slug}' could link to related blog '{blog.slug}'"
                    })
    
    # Blogs should link to related services
    for blog_path, blog in blogs.items():
        for svc_path, svc in services.items():
            if svc_path not in blog.internal_links:
                if any(word in blog.slug for word in svc.slug.split("-")):
                    opportunities.append({
                        "source": blog_path,
                        "target": svc_path,
                        "reason": f"Blog '{blog.slug}' could link to related service '{svc.slug}'"
                    })
    
    return opportunities

def print_report(pages: dict, opportunities: list):
    """Print comprehensive report."""
    print("\n" + "="*80)
    print("TENTRAM.ID INTERNAL LINK ANALYSIS")
    print("="*80)
    
    # Summary
    total_pages = len(pages)
    total_links = sum(len(p.internal_links) for p in pages.values())
    broken_links = sum(len([i for i in p.issues if "Broken" in i]) for p in pages.values())
    
    print(f"\n📊 SUMMARY")
    print(f"   Total pages: {total_pages}")
    print(f"   Total internal links: {total_links}")
    print(f"   Broken links: {broken_links}")
    print(f"   Link opportunities: {len(opportunities)}")
    
    # Pages by type
    print(f"\n📄 PAGES BY TYPE")
    types = {}
    for page in pages.values():
        types[page.type] = types.get(page.type, 0) + 1
    for t, count in types.items():
        print(f"   {t}: {count}")
    
    # Pages with issues
    pages_with_issues = [(p, page) for p, page in pages.items() if page.issues]
    if pages_with_issues:
        print(f"\n⚠️  PAGES WITH ISSUES ({len(pages_with_issues)})")
        for path, page in pages_with_issues:
            print(f"\n   {path} ({page.title})")
            for issue in page.issues:
                print(f"      - {issue}")
    
    # Internal links per page
    print(f"\n🔗 INTERNAL LINKS PER PAGE")
    for path, page in sorted(pages.items(), key=lambda x: len(x[1].internal_links), reverse=True):
        if page.internal_links:
            print(f"\n   {path}")
            for link in page.internal_links:
                print(f"      → {link}")
    
    # Incoming links
    print(f"\n⬅️  INCOMING LINKS PER PAGE")
    for path, page in sorted(pages.items(), key=lambda x: len(x[1].incoming_links), reverse=True):
        if page.incoming_links:
            print(f"\n   {path}")
            for link in page.incoming_links:
                print(f"      ← {link}")
    
    # Link opportunities
    if opportunities:
        print(f"\n💡 LINK OPPORTUNITIES ({len(opportunities)})")
        for opp in opportunities[:20]:  # Top 20
            print(f"\n   {opp['source']} → {opp['target']}")
            print(f"      Reason: {opp['reason']}")

def main():
    print("🔍 Tentram Internal Link Mapper")
    print("="*50)
    
    # Load all pages
    print("\n📚 Loading pages...")
    pages = {}
    
    # Load services
    for svc in load_services():
        pages[svc["path"]] = Page(
            path=svc["path"],
            title=svc["title"],
            type=svc["type"],
            slug=svc["slug"],
            internal_links=[]
        )
    
    # Load blog posts
    for blog in load_blog_posts():
        pages[blog["path"]] = Page(
            path=blog["path"],
            title=blog["title"],
            type=blog["type"],
            slug=blog["slug"],
            internal_links=[]
        )
    
    # Load static pages
    for page in load_static_pages():
        pages[page["path"]] = Page(
            path=page["path"],
            title=page["title"],
            type=page["type"],
            slug=page["slug"],
            internal_links=[]
        )
    
    print(f"   Found {len(pages)} pages")
    
    # Extract internal links from HTML
    print("\n🔗 Extracting internal links...")
    # This would parse the built HTML or use a crawler
    # For now, we'll use the sitemap data
    
    # Load services with their internal links from content.ts
    content_path = Path("./src/data/content.ts")
    content = content_path.read_text()
    
    # Parse internalLinks from the content
    import re
    # Find service sections with internalLinks
    service_sections = re.findall(r"slug:\s*'([^']+)'.*?internalLinks:\s*\[(.*?)\]", content, re.DOTALL)
    
    for slug, links_str in service_sections:
        if links_str.strip():
            # Extract href values
            hrefs = re.findall(r"href:\s*'([^']+)'", links_str)
            path = f"/layanan/{slug}/"
            if path in pages:
                pages[path].internal_links = hrefs
    
    # Build incoming links
    for path, page in pages.items():
        for link in page.internal_links:
            if link in pages:
                pages[link].incoming_links.append(path)
    
    # Validate links
    print("\n✅ Validating links...")
    pages = validate_links(pages)
    
    # Find opportunities
    print("\n💡 Finding link opportunities...")
    opportunities = find_link_opportunities(pages)
    
    # Index to Qdrant
    print("\n📤 Indexing to Qdrant...")
    if check_collection_exists():
        if index_to_qdrant(pages):
            print("   ✅ Indexed successfully")
        else:
            print("   ❌ Failed to index")
    
    # Print report
    print_report(pages, opportunities)
    
    # Save report to file
    report_path = Path("./scripts/link_report.json")
    report_data = {
        "summary": {
            "total_pages": len(pages),
            "total_links": sum(len(p.internal_links) for p in pages.values()),
            "broken_links": sum(len([i for i in p.issues if "Broken" in i]) for p in pages.values()),
            "opportunities": len(opportunities)
        },
        "pages": {
            path: {
                "title": page.title,
                "type": page.type,
                "internal_links": page.internal_links,
                "incoming_links": page.incoming_links,
                "issues": page.issues
            }
            for path, page in pages.items()
        },
        "opportunities": opportunities
    }
    
    report_path.write_text(json.dumps(report_data, indent=2))
    print(f"\n📄 Report saved to: {report_path}")

if __name__ == "__main__":
    main()
