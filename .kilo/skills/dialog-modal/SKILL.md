---
name: dialog-modal
description: Patterns, overlay selection criteria, and MCP discovery protocol for Dialog, Modal, and DialogForm components in Wangs UI.
---

# Skill: Dialog, Modal & Overlay Workflows

Use this skill when building interactive modals, create/edit dialog forms, destructive action confirmations, or slide-in overlay panels.

---

## 1. MCP Inspection Protocol (Mandatory Single Source of Truth)

Do **NOT** guess overlay props, event names, or footer slots. Query the MCP server dynamically to inspect exact contracts and live story implementations:

### Inspect Overlay Contracts:

```json
get-documentation({ "id": "dialog" })
get-documentation({ "id": "dialogform" })
get-documentation({ "id": "modal" })
get-documentation({ "id": "toast" })
```

### Inspect Live Story Implementations:

```json
get-documentation-for-story({ "id": "dialog", "storyName": "Confirmation" })
get-documentation-for-story({ "id": "dialogform", "storyName": "Default" })
get-documentation-for-story({ "id": "modal", "storyName": "Default" })
```

### Inspect Knowledge Graph & Usages:

```json
query_graph({ "query": "Dialog" })
query_graph({ "query": "DialogForm" })
```

---

## 2. Overlay Selection Matrix

| Component        | Primary Use Case                              | Key Characteristics                                                                   |
| :--------------- | :-------------------------------------------- | :------------------------------------------------------------------------------------ |
| **`Dialog`**     | Confirmations, alerts, simple detail previews | Standard `header`, `footer`, and body layout; built-in backdrop dimming.              |
| **`DialogForm`** | Create/Edit forms embedded inside a dialog    | Built-in form submit/cancel action bar, dirty state tracking, and submit lifecycle.   |
| **`Modal`**      | Slide-in drawers, complex custom viewports    | Headless overlay primitive with flexible animations, size variants, and drawer modes. |

---

## 3. Mandatory Implementation Rules

1. **Query MCP for Current Code Patterns**: Always inspect `dialog`, `dialogform`, or `modal` stories via MCP before writing overlay code.
2. **Strict Subpath Imports**: Import via `@wangs-ui/react-core/primitive/dialog`, `@wangs-ui/react-core/primitive/dialogform`, `@wangs-ui/react-core/primitive/modal`, or `@wangs-ui/react-core/primitive/toast`.
3. **Prevent Dismissal During Async Mutations**: Guard the close handler so users cannot accidentally dismiss the dialog while a mutation request is in-flight.
4. **Coordinate with Toast Notifications**: Trigger feedback toasts on successful creation, update, or deletion actions.
5. **Translate All Overlay Copy**: All dialog titles, confirmation descriptions, and button labels must be localized using `t('...')` from `@wangs-ui/react-i18n`.
