#!/usr/bin/env python3
"""
Topical cluster / internal-linking knowledge graph for tentram-id (tentram.id).

Standalone SEO content-planning tool — NOT the platform's knowledge: pipeline
(that one is OpenAI-only end to end; see runtime/hermes-plugins/knowledge).
This uses Jina AI's hosted embeddings API (JINA_API_KEY in .env) instead,
since it needs no local model download and tentram-id's corpus is small
(~20 items) so no vector DB is needed either — plain cosine similarity in
Python is enough.

Method:
1. Embed every blog post (title + description + tags) and every service
   page (title + headline + description) with jina-embeddings-v3.
2. Assign each blog post to its most-similar service (the 9 services are
   the topical "pillars" — see site/src/data/content.ts).
3. Report: content count per pillar (coverage gaps = pillars with 0-1
   posts), near-duplicate pairs above a cannibalization threshold, and
   top cross-neighbors as internal-linking suggestions.

Usage:
  topical_cluster_graph.py                 # full report
  topical_cluster_graph.py --top-k 5        # neighbors per item
"""

import argparse
import json
import math
import os
import re
import sys
from pathlib import Path

import requests
import yaml

SITE_ROOT = Path(__file__).resolve().parents[1] / "site"
BLOG_DIR = SITE_ROOT / "src" / "content" / "blog"
OUT_JSON = Path(__file__).resolve().parents[1] / "topical-cluster-graph.json"
OUT_MD = Path(__file__).resolve().parents[1] / "topical-cluster-report.md"

JINA_URL = "https://api.jina.ai/v1/embeddings"
JINA_MODEL = "jina-embeddings-v3"
CANNIBAL_THRESHOLD = 0.90

# Mirrors site/src/data/content.ts `services` — the 9 topical pillars.
# Update this list if content.ts services are added/removed/renamed.
SERVICES = [
    {"slug": "after-renovasi", "title": "After Renovasi",
     "text": "After Renovasi. Rumah Bersih Setelah Renovasi — Siap Ditempati. "
             "Layanan cleaning pasca renovasi untuk membersihkan debu semen, sisa cat, dan kotoran berat agar rumah Anda siap ditempati.",
     "has_internal_links": False},
    {"slug": "move-in", "title": "Move In Cleaning",
     "text": "Move In Cleaning. Masuk Rumah Baru dalam Keadaan Bersih. "
             "Move in cleaning untuk rumah dan apartemen baru sebelum Anda mulai menempati setiap sudut dengan higienis.",
     "has_internal_links": False},
    {"slug": "home-cleaning", "title": "Home Cleaning",
     "text": "Home Cleaning. Rumah Bersih Tanpa Anda Harus Capek Sendiri. "
             "Layanan home cleaning rutin untuk rumah dan apartemen di Jakarta, BSD, Tangerang, Bekasi, dan sekitarnya.",
     "has_internal_links": False},
    {"slug": "office-cleaning", "title": "Office Cleaning",
     "text": "Office Cleaning. Kantor Bersih untuk Tim dan Pelanggan Anda. "
             "Jasa office cleaning harian atau berkala untuk kantor, coworking space, dan ruang kerja di Jakarta dan sekitarnya.",
     "has_internal_links": False},
    {"slug": "deep-cleaning", "title": "Deep Cleaning",
     "text": "Deep Cleaning. Pembersihan Menyeluruh untuk Rumah yang Siap Ditempati. "
             "Deep cleaning menyeluruh untuk pindahan, renovasi, dan gudang. Tim profesional Tentram bersihkan area yang terlewat: "
             "kerak kamar mandi, debu balik furniture, noda dinding.",
     "has_internal_links": True},
    {"slug": "hydro-cleaning", "title": "Hydro Cleaning",
     "text": "Hydro Cleaning. Sofa, Kasur, dan Karpet Bersih dari Dalam. "
             "Hydro cleaning menggunakan teknologi hydro extraction untuk membersihkan sofa, kasur, karpet, dan interior kain secara mendalam.",
     "has_internal_links": False},
    {"slug": "cuci-ac", "title": "Cuci AC",
     "text": "Cuci AC. AC Dingin, Bersih, dan Bebas Bau. "
             "Layanan cuci AC rumah dan kantor oleh tim profesional tanpa perlu Anda bongkar sendiri.",
     "has_internal_links": False},
    {"slug": "cleaning-gudang", "title": "Cleaning Gudang",
     "text": "Cleaning Gudang. Gudang Rapi, Bersih, dan Aman Digunakan. "
             "Layanan cleaning gudang untuk membersihkan debu, tumpukan kotoran, dan sisa material agar gudang kembali rapi.",
     "has_internal_links": False},
    {"slug": "cleaning-kamar-mandi", "title": "Cleaning Kamar Mandi",
     "text": "Cleaning Kamar Mandi. Kamar Mandi Kinclong dan Bebas Jamur. "
             "Layanan khusus pembersihan kamar mandi: hilangkan kerak, jamur, noda, dan bau tidak sedap secara detail.",
     "has_internal_links": False},
]


def load_env(path) -> dict:
    out = {}
    p = Path(path)
    if not p.exists():
        return out
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip()
    return out


