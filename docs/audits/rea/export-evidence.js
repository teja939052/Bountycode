const fs = require('fs');

// Read UTF-16LE file
const raw = fs.readFileSync('D:/Project-Fremen/docs/audits/rea/frontend-post-cleanup-audit.json');
const text = raw.toString('utf16le');
const lines = text.split('\n').filter(l => l.trim());

// Find the last JSON object (the actual result)
let result = null;
for (let i = lines.length - 1; i >= 0; i--) {
  try {
    const obj = JSON.parse(lines[i]);
    if (obj.evidence_id || obj.predicate_type) {
      result = obj;
      break;
    }
  } catch(e) {}
}

if (!result) {
  console.error('No result object found');
  process.exit(1);
}

// Write as proper UTF-8 JSON
fs.writeFileSync(
  'D:/Project-Fremen/docs/audits/rea/frontend-post-cleanup-evidence.json',
  JSON.stringify(result, null, 2),
  'utf8'
);

console.log('Evidence exported successfully');
console.log('evidence_id:', result.evidence_id);
console.log('predicate_type:', result.predicate_type);
console.log('File size:', fs.statSync('D:/Project-Fremen/docs/audits/rea/frontend-post-cleanup-evidence.json').size, 'bytes');
