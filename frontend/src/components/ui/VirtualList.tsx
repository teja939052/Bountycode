import { List } from "react-window";
import type { CSSProperties } from "react";

interface VirtualListProps<T> {
  items: T[];
  height: number;
  itemHeight: number;
  renderItem: (item: T, index: number) => React.ReactNode;
  className?: string;
}

interface RowData<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
}

export default function VirtualList<T>({
  items,
  height,
  itemHeight,
  renderItem,
  className,
}: VirtualListProps<T>) {
  if (items.length === 0) return null;

  const data: RowData<T> = { items, renderItem };

  return (
    <List
      rowComponent={Row as never}
      rowCount={items.length}
      rowHeight={itemHeight}
      rowProps={data as never}
      className={className}
      style={{ height: Math.min(height, items.length * itemHeight) }}
    />
  );
}

function Row({
  index,
  style,
  items,
  renderItem,
}: {
  index: number;
  style: CSSProperties;
} & RowData<unknown>) {
  const item = items[index];
  return (
    <div style={style}>
      {renderItem(item, index)}
    </div>
  );
}
