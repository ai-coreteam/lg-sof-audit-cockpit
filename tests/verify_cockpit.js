const fs = require('fs');
const path = require('path');
const vm = require('vm');
const assert = require('assert');

const ROOT = path.resolve(__dirname, '..');
const appHtml = fs.readFileSync(path.join(ROOT, 'app/index.html'), 'utf8');
const rootHtml = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');

let passed = 0;
let total = 0;

function check(name, fn) {
  total++;
  fn();
  passed++;
  console.log(`  [PASS ${passed}/${total}] ${name}`);
}

console.log('Running LG SOF Audit & Risk Governance Cockpit Verification Suite...');

// 1. Parity between app/index.html and root index.html
check('app/index.html and root index.html are 100% identical', () => {
  assert.strictEqual(appHtml, rootHtml, 'app/index.html and index.html must match');
});

// 2. Inline JS syntax check
const scriptBlocks = [...appHtml.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
check('Inline JavaScript in index.html compiles with 0 syntax errors', () => {
  assert.ok(scriptBlocks.length > 0, 'Must have inline script block');
  new vm.Script(scriptBlocks[0]);
});

// 3. Asset parity check (app/assets vs root assets)
['w40_audit_cockpit.js', 'w41_audit_cockpit.js', 'w42_audit_cockpit.js'].forEach(file => {
  check(`Asset parity for ${file}`, () => {
    const a = fs.readFileSync(path.join(ROOT, 'app/assets', file), 'utf8');
    const b = fs.readFileSync(path.join(ROOT, 'assets', file), 'utf8');
    assert.strictEqual(a, b, `app/assets/${file} and assets/${file} must match`);
  });
});

// 4. Runtime VM execution & Cycle tests
const elements = {};
function getEl(id) {
  if (!elements[id]) {
    elements[id] = {
      id,
      textContent: '',
      innerHTML: '',
      value: 'ALL',
      style: {},
      href: '',
      classList: {
        classes: new Set(),
        add(c) { this.classes.add(c); },
        remove(c) { this.classes.delete(c); },
        contains(c) { return this.classes.has(c); }
      },
      appendChild() {}
    };
  }
  return elements[id];
}
getEl('searchInput').value = '';

const sandbox = {
  window: { addEventListener() {} },
  document: {
    getElementById: getEl,
    querySelectorAll() { return []; },
    createElement() { return { style: {}, setAttribute() {} }; },
    body: { appendChild() {}, removeChild() {} }
  },
  localStorage: {
    store: {},
    getItem(k) { return this.store[k] || null; },
    setItem(k, v) { this.store[k] = v; }
  },
  navigator: { clipboard: { writeText: async () => {} } },
  setInterval: () => 1,
  setTimeout: () => 1,
  console, Date, Math, Number, String, Object, Array, JSON, parseInt, isNaN
};
sandbox.window.window = sandbox.window;

vm.createContext(sandbox);
vm.runInContext(fs.readFileSync(path.join(ROOT, 'app/assets/w40_audit_cockpit.js'), 'utf8'), sandbox);
vm.runInContext(fs.readFileSync(path.join(ROOT, 'app/assets/w41_audit_cockpit.js'), 'utf8'), sandbox);
vm.runInContext(fs.readFileSync(path.join(ROOT, 'app/assets/w42_audit_cockpit.js'), 'utf8'), sandbox);
vm.runInContext(scriptBlocks[0], sandbox);
vm.runInContext('initStoreCache();', sandbox);

check('Default cycle W42 loads 16 Middle region records (16/16 Done, 0 Pending, 4 PC_ERROR, 16 Extra Notes)', () => {
  const res = vm.runInContext(`
    switchCycle('W42');
    ({
      cycle: currentCycleKey,
      total: allRecords.length,
      done: document.getElementById('kpiDoneCount').textContent,
      pending: document.getElementById('kpiPendingCount').textContent,
      pcErr: document.getElementById('kpiPCError').textContent,
      plausible: document.getElementById('pillPlausible').textContent,
      extraNote: document.getElementById('pillExtraNote').textContent
    });
  `, sandbox);
  assert.strictEqual(res.cycle, 'W42');
  assert.strictEqual(res.total, 16);
  assert.strictEqual(res.done, '16 / 16');
  assert.strictEqual(res.pending, '0 ca');
  assert.strictEqual(res.pcErr, '4 ca');
  assert.strictEqual(String(res.plausible), '12');
  assert.strictEqual(String(res.extraNote), '16');
});

check('CAOPHONG without space (EASV10177 in W42 & EASV10176 in W41) classifies as dealer CP (MC)', () => {
  const res = vm.runInContext(`
    switchCycle('W42');
    const r42 = allRecords.find(r => r.store_code === 'EASV10177');
    switchCycle('W41');
    const r41 = allRecords.find(r => r.store_code === 'EASV10176');
    ({ d42: r42.dealer, c42: r42.channel, d41: r41.dealer, c41: r41.channel });
  `, sandbox);
  assert.strictEqual(res.d42, 'CP');
  assert.strictEqual(res.c42, 'MC');
  assert.strictEqual(res.d41, 'CP');
  assert.strictEqual(res.c41, 'MC');
});

check('W41 Hint (w41_hint) is populated for repeat store/case EASV6502 in W42', () => {
  const hint = vm.runInContext(`
    switchCycle('W42');
    allRecords.find(r => r.store_code === 'EASV6502').w41_hint;
  `, sandbox);
  assert.ok(hint && hint.includes('W41'), 'EASV6502 must carry W41 history hint');
});

check('Multi-line RFC-4180 CSV parser preserves multi-line quoted Extra Note cells', () => {
  const rows = vm.runInContext(`
    parseCsvToRows('col1,col2,col3\\nEASV4271,CP,"Line 1\\nLine 2\\nLine 3"\\nEASV8009,DMX,Simple');
  `, sandbox);
  assert.strictEqual(rows.length, 3);
  assert.strictEqual(rows[1][2], 'Line 1\nLine 2\nLine 3');
});

check('Historical cycle W41 preserves all 11/11 resolved records with 0 Suspicious', () => {
  const res = vm.runInContext(`
    switchCycle('W41');
    ({
      total: allRecords.length,
      done: document.getElementById('kpiDoneCount').textContent,
      susp: document.getElementById('kpiSuspicious').textContent
    });
  `, sandbox);
  assert.strictEqual(res.total, 11);
  assert.strictEqual(res.done, '11 / 11');
  assert.strictEqual(res.susp, '0 ca');
});

check('National Baseline cycle W40 preserves all 632 records (335 Done)', () => {
  const res = vm.runInContext(`
    switchCycle('W40');
    ({
      total: allRecords.length,
      done: document.getElementById('kpiDoneCount').textContent
    });
  `, sandbox);
  assert.strictEqual(res.total, 632);
  assert.strictEqual(res.done, '335 / 632');
});

console.log(`\nALL ${passed}/${total} VERIFICATION TESTS PASSED.`);
