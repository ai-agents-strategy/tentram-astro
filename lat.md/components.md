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

## Property Management landing page (now the homepage)

`/` (`src/pages/index.astro`) is the Property Management conversion page for apartment owners, promoted to the homepage. The old `/property-management/` path now redirects to `/` via `redirects` in `astro.config.mjs`.

Content (target-owner segments, four service-area cards, a pricing table, a 5-step onboarding flow, FAQ) is inlined directly in the page rather than added to `src/data/content.ts#services`, since it doesn't fit the `Service` interface used by cleaning jobs. It reuses the same design tokens and card/step/FAQ markup patterns as `src/pages/layanan/[slug].astro` for visual consistency, and emits its own `Service` + `FAQPage` JSON-LD the same way.

The hero headline leads with a passive-income hook ("Duduk Manis, Apartemen Anda Tetap Hasilkan Passive Income"), styled with the same `em`-accent pattern as [[lat.md/components#Components#General cleaning-service page (moved to /jasa-kebersihan/)|Hero.astro's headline on the old homepage]]. All five [[lat.md/apartment-management-strategy#Apartment Management Strategy for Tentram Cleaning Service|property management funnel blog articles]] link here (updated from `/property-management/` to `/`), and the page links back to each article. It is intentionally not linked from `SiteHeader.astro`'s nav (which still points to `/jasa-kebersihan/` sections and `/layanan/`) — the homepage is reached via `/`, the blog funnel, and direct/ad traffic.

## General cleaning-service page (moved to /jasa-kebersihan/)

`/jasa-kebersihan/` (`src/pages/jasa-kebersihan/index.astro`) holds the general cleaning-service homepage content displaced when [[lat.md/components#Components#Property Management landing page (now the homepage)|the Property Management page became the homepage]]: `Hero`, `Situations`, `WhyTentram`, `BeforeAfter`, `BookingSteps`, `Reviews`, `ServiceArea`, `Faq`, `FinalCta`.

`SiteHeader.astro`'s in-page anchor links (`#situasi`, `#solusi`, `#alasan`, `#faq`) point at sections defined here (`Situations.astro`, `WhyTentram.astro`, `Faq.astro`), so the nav — rendered on every page via the shared header — prefixes them with `/jasa-kebersihan/` rather than assuming they're on the current page.

## App deep-link redirect pages

`/register-pin` and `/reset-pin` are standalone light landing pages for the mobile app: each tries to deep-link into the app and shows store download badges as fallback.

Both pages (`src/pages/register-pin.astro`, `src/pages/reset-pin.astro`) are thin wrappers around the shared `src/components/AppRedirect.astro`, passing their deep link via the `appScheme` prop (`tentram://register-pin`, `tentram://reset-pin`). On load an inline script navigates to that custom scheme, forwarding the page's query string (e.g. the PIN token); if the app is not installed the navigation silently fails and the page stays visible. The component shows the Tentram logo, "Unduh atau Buka Tentram" heading, and Google Play / App Store badge links (`public/googleplay.png`, `public/appstore.png`). Store URLs (`PLAY_URL`, `APPSTORE_URL`) point to the live listings: Google Play `id.tentram.app`, App Store `tentram-id` id6751527547. The pages are `noindex` and deliberately do not use [[lat.md/components#Components#Layout & SEO|the shared Layout]] (no GTM/Ads tracking, own light styling: white card with soft shadow on `#eef0f2` page background).

## Layout & SEO

`src/layouts/Layout.astro` wraps every page with shared `<head>` tags: charset, viewport, favicon, description, and Open Graph / Twitter card meta.

`title`, `description`, and `ogImage` are optional props on the layout, defaulting to the homepage's copy and `/aman-dengan-dokumentasi.png` — pages like [[lat.md/blog#Blog]] override them per-page. `og:image`/`twitter:image` are resolved to an absolute URL via `new URL(ogImage, Astro.url)` so link previews (WhatsApp, social shares) render the correct thumbnail.

### Google Tag Manager

GTM container `GTM-PXRLQC8G` is wired into `src/layouts/Layout.astro` following Google's required placement: the loader script immediately after the `<head>` opening tag, and the `<noscript>` fallback iframe immediately after `<body>` opens.

The loader script uses Astro's `is:inline` directive so Astro ships it byte-for-byte instead of processing/bundling it as a module — required for the GTM snippet's IIFE to run as-is.

### Google Ads conversion tracking

Clicking any outbound WhatsApp link fires a Google Ads conversion event (`AW-18308049507/MDFHCPjhtc0cEOPU-plE`), so ad spend can be attributed to WA leads.

`src/layouts/Layout.astro` loads `gtag.js` and defines `gtag_report_conversion()` in `<head>` (Google's standard snippet, `is:inline` for the same reason as the GTM loader). A single delegated click listener at the end of `<body>` matches any `a[href*="wa.me"]` — this covers all [[lat.md/components#Components#WhatsApp CTAs]] without per-component wiring. Since every WA link uses `target="_blank"`, the conversion call is fired without a redirect URL — no `event_callback` navigation is needed because the new tab already opens natively.
