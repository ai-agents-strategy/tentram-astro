# Blog

Content-collection-backed blog: Markdown posts in `src/content/blog/`, an archive at `/blog/`, and a per-post detail page.

## Content collection

[[src/content.config.ts#collections]] defines the `blog` collection via Astro's `glob` loader over `src/content/blog/**/*.md`, with a schema requiring `title`, `description`, `pubDate`, and optional `image` (a `public/` path, matching the plain-string image convention in [[src/data/content.ts]]) and `tags`.

Each post's `id` (derived by the loader from its filename) is used directly as the URL slug.

## Archive page

`src/pages/blog/index.astro` lists all posts sorted by `pubDate` descending as cards (image, date, title, description), linking to `/blog/{id}/`. Uses the shared [[lat.md/components#Components#Layout & SEO|Layout]] with blog-specific `title`/`description` overrides.

## Post detail page

`src/pages/blog/[slug].astro` pre-renders one page per collection entry via `getStaticPaths` and renders the Markdown body with `render()` from `astro:content`.

Passes the post's `title`, `description`, and `image` as the Layout's SEO overrides so each post gets correct link-preview metadata.

## Navigation

`src/components/SiteHeader.astro` links to `/blog/` from both the desktop nav and mobile menu.

The homepage-section anchors (`#situasi`, `#solusi`, `#alasan`, `#faq`) are rooted at `/#...` rather than bare `#...` so they still resolve correctly when clicked from `/blog/` pages.
