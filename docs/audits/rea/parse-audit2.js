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

function findInObject(obj, path, results, patterns) {
  if (obj === null || obj === undefined) return;
  if (typeof obj === 'string') {
    for (const pat of patterns) {
      if (obj.includes(pat)) {
        results.push({ pat, value: obj, path });
      }
    }
    return;
  }
  if (Array.isArray(obj)) {
    obj.forEach((item, i) => findInObject(item, path + '[' + i + ']', results, patterns));
    return;
  }
  if (typeof obj === 'object') {
    for (const [key, val] of Object.entries(obj)) {
      findInObject(val, path + '.' + key, results, patterns);
    }
  }
}

const allObjs = [...nodes, ...edges, ...semNodes, ...semRelations];

// 1. Dashboard references
console.log('=== 1. /dashboard references ===');
let dashboard = [];
for (const o of allObjs) { findInObject(o, 'obj', dashboard, ['/dashboard']); }
console.log('Count:', dashboard.length);
dashboard.slice(0, 10).forEach(r => console.log('  ', r.value.substring(0, 150)));

// 2. SearchModal
console.log('\n=== 2. SearchModal references ===');
let searchModal = [];
for (const o of allObjs) { findInObject(o, 'obj', searchModal, ['SearchModal']); }
console.log('Count:', searchModal.length);
searchModal.slice(0, 10).forEach(r => console.log('  ', r.value.substring(0, 150)));

// 3. uiverse
console.log('\n=== 3. uiverse references ===');
let uiverse = [];
for (const o of allObjs) { findInObject(o, 'obj', uiverse, ['uiverse']); }
console.log('Count:', uiverse.length);
uiverse.slice(0, 10).forEach(r => console.log('  ', r.value.substring(0, 150)));

// 4. /landing redirect target
console.log('\n=== 4. /landing route context ===');
let landing = [];
for (const o of allObjs) { findInObject(o, 'obj', landing, ['/landing']); }
console.log('Count:', landing.length);
landing.slice(0, 10).forEach(r => console.log('  ', r.value.substring(0, 200)));

// 5. Mission routes
console.log('\n=== 5. Mission route references ===');
let missions = [];
for (const o of allObjs) { findInObject(o, 'obj', missions, ['/mission/for-loops', '/mission/sliding-window', '/mission/sql-joins', 'for-loops', 'sliding-window', 'sql-joins']); }
console.log('Count:', missions.length);
missions.slice(0, 10).forEach(r => console.log('  ', r.value.substring(0, 150)));

// 6. API fetch calls with endpoints
console.log('\n=== 6. API endpoint patterns ===');
let apiEndpoints = [];
for (const o of allObjs) { findInObject(o, 'obj', apiEndpoints, ['/api/v1/', '/api/']); }
console.log('Count:', apiEndpoints.length);
const seen = new Set();
apiEndpoints.slice(0, 30).forEach(r => {
  const key = r.value.substring(0, 100);
  if (!seen.has(key)) {
    seen.add(key);
    console.log('  ', r.value.substring(0, 150));
  }
});

// 7. External domains (non-coddy.tech, non-localhost)
console.log('\n=== 7. External URLs ===');
let external = [];
for (const o of allObjs) { findInObject(o, 'obj', external, ['http://', 'https://']); }
const extSeen = new Set();
external.slice(0, 30).forEach(r => {
  const key = r.value.substring(0, 100);
  if (!extSeen.has(key)) {
    extSeen.add(key);
    console.log('  ', r.value.substring(0, 150));
  }
});

// 8. Diagnostic calls
console.log('\n=== 8. Diagnostic references ===');
let diag = [];
for (const o of allObjs) { findInObject(o, 'obj', diag, ['diagnostic', 'Diagnostic']); }
console.log('Count:', diag.length);
diag.slice(0, 10).forEach(r => console.log('  ', r.value.substring(0, 150)));

// 9. Compiler calls
console.log('\n=== 9. Compiler references ===');
let comp = [];
for (const o of allObjs) { findInObject(o, 'obj', comp, ['compiler', 'Compiler', 'piston', 'execute']); }
console.log('Count:', comp.length);
comp.slice(0, 10).forEach(r => console.log('  ', r.value.substring(0, 150)));
