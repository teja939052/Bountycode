const fs = require('fs');

function loadAudit(path) {
  const raw = fs.readFileSync(path);
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
  return result;
}

const pre = loadAudit('D:/Project-Fremen/docs/audits/rea/frontend-bundle-audit.json');
const post = loadAudit('D:/Project-Fremen/docs/audits/rea/frontend-post-cleanup-audit.json');

function extractStrings(obj, patterns, results = []) {
  if (obj === null || obj === undefined) return results;
  if (typeof obj === 'string') {
    for (const pat of patterns) {
      if (obj.includes(pat)) {
        results.push({ pat, value: obj });
      }
    }
    return results;
  }
  if (Array.isArray(obj)) {
    obj.forEach(item => extractStrings(item, patterns, results));
    return results;
  }
  if (typeof obj === 'object') {
    for (const val of Object.values(obj)) {
      extractStrings(val, patterns, results);
    }
  }
  return results;
}

const patterns = [
  '/dashboard', '/journey', '/learning', '/learn', '/arena', '/start',
  '/landing', '/placement', '/curriculum', '/question-bank', '/mock-oa',
  '/profile', '/mission/for-loops', '/mission/sliding-window', '/mission/sql-joins',
  'SearchModal', 'uiverse', '/api/v1/', 'https://', 'http://',
  'fetch(', 'XMLHttpRequest'
];

console.log('=== COMPARISON: PRE-CLEANUP vs POST-CLEANUP ===\n');

const preNodes = pre.normalized_result.graph.nodes || [];
const preEdges = pre.normalized_result.graph.edges || [];
const preSemNodes = pre.normalized_result.semantic_graph.nodes || [];
const preSemRelations = pre.normalized_result.semantic_graph.relations || [];

const postNodes = post.normalized_result.graph.nodes || [];
const postEdges = post.normalized_result.graph.edges || [];
const postSemNodes = post.normalized_result.semantic_graph.nodes || [];
const postSemRelations = post.normalized_result.semantic_graph.relations || [];

console.log('Graph nodes:  pre=' + preNodes.length + '  post=' + postNodes.length);
console.log('Graph edges:  pre=' + preEdges.length + '  post=' + postEdges.length);
console.log('Semantic nodes: pre=' + preSemNodes.length + '  post=' + postSemNodes.length);
console.log('Semantic relations: pre=' + preSemRelations.length + '  post=' + postSemRelations.length);

const preAll = [...preNodes, ...preEdges, ...preSemNodes, ...preSemRelations];
const postAll = [...postNodes, ...postEdges, ...postSemNodes, ...postSemRelations];

const preFound = {};
const postFound = {};

for (const pat of patterns) {
  const preResults = extractStrings(preAll, [pat]);
  const postResults = extractStrings(postAll, [pat]);
  const preVals = [...new Set(preResults.map(r => r.value))];
  const postVals = [...new Set(postResults.map(r => r.value))];
  preFound[pat] = preVals;
  postFound[pat] = postVals;
}

console.log('\n=== ROUTE & DEPENDENCY DELTA ===\n');
for (const pat of patterns) {
  const preVals = preFound[pat] || [];
  const postVals = postFound[pat] || [];
  const removed = preVals.filter(v => !postVals.includes(v));
  const added = postVals.filter(v => !preVals.includes(v));
  
  console.log('Pattern: ' + pat);
  console.log('  PRE: ' + preVals.length + ' unique values');
  console.log('  POST: ' + postVals.length + ' unique values');
  if (removed.length > 0) {
    console.log('  REMOVED (' + removed.length + '):');
    removed.slice(0, 10).forEach(v => console.log('    - ' + v.substring(0, 100)));
  }
  if (added.length > 0) {
    console.log('  ADDED (' + added.length + '):');
    added.slice(0, 10).forEach(v => console.log('    + ' + v.substring(0, 100)));
  }
  if (removed.length === 0 && added.length === 0) {
    console.log('  UNCHANGED');
  }
  console.log('');
}

// Summary for acceptance checks
console.log('=== ACCEPTANCE CHECK SUMMARY ===\n');
console.log('1. /dashboard as student recovery route:');
console.log('   PRE: ' + (preFound['/dashboard'] || []).length + ' references');
console.log('   POST: ' + (postFound['/dashboard'] || []).length + ' references');
console.log('   STATUS: ' + ((postFound['/dashboard'] || []).length === 0 ? 'PASS - Removed' : 'FAIL - Still present') + '\n');

console.log('2. SearchModal entries:');
console.log('   PRE: ' + (preFound['SearchModal'] || []).length + ' references');
console.log('   POST: ' + (postFound['SearchModal'] || []).length + ' references');
console.log('   STATUS: ' + ((postFound['SearchModal'] || []).length === 0 ? 'PASS - Removed' : 'FAIL - Still present') + '\n');

console.log('3. Ghost links (/journey, /learning, /learn, /arena, /start):');
for (const g of ['/journey', '/learning', '/learn', '/arena', '/start']) {
  const preCount = (preFound[g] || []).length;
  const postCount = (postFound[g] || []).length;
  console.log('   ' + g + ': PRE=' + preCount + ' POST=' + postCount + ' ' + (postCount === 0 ? 'PASS' : 'REVIEW'));
}
console.log('');

console.log('4. /landing redirect:');
console.log('   PRE: ' + (preFound['/landing'] || []).length + ' references');
console.log('   POST: ' + (postFound['/landing'] || []).length + ' references');
console.log('   STATUS: ' + (postFound['/landing'] && postFound['/landing'].length > 0 ? 'Still present - verify redirect to /' : 'Removed') + '\n');

console.log('5. Five-tab journey:');
for (const t of ['/placement', '/curriculum', '/question-bank', '/mock-oa', '/profile']) {
  const postCount = (postFound[t] || []).length;
  console.log('   ' + t + ': POST=' + postCount + ' ' + (postCount > 0 ? 'PRESENT' : 'MISSING'));
}
console.log('');

console.log('6. Mission routes:');
for (const m of ['/mission/for-loops', '/mission/sliding-window', '/mission/sql-joins']) {
  const postCount = (postFound[m] || []).length;
  console.log('   ' + m + ': POST=' + postCount + ' (check /mission/:slug pattern)');
}
console.log('');

console.log('7. External endpoints:');
const preExt = (preFound['https://'] || []).concat(preFound['http://'] || []);
const postExt = (postFound['https://'] || []).concat(postFound['http://'] || []);
const preExtUnique = [...new Set(preExt)];
const postExtUnique = [...new Set(postExt)];
console.log('   PRE external URLs: ' + preExtUnique.length);
preExtUnique.slice(0, 10).forEach(v => console.log('     ' + v.substring(0, 100)));
console.log('   POST external URLs: ' + postExtUnique.length);
postExtUnique.slice(0, 10).forEach(v => console.log('     ' + v.substring(0, 100)));
console.log('');

console.log('8. API endpoints:');
const preApi = [...new Set((preFound['/api/v1/'] || []))];
const postApi = [...new Set((postFound['/api/v1/'] || []))];
console.log('   PRE: ' + preApi.length + ' unique');
preApi.slice(0, 10).forEach(v => console.log('     ' + v.substring(0, 100)));
console.log('   POST: ' + postApi.length + ' unique');
postApi.slice(0, 10).forEach(v => console.log('     ' + v.substring(0, 100)));
