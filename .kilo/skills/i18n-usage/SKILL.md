---
name: i18n-usage
description: Comprehensive guidelines for application internationalization, JIT translations (t), ICU formatting, and locale-aware formatting with @wangs-ui/react-i18n.
---

# Skill: Application Internationalization & Formatting Protocol

Use this skill when implementing multi-language interfaces, translating user-facing text, formatting dates, times, currencies, or numbers in React applications built with Wangs UI and `@wangs-ui/react-i18n`.

---

## 1. The MCP Discovery Protocol (Single Source of Truth)

Do **NOT** guess component localization contracts, language switcher variants, or datepicker props. Query the MCP server dynamically to inspect exact props and live story implementations:

### Inspect Localized Component Contracts:

```json
get-documentation({ "id": "languageswitcher" })
get-documentation({ "id": "currencyinput" })
get-documentation({ "id": "datepicker" })
get-documentation({ "id": "select" })
get-documentation({ "id": "datatable" })
```

### Inspect Live Story Implementations:

```json
get-documentation-for-story({ "id": "languageswitcher", "storyName": "Basic" })
get-documentation-for-story({ "id": "currencyinput", "storyName": "Basic" })
get-documentation-for-story({ "id": "datepicker", "storyName": "Default" })
```

---

## 2. Root Provider Setup (`WangsUiI18nProvider`)

Wrap the application root with `WangsUiI18nProvider` from `@wangs-ui/react-i18n` to enable dynamic JIT translations, versioned cache invalidation, and locale context:

```tsx
import { WangsUiI18nProvider } from '@wangs-ui/react-i18n';
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <WangsUiI18nProvider defaultLocale="en" baseUrl={import.meta.env.VITE_API_URL || ''}>
      <App />
    </WangsUiI18nProvider>
  </React.StrictMode>,
);
```

---

## 3. Translation Protocol with `useI18n()`

The `@wangs-ui/react-i18n` package uses a Just-In-Time (JIT) translation architecture where natural English text strings serve as database keys.

### A. Consumer-Level Translation for `ReactNode` Props (Mandatory)

All user-facing text props in Wangs UI components (`placeholder`, `label`, `emptyMessage`, `header`, `tooltip`, etc.) are typed as `ReactNode` and rendered as-is. Components do **NOT** automatically translate custom strings. Translation **MUST** be called at the application/consumer level:

```tsx
import { useI18n } from '@wangs-ui/react-i18n';
import Button from '@wangs-ui/react-core/primitive/button';
import DataTable from '@wangs-ui/react-core/primitive/datatable';
import Select from '@wangs-ui/react-core/primitive/select';

export function OrderList() {
  const { t } = useI18n();

  return (
    <div>
      <Select placeholder={t('Search category...')} />
      <DataTable emptyMessage={t('No orders found')} />
      <Button label={t('Create new order')} />
    </div>
  );
}
```

### B. Natural English Sentence Keys

Always write full, natural English sentences as translation keys. Never use artificial dotted namespace keys:

```tsx
// ✅ Good — Natural English
t('Invoice Summary');
t('Are you sure you want to delete this customer?');

// ❌ Bad — Artificial dotted keys
t('invoice.summary.title');
t('dialog.delete.customer.confirm');
```

### C. Named Variable Interpolation (Single Braces `{var}`)

Pass interpolation values inside a plain object using descriptive named variables. This provides crucial semantic context for AI translation engines:

```tsx
// ✅ Good — Named variables provide context
t('Upload {count} files to {groupName}', { count: 5, groupName: 'Marketing' });
t('Welcome back, {userName}!', { userName: user.name });

// ❌ Bad — Concatenation or positional arguments
t('Welcome back, ' + user.name);
t('Upload {0} files to {1}', 5, 'Marketing');
```

### D. ICU Pluralization & Zero-State (`=0`)

Always handle singular, plural, and zero states directly within ICU MessageFormat strings. Do **NOT** use JavaScript ternary operators:

```tsx
// ✅ Good — Clean ICU pluralization with zero-state handling
t('{count, plural, =0 {No items selected} one {1 item selected} other {{count} items selected}}', {
  count: selectedCount,
});

// ❌ Bad — Manual JS branching
selectedCount === 0
  ? t('No items selected')
  : selectedCount === 1
    ? t('1 item selected')
    : t('{count} items selected', { count: selectedCount });
```

