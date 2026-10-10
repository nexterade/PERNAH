# PERNAH Visual Identity System

## Identity

**Symbol + Wordmark — The Continuity P**

PERNAH's visual language represents **Memory · Knowledge · Continuity** through archive, signal, connection, node, layer, and timeline metaphors.

Avoid literal botanical/nature motifs, brains, books, clouds, database cylinders, or AI robots as identity symbols unless a future brand decision explicitly introduces them.

## Typography

- **LEMON MILK** — brand, display headings, chapter numbers, high-level labels.
- **Open Sans** — body, navigation, metadata, controls, forms, and long reading.
- No remote font dependency is required. A licensed local font may be supplied by a user/deployment; otherwise the system falls back to generic sans-serif fonts.

## Color tokens

### Dark

| Token | Value | Meaning |
|---|---|---|
| `--bg` | `#141414` | primary background |
| `--surface` | `#1C1C1C` | elevated surface |
| `--surface-2` | `#101010` | deep surface |
| `--text` | `#F2F2F2` | primary text |
| `--muted` | `#A7A7A7` | secondary text |
| `--border` | `#2B2B2B` | structural border |
| `--accent` | `#2BEE34` | active/signal/action state |
| `--accent-soft` | `#102A12` | restrained accent surface |

### Light

| Token | Value | Meaning |
|---|---|---|
| `--bg` | `#F4F5EF` | primary background |
| `--surface` | `#FFFFFF` | elevated surface |
| `--surface-2` | `#ECEFE8` | secondary surface |
| `--text` | `#141414` | primary text |
| `--muted` | `#5F635F` | secondary text |
| `--border` | `#D9DDD5` | structural border |
| `--accent` | `#176B1D` | readable action/signal state |
| `--accent-soft` | `#E4F4E5` | restrained accent surface |

## Semantic rules

Green is a **signal**, not a decorative flood. Use it for active, connected, current, verified, focused, or actionable states.

Historical/current distinctions must not rely on color alone; pair color with text, shape, or labels.

## Shared interaction language

- Header: PERNAH symbol + wordmark, primary navigation, theme control.
- Sidebar: collapsible on desktop; drawer on mobile where applicable.
- Floating action: context-aware, compact, keyboard/focus accessible.
- Buttons: primary, secondary, ghost, disabled states.
- Inputs: clear focus ring and comfortable touch target.
- Provenance/status: concise labels such as Current, Historical, Derived, Verified.
- Motion: subtle; respect `prefers-reduced-motion`.

## Surface-specific expression

- **Creation Chronicle:** editorial archive, timeline, provenance, historical reading.
- **Glossary:** knowledge dictionary, alphabetical/category scanning, dense reference reading.
- **Web Interface:** focused local capture, clear status, minimal distraction.
- **Future Memory UI:** retrieval, timeline, relationships, canonical/derived distinction.

The system is shared; individual surfaces should not become visually identical templates.
