import { List } from "react-window";
import type { CSSProperties } from "react";

interface Column<T> {
  key: string;
  header: string;
  width: number;
  render?: (item: T, index: number) => React.ReactNode;
}

interface VirtualTableProps<T> {
  columns: Column<T>[];
  items: T[];
  height: number;
  rowHeight: number;
  className?: string;
  headerClassName?: string;
}

interface RowData<T> {
  columns: Column<T>[];
  items: T[];
}

export default function VirtualTable<T>({
  columns,
  items,
  height,
  rowHeight,
  className = "",
  headerClassName = "",
}: VirtualTableProps<T>) {
  if (items.length === 0) return null;

  const data: RowData<T> = { columns, items };

  return (
    <div className={`rounded-xl border border-black/5 dark:border-gray-800/50 overflow-hidden bg-white dark:bg-gray-900/40 ${className}`}>
      <div
        className={`flex items-center bg-gray-50 dark:bg-gray-800/30 border-b border-black/5 dark:border-gray-800/50 ${headerClassName}`}
      >
        {columns.map((col) => (
          <div
            key={col.key}
            className="px-3 py-2.5 text-[10px] font-mono font-semibold uppercase tracking-wider text-brand-dim dark:text-gray-400 shrink-0"
            style={{ width: col.width }}
          >
            {col.header}
          </div>
        ))}
      </div>
      <List
        rowComponent={Row as never}
        rowCount={items.length}
        rowHeight={rowHeight}
        rowProps={data as never}
        style={{ height: Math.min(height, items.length * rowHeight) }}
      />
    </div>
  );
}

function Row({
  index,
  style,
  columns,
  items,
}: {
  index: number;
  style: CSSProperties;
} & RowData<unknown>) {
  const item = items[index];
  return (
    <div
      style={style}
      className="flex items-center border-b border-black/5 dark:border-gray-800/50 hover:bg-black/[0.02] dark:hover:bg-white/[0.02] transition-colors"
    >
      {columns.map((col) => (
        <div
          key={col.key}
          className="px-3 py-2 text-sm truncate shrink-0"
          style={{ width: col.width }}
        >
          {col.render
            ? col.render(item, index)
            : String((item as Record<string, unknown>)[col.key] ?? "")}
        </div>
      ))}
    </div>
  );
}