def load_blog_posts():
    posts = []
    for md_path in sorted(BLOG_DIR.glob("*.md")):
        raw = md_path.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n", raw, re.DOTALL)
        if not m:
            continue
        fm = yaml.safe_load(m.group(1)) or {}
        title = fm.get("title", md_path.stem)
        description = fm.get("description", "")
        tags = fm.get("tags", [])
        posts.append({
            "type": "blog",
            "slug": md_path.stem,
            "title": title,
            "text": f"{title}. {description} Tags: {', '.join(tags)}",
        })
    return posts


def embed(texts, api_key):
    resp = requests.post(
        JINA_URL,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        json={"model": JINA_MODEL, "task": "text-matching", "input": texts},
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()["data"]
    data.sort(key=lambda d: d["index"])
    return [d["embedding"] for d in data]


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--top-k", type=int, default=5, help="Neighbors per item in the report")
    args = p.parse_args()

    customer_env = load_env(Path(__file__).resolve().parents[1] / ".env")
    api_key = customer_env.get("JINA_API_KEY") or os.environ.get("JINA_API_KEY")
    if not api_key:
        sys.exit("error: JINA_API_KEY not set in customers/tentram-id/.env")

    services = [{"type": "service", **s} for s in SERVICES]
    blogs = load_blog_posts()
    items = services + blogs

    print(f"Embedding {len(items)} items ({len(services)} services, {len(blogs)} blog posts) via Jina...")
    vectors = embed([it["text"] for it in items], api_key)
    for it, vec in zip(items, vectors):
        it["vector"] = vec

    # Assign each blog post to its most-similar service pillar.
    service_items = [it for it in items if it["type"] == "service"]
    blog_items = [it for it in items if it["type"] == "blog"]

    pillar_assignment = {}  # service slug -> list of blog slugs
    for s in service_items:
        pillar_assignment[s["slug"]] = []

    for b in blog_items:
        best = max(service_items, key=lambda s: cosine(b["vector"], s["vector"]))
        score = cosine(b["vector"], best["vector"])
        b["pillar"] = best["slug"]
        b["pillar_score"] = round(score, 4)
        pillar_assignment[best["slug"]].append({"slug": b["slug"], "title": b["title"], "score": round(score, 4)})

    # Cannibalization: blog-blog pairs above threshold.
    cannibal_pairs = []
    for i in range(len(blog_items)):
        for j in range(i + 1, len(blog_items)):
            score = cosine(blog_items[i]["vector"], blog_items[j]["vector"])
            if score >= CANNIBAL_THRESHOLD:
                cannibal_pairs.append({
                    "a": blog_items[i]["slug"], "b": blog_items[j]["slug"], "score": round(score, 4),
                })

    # Top-k neighbors per item (any type) for internal-linking suggestions.
    neighbor_index = {}
    for it in items:
        scored = sorted(
            ({"slug": o["slug"], "type": o["type"], "title": o["title"], "score": round(cosine(it["vector"], o["vector"]), 4)}
             for o in items if o["slug"] != it["slug"]),
            key=lambda d: d["score"], reverse=True,
        )
        neighbor_index[it["slug"]] = scored[:args.top_k]

    coverage_gaps = [s["slug"] for s in service_items if len(pillar_assignment[s["slug"]]) <= 1]
    no_internal_links = [s["slug"] for s in SERVICES if not s["has_internal_links"]]

    output = {
        "meta": {"model": JINA_MODEL, "total_services": len(service_items), "total_blog_posts": len(blog_items)},
        "pillar_assignment": pillar_assignment,
        "coverage_gaps": coverage_gaps,
        "cannibalization_pairs": cannibal_pairs,
        "services_missing_internal_links": no_internal_links,
        "neighbor_index": neighbor_index,
    }
    OUT_JSON.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_JSON}")

    lines = [
        "# Tentram Topical Cluster Report",
        "",
        f"Generated from {len(service_items)} service pillars and {len(blog_items)} blog posts using `{JINA_MODEL}` (Jina Cloud API) embeddings + cosine similarity.",
        "",
        "## Content coverage per service pillar",
        "",
        "Blog posts assigned to their most-similar service. Pillars with 0-1 posts are content gaps.",
        "",
    ]
    for s in service_items:
        posts = pillar_assignment[s["slug"]]
        flag = "  ⚠️ GAP" if len(posts) <= 1 else ""
        lines.append(f"### {s['title']} ({s['slug']}) — {len(posts)} post(s){flag}")
        for post in sorted(posts, key=lambda x: x["score"], reverse=True):
            lines.append(f"- {post['score']} — [{post['slug']}] {post['title']}")
        if not posts:
            lines.append("- (none)")
        lines.append("")

    lines.extend(["## Services missing internal links (site/src/data/content.ts internalLinks field)", ""])
    for slug in no_internal_links:
        lines.append(f"- {slug}")
    lines.append("")

    lines.extend([
        "## Potential cannibalization",
        "",
        f"Blog post pairs with cosine similarity >= {CANNIBAL_THRESHOLD} — review for distinct angles or merge.",
        "",
    ])
    if cannibal_pairs:
        for pair in sorted(cannibal_pairs, key=lambda x: x["score"], reverse=True):
            lines.append(f"- **{pair['score']}** — {pair['a']} / {pair['b']}")
    else:
        lines.append("None above threshold.")
    lines.append("")

    out_md_text = "\n".join(lines)
    OUT_MD.write_text(out_md_text, encoding="utf-8")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
