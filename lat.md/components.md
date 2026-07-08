# Components

Astro UI components rendering the Tentram landing page sections.

## Situations

Grid of service-situation cards (`src/components/Situations.astro`) driven by [[src/data/content.ts#situations]].

Each card can carry an optional `badge` label (e.g. "Baru") shown top-left over the image to highlight new/featured services — set via `Situation.badge` in the data entry.

## Design Tokens

CSS custom properties in `src/styles/global.css` define the brand color system.

Burgundy primary (`--green`/`--green-hover`, var names kept for compat), gold accent (`--gold`), warm ivory/beige backgrounds (`--bg`/`--bg-section`), and official WhatsApp green (`--wa`/`--wa-hover`) reserved for WhatsApp CTAs only.

## WhatsApp CTAs

All WA-branded buttons (`.btn-wa` and the floating `.wa-sticky`) share the label "WhatsApp Us" and a common icon.

Icon is `src/components/icons/WhatsAppIcon.astro`, sized per placement (16px nav, 18px inline buttons, 26px floating sticky button). Used in `Hero.astro`, `FinalCta.astro` (primary button only — its secondary outline button keeps distinct "Chat via WhatsApp" copy), `BookingSteps.astro`, `SiteHeader.astro`, and `StickyWhatsApp.astro`.

## Layout & SEO

`src/layouts/Layout.astro` wraps every page with shared `<head>` tags: charset, viewport, favicon, description, and Open Graph / Twitter card meta.

`og:image` and `twitter:image` point at `public/aman-dengan-dokumentasi.png`, resolved to an absolute URL via `new URL(path, Astro.url)` so link previews (WhatsApp, social shares) render the correct thumbnail.
