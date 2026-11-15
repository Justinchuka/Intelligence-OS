# Dashboard templates

All templates read one shared data model (the state pack) and render the same components: Overview, Discoveries, Trackers, Goals, Actions, Analysis, Library, Reports, History, Administration. They differ in **layout system**, not just colour. `ios.py render --template <id>` produces `dashboard.html`. Switching never touches data.

| id | Name | Layout system | Offered at setup |
|---|---|---|---|
| essential-minimal | Essential — Minimal | single centred column, large type, generous whitespace, collapsible sections, light | yes |
| intelligence-operations | Intelligence — Operations | dense 12-column monitoring grid, fixed left rail, status strip, sortable tables, dark high-contrast | yes |
| atmosphere-glass | Atmosphere — Glass | layered translucent cards floating over a gradient field, blur, top pill navigation | yes |
| editorial-magazine | Editorial — Magazine | asymmetric 2/3 + 1/3 editorial grid, featured lead discovery, serif story-led headings | after setup |
| mosaic-bento | Mosaic — Bento | variable-size tiles (1x1, 2x1, 2x2) mixing counters, sparklines and records | after setup |
| enterprise-structured | Enterprise — Structured | top bar + hierarchical left nav, breadcrumb, filter bar over wide tables, split analytic pane | after setup |
| atelier-soft-luxury | Atelier — Soft Luxury | warm pastel surfaces, thin dividers, centred elegant serif, airy card rows | after setup |
| observatory-data | Observatory — Data | visualisation-first: full-width timeline and trend charts above compact record tables | after setup |
| workspace-productivity | Workspace — Productivity | three columns: queue/filters | task list | detail and activity feed | after setup |
| frontier-experimental | Frontier — Experimental | off-grid asymmetric blocks, oversized numerals as anchors, vertical side navigation, scroll-snap sections | after setup |

Responsive: every layout collapses to one column below 760px. Layout presets (compact, expanded, research-focused, monitoring-focused) are `config.appearance.preset` values that change density and section order. Drag/resize/rearrange is **not** supported in a static artefact; section order and visibility are set in config. Custom templates: owner describes the layout in words; Claude writes a layout spec (`config.appearance.custom_template`: regions, order, density, typography, colour tokens) and re-renders; a layout is not just a palette.
Charts are drawn as inline SVG by the renderer (no external scripts).
