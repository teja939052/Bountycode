---
name: data-table
description: Architecture, workflows, and MCP discovery protocol for building DataTables with sorting, pagination, filtering, selection, and export.
---

# Skill: DataTable Architecture & Integration Workflows

Use this skill when implementing data grids, server-paginated tables, filterable listing views, or batch management interfaces with `@wangs-ui/react-core`.

---

## 1. MCP Inspection Protocol (Mandatory Single Source of Truth)

Do **NOT** guess table prop names or hardcode table structures. Query the MCP server dynamically to inspect exact TypeScript signatures, live story implementations, and companion controls:

### Inspect Component Contracts:

```json
get-documentation({ "id": "datatable" })
get-documentation({ "id": "exportbutton" })
get-documentation({ "id": "filtercontainer" })
get-documentation({ "id": "bulkactionbutton" })
```

### Inspect Live Story Implementations:

```json
get-documentation-for-story({ "id": "datatable", "storyName": "Basic" })
get-documentation-for-story({ "id": "datatable", "storyName": "ServerPagination" })
get-documentation-for-story({ "id": "datatable", "storyName": "Sortable" })
get-documentation-for-story({ "id": "datatable", "storyName": "MultipleSelection" })
get-documentation-for-story({ "id": "datatable", "storyName": "CustomColumn" })
get-documentation-for-story({ "id": "exportbutton", "storyName": "WithTable" })
```

### Inspect Knowledge Graph & Usages:

```json
query_graph({ "query": "DataTable" })
query_graph({ "query": "useDataTableFetch" })
```

---

## 2. Core Architecture & Mental Model

The Wangs UI `DataTable` is built on a modular, headless-first architecture:

1. **Declarative Column Definitions (`TableColumn<T>[]`)**:
   Columns are configured as typed array objects, not as JSX children. Check `get-documentation({ "id": "datatable" })` for column field types.
2. **Table Instance Hook (`useDataTable`)**:
   Coordinates table state (sorting, pagination, selection, column ordering, pinning, visibility).
3. **Data Fetching Hook (`useDataTableFetch`)**:
   Feeds server-side data, handles loading indicators, manages query parameters (`search`, `filter`, `sort`, `page`, `limit`), and debounces requests automatically.
4. **Ecosystem Companions**:
   - `FilterContainer` & `FilterToggleButton`: Filter popovers and faceted search.
   - `ExportButton`: Client/server export to Excel, CSV, PDF, or Print.
   - `BulkActionButton`: Contextual batch actions triggered when rows are selected.
   - `CustomColumn`: User-controlled column ordering, visibility toggling, and pinning.

---

## 3. Mandatory Implementation Rules

1. **Query MCP for Current Code Patterns**: Always run `get-documentation-for-story` for `datatable` before drafting code.
2. **Strict Subpath Imports**: Import via `@wangs-ui/react-core/primitive/datatable` and companion primitive paths.
3. **Always Translate Visible Copy**: All column header labels, empty state messages, and action button labels must be wrapped in `t('...')` from `@wangs-ui/react-i18n`.
4. **Stable Row Identity**: Always configure a unique key identifier for stable selection and row identity.
