function inlineToNodes(text, keyBase) {
  const nodes = [];
  const regex = /(\*\*[^*]+\*\*|`[^`]+`)/g;
  let last = 0;
  let match;
  let i = 0;
  while ((match = regex.exec(text)) !== null) {
    if (match.index > last) nodes.push(text.slice(last, match.index));
    const token = match[0];
    if (token.startsWith("**")) {
      nodes.push(
        <strong key={`${keyBase}-b${i}`} className="font-semibold text-text-primary">
          {token.slice(2, -2)}
        </strong>
      );
    } else {
      nodes.push(
        <code
          key={`${keyBase}-c${i}`}
          className="rounded bg-[#EEF5E7] px-1 py-0.5 font-mono text-[0.85em] text-nature-blossom"
        >
          {token.slice(1, -1)}
        </code>
      );
    }
    last = match.index + token.length;
    i += 1;
  }
  if (last < text.length) nodes.push(text.slice(last));
  return nodes;
}

function parseTableLine(line) {
  return line
    .replace(/^\||\|$/g, "")
    .split("|")
    .map((cell) => cell.trim());
}

export default function Markdown({ children }) {
  if (typeof children !== "string") return null;
  const lines = children.split("\n");
  const blocks = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];

    if (line.startsWith("```")) {
      const lang = line.slice(3).trim();
      const code = [];
      i += 1;
      while (i < lines.length && !lines[i].startsWith("```")) {
        code.push(lines[i]);
        i += 1;
      }
      i += 1;
      blocks.push(
        <pre
          key={`pre${blocks.length}`}
          className="overflow-x-auto rounded-xl border border-nature-bark bg-[#F4FAEF] p-4 font-mono text-[13px] leading-relaxed text-[#2F3E2F]"
        >
          <code>{code.join("\n")}</code>
        </pre>
      );
      continue;
    }

    if (line.startsWith("### ")) {
      blocks.push(
        <h3 key={`h3${blocks.length}`} className="mb-2 mt-5 text-lg font-bold text-text-primary">
          {inlineToNodes(line.slice(4), `h3${blocks.length}`)}
        </h3>
      );
      i += 1;
      continue;
    }

    if (line.startsWith("## ")) {
      blocks.push(
        <h2 key={`h2${blocks.length}`} className="mb-2 mt-6 text-xl font-black text-text-primary">
          {inlineToNodes(line.slice(3), `h2${blocks.length}`)}
        </h2>
      );
      i += 1;
      continue;
    }

    if (line.startsWith("|") && i + 1 < lines.length && /^\|[\s:-]+\|/.test(lines[i + 1])) {
      const header = parseTableLine(line);
      const rows = [];
      i += 2;
      while (i < lines.length && lines[i].startsWith("|")) {
        rows.push(parseTableLine(lines[i]));
        i += 1;
      }
      blocks.push(
        <div key={`t${blocks.length}`} className="my-4 overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b-2 border-nature-bark">
                {header.map((h, hi) => (
                  <th key={hi} className="px-3 py-2 font-bold text-text-primary">
                    {inlineToNodes(h, `th${blocks.length}-${hi}`)}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((row, ri) => (
                <tr key={ri} className="border-b border-[#E5E7EB]">
                  {row.map((cell, ci) => (
                    <td key={ci} className="px-3 py-2 text-text-secondary">
                      {inlineToNodes(cell, `td${blocks.length}-${ri}-${ci}`)}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
      continue;
    }

    if (/^\s*[-*] /.test(line)) {
      const items = [];
      while (i < lines.length && /^\s*[-*] /.test(lines[i])) {
        items.push(lines[i].replace(/^\s*[-*] /, ""));
        i += 1;
      }
      blocks.push(
        <ul key={`ul${blocks.length}`} className="my-3 list-disc space-y-1 pl-5 text-text-secondary">
          {items.map((item, ii) => (
            <li key={ii}>{inlineToNodes(item, `li${blocks.length}-${ii}`)}</li>
          ))}
        </ul>
      );
      continue;
    }

    if (/^\s*\d+\. /.test(line)) {
      const items = [];
      while (i < lines.length && /^\s*\d+\. /.test(lines[i])) {
        items.push(lines[i].replace(/^\s*\d+\. /, ""));
        i += 1;
      }
      blocks.push(
        <ol key={`ol${blocks.length}`} className="my-3 list-decimal space-y-1 pl-5 text-text-secondary">
          {items.map((item, ii) => (
            <li key={ii}>{inlineToNodes(item, `oli${blocks.length}-${ii}`)}</li>
          ))}
        </ol>
      );
      continue;
    }

    if (/^\s*$/.test(line)) {
      i += 1;
      continue;
    }

    if (/^---+$/.test(line.trim())) {
      blocks.push(<hr key={`hr${blocks.length}`} className="my-5 border-[#E5E7EB]" />);
      i += 1;
      continue;
    }

    blocks.push(
      <p key={`p${blocks.length}`} className="my-2 leading-relaxed text-text-secondary">
        {inlineToNodes(line, `p${blocks.length}`)}
      </p>
    );
    i += 1;
  }

  return <div className="text-[15px]">{blocks}</div>;
}
