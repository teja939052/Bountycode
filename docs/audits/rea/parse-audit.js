const fs = require('fs');
const raw = fs.readFileSync('D:/Project-Fremen/docs/audits/rea/frontend-post-cleanup-audit.json');
const text = raw.toString('utf16le');
const lines = text.split('\n').filter(l => l.trim());

let result = null;
for (const line of lines) {
  try {
    const obj = JSON.parse(line);
    if (obj.evidence_id || obj.predicate_type) {
      result = obj;
    }
  } catch(e) {}
}

const nr = result.normalized_result;
const nodes = nr.graph.nodes || [];
const edges = nr.graph.edges || [];
const semNodes = nr.semantic_graph.nodes || [];
const semRelations = nr.semantic_graph.relations || [];

console.log('Graph nodes:', nodes.length);
console.log('Graph edges:', edges.length);
console.log('Semantic nodes:', semNodes.length);
console.log('Semantic relations:', semRelations.length);

const routePatterns = [
  '/dashboard', '/journey', '/learning', '/learn', '/arena', '/start',
  '/landing', '/placement', '/curriculum', '/question-bank', '/mock-oa',
  '/profile', '/mission/for-loops', '/mission/sliding-window', '/mission/sql-joins',
  'SearchModal', 'uiverse', 'fetch(', 'axios', 'XMLHttpRequest'
];

function findInObject(obj, path, results) {
  if (obj === null || obj === undefined) return;
  if (typeof obj === 'string') {
    for (const pat of routePatterns) {
      if (obj.includes(pat)) {
        results.push({ pat, value: obj, path });
      }
    }
    return;
  }
  if (Array.isArray(obj)) {
    obj.forEach((item, i) => findInObject(item, path + '[' + i + ']', results));
    return;
  }
  if (typeof obj === 'object') {
    for (const [key, val] of Object.entries(obj)) {
      findInObject(val, path + '.' + key, results);
    }
  }
}

let allResults = [];
for (const node of nodes) { findInObject(node, 'node', allResults); }
for (const edge of edges) { findInObject(edge, 'edge', allResults); }
for (const sn of semNodes) { findInObject(sn, 'semNode', allResults); }
for (const sr of semRelations) { findInObject(sr, 'semRel', allResults); }

const seen = new Set();
const unique = [];
for (const r of allResults) {
  const key = r.pat + '|' + r.value;
  if (!seen.has(key)) {
    seen.add(key);
    unique.push(r);
  }
}

console.log('\n=== ROUTE REFERENCES FOUND ===');
const byPat = {};
for (const r of unique) {
  if (!byPat[r.pat]) byPat[r.pat] = [];
  byPat[r.pat].push(r.value);
}
for (const [pat, values] of Object.entries(byPat)) {
  console.log(pat + ': ' + values.length + ' occurrences');
  values.slice(0, 5).forEach(function(v) { console.log('  ' + v.substring(0, 120)); });
}

// Check API endpoints
console.log('\n=== API ENDPOINT REFERENCES ===');
const apiResults = [];
for (const node of nodes) {
  findInObject(node, 'node', apiResults.filter(function() { return false; })); // dummy
}
// Re-collect just API-related
const apiPatterns = ['/api/', 'fetch(', 'XMLHttpRequest', 'axios'];
let apiResults2 = [];
for (const node of nodes) { findInObject(node, 'node', apiResults2); }
for (const edge of edges) { findInObject(edge, 'edge', apiResults2); }
const apiSeen = new Set();
const apiUnique = [];
for (const r of apiResults2) {
  if (r.pat === '/api/' || r.pat === 'fetch(' || r.pat === 'XMLHttpRequest' || r.pat === 'axios') {
    const key = r.pat + '|' + r.value;
    if (!apiSeen.has(key)) {
      apiSeen.add(key);
      apiUnique.push(r);
    }
  }
}
const byApiPat = {};
for (const r of apiUnique) {
  if (!byApiPat[r.pat]) byApiPat[r.pat] = [];
  byApiPat[r.pat].push(r.value);
}
for (const [pat, values] of Object.entries(byApiPat)) {
  console.log(pat + ': ' + values.length + ' occurrences');
  values.slice(0, 10).forEach(function(v) { console.log('  ' + v.substring(0, 150)); });
}
