# Components

Astro UI components rendering the Tentram landing page sections.

## Situations

Grid of service-situation cards (`src/components/Situations.astro`) driven by [[src/data/content.ts#situations]].

Each card can carry an optional `badge` label (e.g. "Baru") shown top-left over the image to highlight new/featured services — set via `Situation.badge` in the data entry.
