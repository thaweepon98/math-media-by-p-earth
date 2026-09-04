---
version: 1.0
name: math-media-by-p-earth design system
description: A warm, forest-green teaching-materials site inspired by Tomorro's fintech UI (getdesign.md). Deep forest-green chrome, a lime-green accent lifted straight from Tomorro's CTA button, and a soft sage/cream canvas replace the site's original navy-and-pastel palette. Sarabun carries all Thai typography; structure and components are unchanged from the original build — only the token values shifted.

colors:
  primary: "#1C3B22"
  primary-2: "#2E5936"
  secondary: "#FF8A3D"
  secondary-light: "#FFB37A"
  accent: "#68EF3F"
  accent-light: "#8AF25E"
  accent-2: "#3FA82E"
  bg: "#F3F7EC"
  card: "#FFFFFF"
  tag-bg: "#E3F3D8"
  info-box-bg: "#EEF7E6"
  text: "#2D3748"
  muted: "#718096"
  border: "#E2E8F0"
  shadow-tint: "rgba(28,59,34,0.10)"

typography:
  font-family: "'Sarabun', sans-serif"
  weights: [300, 400, 500, 600, 700, 800]
  header-h1:
    fontSize: "1.5–1.6rem"
    fontWeight: 700–800
    letterSpacing: "1px (when weight 800)"
  card-title:
    fontSize: "1.1–1.15rem"
    fontWeight: 700
    color: "{colors.primary}"
  body:
    fontSize: "0.85–1rem"
    lineHeight: 1.5–1.7
    color: "{colors.text}"
  muted-caption:
    fontSize: "0.72–0.9rem"
    color: "{colors.muted}"

radius:
  card: 16px
  pill: 999px
  formula-box: 12px
  info-box: 10px

spacing:
  page-max-width: 1000–1100px
  card-padding: "18–24px"
  grid-gap: 18px

components:
  header:
    backgroundColor: "linear-gradient(135deg, {colors.primary} 0%, {colors.primary-2} 100%)"
    textColor: "#ffffff"
    padding: "16–32px 24–40px"
  lang-toggle:
    backgroundColor: "rgba(255,255,255,.15)"
    border: "1.5px solid rgba(255,255,255,.5)"
    textColor: "#ffffff"
    rounded: "{radius.pill}"
  card:
    backgroundColor: "{colors.card}"
    border: "1px solid {colors.border}"
    rounded: "{radius.card}"
    boxShadow: "0 4px 24px {colors.shadow-tint}"
    hover: "translateY(-3px), deeper shadow"
  tag-pill:
    backgroundColor: "{colors.tag-bg}"
    textColor: "{colors.primary}"
    rounded: "{radius.pill}"
    fontSize: "0.72rem"
    fontWeight: 600
  tab-btn:
    textColor: "{colors.muted}"
    active:
      textColor: "{colors.primary}"
      borderBottomColor: "{colors.primary}"
      backgroundColor: "{colors.tag-bg}"
  formula-box:
    backgroundColor: "linear-gradient(135deg, {colors.primary}, {colors.primary-2})"
    textColor: "#ffffff"
    rounded: "{radius.formula-box}"
  info-box:
    backgroundColor: "{colors.info-box-bg}"
    borderLeft: "4px solid {colors.primary}"
    rounded: "{radius.info-box}"
  back-link:
    textColor: "#ffffff (on header) or {colors.primary} (on crumb)"
---

## Overview

This is the live design system for **รวมสื่อการสอน by P'Earth** (math-media-by-p-earth), a Thai-language teaching-materials site with a home page, per-subject and per-topic index pages, and dozens of interactive HTML lessons (GeoGebra-style graphs, drag-and-drop widgets, quizzes).

