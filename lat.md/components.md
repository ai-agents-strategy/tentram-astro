# Components

Astro UI components rendering the Tentram landing page sections.

## Situations

Grid of service-situation cards (`src/components/Situations.astro`) driven by [[src/data/content.ts#situations]].

Each card can carry an optional `badge` label (e.g. "Baru") shown top-left over the image to highlight new/featured services — set via `Situation.badge` in the data entry.

## Layout & SEO

`src/layouts/Layout.astro` wraps every page with shared `<head>` tags: charset, viewport, favicon, description, and Open Graph / Twitter card meta.

`og:image` and `twitter:image` point at `public/aman-dengan-dokumentasi.png`, resolved to an absolute URL via `new URL(path, Astro.url)` so link previews (WhatsApp, social shares) render the correct thumbnail.
