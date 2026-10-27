---
name: layout-navigation
description: Architecture, navigation hierarchies, and MCP discovery protocol for AppLayout, Sidebar, Breadcrumb, and Tabs in Wangs UI.
---

# Skill: Application Layout & Navigation Hierarchy

Use this skill when constructing application shells, multi-level sidebars, page headers, breadcrumbs, or tabbed views with `@wangs-ui/react-core`.

---

## 1. MCP Inspection Protocol (Mandatory Single Source of Truth)

Do **NOT** guess layout block slots, sidebar item interfaces, or breadcrumb props. Query the MCP server dynamically to inspect exact contracts and live story implementations:

### Inspect Layout & Navigation Contracts:

```json
get-documentation({ "id": "applayout" })
get-documentation({ "id": "sidebar" })
get-documentation({ "id": "breadcrumb" })
get-documentation({ "id": "tabs" })
```

### Inspect Live Story Implementations:

```json
get-documentation-for-story({ "id": "applayout", "storyName": "Default" })
get-documentation-for-story({ "id": "sidebar", "storyName": "Default" })
get-documentation-for-story({ "id": "breadcrumb", "storyName": "Default" })
get-documentation-for-story({ "id": "tabs", "storyName": "Default" })
```

### Inspect Knowledge Graph & Usages:

```json
query_graph({ "query": "AppLayout" })
query_graph({ "query": "Sidebar" })
```

---

## 2. Layout Architecture & Mental Model

1. **Top-Level App Shell (`AppLayout`)**:
   Provides structured slots for `sidebar`, `header`, and main content view, handling responsive viewport scaling and mobile navigation overlays.
2. **Hierarchical Menu (`Sidebar`)**:
   Renders single and nested navigation items, active route indicators, collapsible state, and notification badges.
3. **Breadcrumb Trail (`Breadcrumb`)**:
   Maintains clear navigational hierarchy on page headers.
4. **Tabbed Sub-Views (`Tabs`)**:
   Organizes complex entity detail views or multi-section settings into distinct tabbed panels.

---

## 3. Mandatory Implementation Rules

1. **Query MCP for Current Code Patterns**: Inspect `applayout` and `sidebar` stories via MCP before assembling the layout.
2. **Strict Subpath Imports**: Import layout blocks via `@wangs-ui/react-core/blocks/*` and primitives via `@wangs-ui/react-core/primitive/*`.
3. **Consistent Spacing Grid**: Use standard container padding (`p-6` or `p-3xl`) across page contents.
4. **Page Hierarchy Alignment**: Every page view inside the layout must provide a clear `.heading-1` hierarchy and synchronized breadcrumbs.
5. **Translate Navigation Labels**: Wrap all sidebar item labels and breadcrumb texts in `t('...')` from `@wangs-ui/react-i18n`.