The palette was picked by browsing [getdesign.md](https://getdesign.md)'s catalog and landing on **Tomorro** (a fintech contract-management site: deep forest-green hero, bright lime-green CTA pills). Colors were extracted from Tomorro's live site via computed styles, then mapped onto this project's existing CSS-variable structure — the same `--primary` / `--secondary` / `--accent` / `--bg` tokens every page already declared, just repointed to new hex values. No layout, component, or interaction changes were made; this is a palette swap, not a redesign.

**Key characteristics:**
- Deep forest-green (`{colors.primary}`) replaces the original navy for headers, links, tab underlines, and card titles — same gradient structure (`135deg`, two stops), just greener.
- Tomorro's actual lime-green CTA color (`{colors.accent}` — `#68EF3F`) replaces the old mint/teal accent used inside interactive widgets.
- The old rose/pink secondary became a warm amber (`{colors.secondary}` — `#FF8A3D`), keeping a warm counterpoint to the green without clashing.
- Page background shifted from pale blue to a soft sage/cream (`{colors.bg}` — `#F3F7EC`), and every purple/blue-tinted shadow became a green-tinted one (`{colors.shadow-tint}`).
- Sarabun remains the only typeface — it already covers the full weight range (300–800) this site's headers and body copy need, and Thai-script support was non-negotiable.
- **Scope discipline:** only the *shared brand chrome* (header, links, tags, card shadows, formula/info boxes) was reskinned across all 31 HTML files. Widget-internal functional colors — correct/incorrect states, category legends in set-operations diagrams, the dark 3D canvas in the conic-sections unit — were deliberately left untouched, since they carry meaning specific to each lesson and recoloring them without reviewing each widget individually risked breaking usability.

## Colors

### Brand
- **Primary — Forest Green** (`{colors.primary}` — `#1C3B22`): header/hero gradient start, all links, card titles, active tab text + underline, info-box border and bold text. Site's dominant identity color.
- **Primary 2 — Gradient stop** (`{colors.primary-2}` — `#2E5936`): the second stop in every two-tone gradient (header, formula boxes). Lighter, slightly more olive than primary.
- **Accent — Lime** (`{colors.accent}` — `#68EF3F`): lifted directly from Tomorro's "Schedule a demo" button. Used inside interactive widgets wherever the old mint/teal accent appeared (fills, highlight strokes, gradient stops in drag-and-drop games).
- **Accent 2 — Deep green** (`{colors.accent-2}` — `#3FA82E`): a third, darker green tier for widgets that needed a 3-way palette (e.g. stacked gradient fills).
- **Secondary — Amber** (`{colors.secondary}` — `#FF8A3D`) and **Secondary light** (`{colors.secondary-light}` — `#FFB37A`): warm counterpoint used where a widget needs a color clearly distinct from the green family (e.g. distinguishing two draggable elements).

### Surface
- **Page background** (`{colors.bg}` — `#F3F7EC`): soft sage/cream, replaces the original pale blue across every page.
- **Card** (`{colors.card}` — `#FFFFFF`): unchanged, pure white for all cards and panels.
- **Tag pill background** (`{colors.tag-bg}` — `#E3F3D8`): pale sage-green fill for subject/topic tag pills, pairs with primary-green text.
- **Info-box background** (`{colors.info-box-bg}` — `#EEF7E6`): pale sage fill for disclaimer/note callouts.

### Text
- **Text** (`{colors.text}` — `#2D3748`): unchanged — body copy on light surfaces.
- **Muted** (`{colors.muted}` — `#718096`): unchanged — captions, descriptions, inactive tab labels.

### Shadow
- **Shadow tint** (`{colors.shadow-tint}` — `rgba(28,59,34,0.10)`): replaces the original purple/navy-tinted `rgba(108,99,255,…)` / `rgba(27,59,111,…)` — every card and button shadow is now green-tinted instead of blue/purple-tinted.

## Typography

Single family throughout: **Sarabun** (`@import` from Google Fonts, weights 300–800), chosen for full Thai-script coverage. No substitution needed — this was already the project's font before the rebrand and required no change.

- Header `h1`: 1.5–1.6rem, weight 700–800, +1px letter-spacing at weight 800.
- Card title: 1.1–1.15rem, weight 700, colored `{colors.primary}`.
- Body copy: 0.85–1rem, line-height 1.5–1.7, `{colors.text}`.
- Muted/caption text: 0.72–0.9rem, `{colors.muted}`.

## Components

- **Header** — two-stop diagonal gradient (`{colors.primary}` → `{colors.primary-2}`), white text, houses the page title, subtitle, an EN/TH language toggle pill, and (on sub-pages) a back-link.
- **Card** — white panel, `{radius.card}` (16px) corners, 1px `{colors.border}` outline, soft green-tinted shadow that deepens on hover with a `-3px` lift.
- **Tag pill** — small rounded-pill label inside a card, sage-green fill, forest-green text, 600 weight.
- **Tab bar** (content pages) — horizontal tabs under the header; active tab gets primary-green text, a primary-green underline, and a sage-tinted background.
- **Formula box** — same two-stop gradient as the header, white bold text, used to highlight a key equation.
- **Info box** — pale sage background with a 4px primary-green left border, used for asides/notes/disclaimers.
- **Lang toggle** — translucent white pill button sitting in the header's top-right corner.

## Do's and Don'ts

### Do
- Keep `{colors.primary}` / `{colors.primary-2}` as the only gradient pair used for headers and formula boxes — that two-stop diagonal gradient is this site's signature shape.
- Use `{colors.accent}` (lime) sparingly inside widgets, the way Tomorro uses it: as the one "this is interactive/positive" signal, not as a general decoration.
- Route all new Thai copy through Sarabun — no other typeface is loaded.
- When adding a new page (per `CLAUDE.md`), copy the color block from an existing `index.html` verbatim — every page embeds its own `<style>`, so the tokens must be copied, not linked.

### Don't
- Don't touch the widget-internal functional colors (success/error states, multi-category legends, the dark 3D conic-section canvas) as part of a "theme" pass — they were intentionally left out of this rebrand and need per-widget review, not a global find-and-replace.
- Don't introduce a third gradient pair — the header/formula-box gradient is the only one this system uses.
- Don't swap in a second typeface for Latin/numeral text — Sarabun's Latin glyphs already cover it.

## Provenance

Palette sourced from [tomorro.com](https://tomorro.com) via `getdesign.md`'s catalog (Fintech → Tomorro). Exact values pulled from the live site's computed styles: hero background `rgb(18,35,20)`, CTA button `rgb(104,239,63)`, on-light text `rgb(39,63,43)`. Adapted (not copied 1:1) to fit this project's existing lighter, content-forward layout rather than Tomorro's full-bleed dark-hero marketing style.
