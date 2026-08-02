import { useMemo } from "react";

const CELL_SIZE = 10;
const GAP = 2;
const WEEKS_TO_SHOW = 52;

export default function ActivityHeatmap({ data = [] }) {
  const days = useMemo(() => {
    const today = new Date();
    const days = [];
    for (let i = WEEKS_TO_SHOW * 7 - 1; i >= 0; i--) {
      const d = new Date(today);
      d.setDate(d.getDate() - i);
      const key = d.toISOString().slice(0, 10);
      const entry = data.find((item) => item.date === key);
      days.push({
        date: key,
        count: entry ? (entry.total ?? entry.count ?? (entry.solves || 0) + (entry.submissions || 0)) : 0,
      });
    }
    return days;
  }, [data]);

  const maxCount = Math.max(...days.map((d) => d.count), 1);

  const getColor = (count) => {
    if (count === 0) return "bg-gray-800 dark:bg-gray-800";
    const intensity = count / maxCount;
    if (intensity < 0.25) return "bg-green-900 dark:bg-green-900";
    if (intensity < 0.5) return "bg-green-700 dark:bg-green-700";
    if (intensity < 0.75) return "bg-green-500 dark:bg-green-500";
    return "bg-green-400 dark:bg-green-400";
  };

  // Group into weeks (columns)
  const weeks = [];
  for (let i = 0; i < days.length; i += 7) {
    weeks.push(days.slice(i, i + 7));
  }

  return (
    <div className="overflow-x-auto pb-1">
      <div className="flex gap-[2px]" style={{ minWidth: weeks.length * (CELL_SIZE + GAP) }}>
        {weeks.map((week, wi) => (
          <div key={wi} className="flex flex-col gap-[2px]">
            {week.map((day, di) => (
              <div
                key={day.date}
                className={`rounded-sm ${getColor(day.count)}`}
                style={{
                  width: CELL_SIZE,
                  height: CELL_SIZE,
                }}
                title={`${day.date}: ${day.count} activities`}
              />
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}
