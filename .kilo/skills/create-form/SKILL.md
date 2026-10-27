---
name: create-form
description: Form architecture, validation workflows, strongly-typed forms (useForm, useDialogForm, useWatchField), initialValues/reset lifecycle, and MCP discovery protocol for building forms and input controls with @wangs-ui/react-core.
---

# Skill: Form Architecture & Validation Workflows

Use this skill when building forms, data entry panels, modal forms, settings pages, or multipart forms in Wangs UI applications.

---

## 1. MCP Protocol & Component Rules (Mandatory Single Source of Truth)

Do **NOT** hardcode or guess prop names, component options, preset variations, or Storybook patterns in this document. Always retrieve component definitions, active props, and live Storybook implementations directly via MCP:

### Component & Form Documentation Protocol:

```json
get-documentation({ "id": "form" })
get-documentation({ "id": "field" })
get-documentation({ "id": "dialogform" })
get-documentation({ "id": "input" })
get-documentation({ "id": "numberinput" })
get-documentation({ "id": "select" })
get-documentation({ "id": "multiselect" })
get-documentation({ "id": "datepicker" })
get-documentation({ "id": "fileupload" })
```

### Live Storybook & Interactive Behavior Protocol:

```json
get-documentation-for-story({ "id": "form", "storyName": "Default" })
get-documentation-for-story({ "id": "form", "storyName": "AsyncInitialValues" })
get-documentation-for-story({ "id": "form", "storyName": "ConditionalFields" })
get-documentation-for-story({ "id": "form", "storyName": "CascadingOptions" })
get-documentation-for-story({ "id": "dialogform", "storyName": "Default" })
```

### Knowledge Graph & Symbol Usages:

```json
query_graph({ "query": "useForm" })
query_graph({ "query": "useDialogForm" })
query_graph({ "query": "useWatchField" })
```

---

## 2. Core Form Concepts & Lifecycle Mechanics

### A. Strongly Typed Form Instance (`useForm<TForm>()`)

`useForm<TForm>()` instantiates a `FormControl` natively bound to model type `TForm`.

- `Field`: `name` is strictly typed to `Path<TForm>` dot-paths.
- `useWatchField`: `name` is strictly typed to `Path<TForm>`.
- `control`: Provides `setInitialValues`, `setValues`, `setFieldError`, `setErrors`, and `reset`.

### B. Dynamic Initial Values & Baseline Reset (`setInitialValues` vs `setValues`)

1. **Async Initial Values (`control.setInitialValues(values)`)**:
   - Accepts a `Partial<TForm>` JSON object (e.g. fetched from an API).
   - Establishes an **immutable baseline** for registered fields. Once set for a field path, subsequent calls to `setInitialValues` for that path are ignored.
2. **Batch Value Updates (`control.setValues(values)`)**:
   - Accepts a `Partial<TForm>` JSON object to update current input values without altering the initial baseline.
3. **Reset Behavior (`control.reset()`)**:
   - Restores all fields back to their registered initial baseline values (set via `setInitialValues` or field `initialValue`) and clears all field-level validation errors.

### C. Primitive Component Integration Architecture

`Field` serves as the form integration wrapper for primitive UI input components (`Input`, `Select`, `MultiSelect`, `DatePicker`, `NumberInput`, `FileUpload`, `Calendar`, etc.):

- **Children Render Callback**: `Field` yields `{ fieldProps, fieldState }`.
- **`fieldProps`**: Pass directly to primitive inputs (`<Input {...fieldProps} />`). Contains `name`, `value`, `ref`, `onChange`.
- **`fieldState`**: Provides `invalid`, `error`, `isDirty`, `isPending`. Pass `invalid={fieldState.invalid}` to primitive components for accessibility and validation styling.

---

## 3. High-Level Form Architecture & Usage Patterns

### Pattern 1: Page Forms (`useForm<T>()`)

```tsx
import Button from '@wangs-ui/react-core/primitive/button';
import { useForm } from '@wangs-ui/react-core/primitive/form';
import Input from '@wangs-ui/react-core/primitive/input';
import { useI18n } from '@wangs-ui/react-i18n';
import { useEffect } from 'react';

interface UserProfile {
  name: string;
  email: string;
}

export function UserProfilePage({ userId }: { userId: string }) {
  const { t } = useI18n();
  const { Form, Field, control } = useForm<UserProfile>();

  useEffect(() => {
    async function loadData() {
      const data = await fetchUserData(userId);
      // Establish immutable initial baseline from async response
      control.setInitialValues(data);
    }
    loadData();
  }, [userId, control]);

  return (
    <Form control={control} onSubmit={(values) => saveUserData(values)}>
      <Field required label={t('Full Name')} name="name">
        {({ fieldProps, fieldState }) => (
          <Input {...fieldProps} invalid={fieldState.invalid} placeholder={t('Enter full name')} />
        )}
      </Field>

      <div className="flex gap-2">
        <Button
          label={t('Reset')}
          type="button"
          variant="outlined"
          onClick={() => control.reset()}
        />
        <Button label={t('Save')} type="submit" />
      </div>
    </Form>
  );
}
```

### Pattern 2: Modal Forms (`useDialogForm<T>()`)

```tsx
import Button from '@wangs-ui/react-core/primitive/button';
import { useDialogForm } from '@wangs-ui/react-core/primitive/dialogform';
import Input from '@wangs-ui/react-core/primitive/input';
import { useI18n } from '@wangs-ui/react-i18n';
import { useState } from 'react';

interface EditUserForm {
  name: string;
}

export function EditUserModal() {
  const { t } = useI18n();
  const [open, setOpen] = useState(false);
  const { DialogForm, Field, control } = useDialogForm<EditUserForm>();

  return (
    <>
      <Button label={t('Edit')} onClick={() => setOpen(true)} />
      <DialogForm
        closeOnSubmit
        control={control}
        header={t('Edit User')}
        open={open}
        onOpenChange={setOpen}
        onSubmit={(values) => handleSave(values)}
      >
        <Field required label={t('Full Name')} name="name">
          {({ fieldProps, fieldState }) => <Input {...fieldProps} invalid={fieldState.invalid} />}
        </Field>
      </DialogForm>
    </>
  );
}
```

---

## 4. Mandatory Implementation Guidelines

1. **Query MCP First**: Never guess component props or story examples — inspect via MCP tools.
2. **Granular Primitive Subpaths**: Import primitives via exact subpath modules (`@wangs-ui/react-core/primitive/form`, `@wangs-ui/react-core/primitive/dialogform`, `@wangs-ui/react-core/primitive/input`).
3. **i18n Localization**: Wrap all user-visible labels, placeholders, and error strings in `t('...')` from `@wangs-ui/react-i18n`.
4. **Server Error Mapping**: Map HTTP validation errors (e.g. 422 response) into the form using `control.setErrors(apiErrors)`.
