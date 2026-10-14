// @ts-nocheck
import { motion } from "framer-motion";

type PhoneBookProps = {
  entries: Array<{ name: string; value: string }>;
  lookupName?: string;
};

export default function PhoneBook({ entries, lookupName }: PhoneBookProps) {
  const found = entries.find((e) => e.name === lookupName);
  return (
    <div className="flex flex-col items-center gap-3">
      <div className="w-64 bg-white border rounded-xl shadow-sm divide-y">
        {entries.map((entry) => (
          <div
            key={entry.name}
            className={`flex items-center justify-between px-4 py-2 text-sm ${
              entry.name === lookupName ? "bg-brand-50" : ""
            }`}
          >
            <span className="font-medium text-gray-700">{entry.name}</span>
            <span className="text-gray-500 font-mono">{entry.value}</span>
          </div>
        ))}
      </div>
      {found && (
        <motion.p
          className="text-sm text-gray-700"
          initial={{ opacity: 0, y: 5 }}
          animate={{ opacity: 1, y: 0 }}
        >
          Found: <strong>{found.name}</strong> → <span className="font-mono">{found.value}</span>
        </motion.p>
      )}
      <p className="text-xs text-gray-500">Look up by name, return the value</p>
    </div>
  );
}