### E. Rich Text / Annotated Strings

Use standard supported HTML tags (`<a>`, `<b>`, `<i>`, `<u>`, `<s>`, `<br/>`, `<sub>`, `<sup>`, `<code>`, `<mark>`) for inline styling. Tags are automatically parsed into React elements without custom regex or string manipulation:

```tsx
import Link from '@wangs-ui/foundation/theme/Link';

t('You have selected <b>{count} items</b>. Click <a>here</a> to review.', {
  count: selectedCount,
  a: (chunks) => <Link href="/review">{chunks}</Link>,
});
```

---

## 4. Locale Formatting Protocol with `useLocaleFormatter()`

For locale-aware formatting of dates, relative times, currencies, numbers, and display names, use the dedicated `useLocaleFormatter()` hook. All functions automatically adapt to the active locale without triggering backend database requests:

```tsx
import { useLocaleFormatter } from '@wangs-ui/react-i18n';

export function SummaryCard({ updatedAt, amount, count }: Props) {
  const {
    formatDate,
    formatRelativeTime,
    formatCurrency,
    formatNumber,
    formatDisplayName,
    formatList,
    truncateText,
  } = useLocaleFormatter();

  return (
    <div>
      {/* Date formatting with Go tokens or date-fns tokens, and timezone */}
      <p>{formatDate(new Date(), 'dd MMMM yyyy, HH:mm', 'Asia/Jakarta')}</p>

      {/* Relative time */}
      <p>{formatRelativeTime(updatedAt)}</p>

      {/* Currency formatting */}
      <p>{formatCurrency(amount, 'IDR')}</p>

      {/* Number formatting with locale grouping */}
      <p>{formatNumber(count)}</p>

      {/* ISO code to localized name */}
      <p>{formatDisplayName('id', 'language')}</p>

      {/* Localized list */}
      <p>{formatList(['Finance', 'Operations', 'IT'])}</p>

      {/* Emoji & multi-byte safe text truncation */}
      <p>{truncateText('Long product description with emojis 🚀', 20)}</p>
    </div>
  );
}
```

> [!NOTE]
> Formatters MUST NOT be called as standalone `t()` keys (e.g. `t(formatRelativeTime(date))`). Instead, pass the formatted result as a named variable:
>
> ```tsx
> const { t } = useI18n();
> const { formatRelativeTime } = useLocaleFormatter();
> const label = t('Updated {time}', { time: formatRelativeTime(updatedAt) });
> ```

---

## 5. Language Switching UI Integration

Connect the Wangs UI `LanguageSwitcher` primitive directly with `useI18n()` state:

```tsx
import LanguageSwitcher from '@wangs-ui/react-core/primitive/languageswitcher';
import { useI18n } from '@wangs-ui/react-i18n';

export function HeaderLanguageSwitcher() {
  const { locale, setLocale, languageOptions } = useI18n();

  return (
    <LanguageSwitcher
      options={languageOptions}
      value={locale}
      onChange={(code) => setLocale(code)}
    />
  );
}
```

---

## 6. Strict Behavioral Constraints (MUST NOT)

- **NO Formatters Destructured from `useI18n()`:** Formatters are isolated in `useLocaleFormatter()`. Never attempt to import `formatDate` or `formatCurrency` from `useI18n()`.
- **NO String Concatenation in `t()` Keys:** Never concatenate strings or use dynamic template literals (e.g. `t('Hello ' + user.name)` or ``t(`Hello ${user.name}`)``). This creates infinite distinct keys in the translation database and prevents caching.
- **NO Manual Zero-State JavaScript Branching:** Always use ICU `=0` syntax inside a single plural key.
- **NO Dotted Artificial Translation Keys:** Never use dotted keys like `t('app.header.title')`. Use natural English sentences.
- **NO Custom Markdown Formatting Symbols:** Do not use `*bold*` or `_italic_` in translation keys. Use valid HTML tags like `<b>bold</b>`.
- **NO Hardcoded Static Translation Dictionaries:** Do not bundle static translation files (`id.json`, `zh.json`). The JIT backend broker manages translations dynamically.
- **NO Unnecessary English Key Modifications:** Minor typos or punctuation changes in keys create orphaned entries in the translation backend and trigger new AI translation costs.
