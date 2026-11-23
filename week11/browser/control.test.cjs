const assert = require('node:assert/strict');
const { test } = require('node:test');
const { mapOpacity, RESET_AFTER_MS } = require('./control.js');

test('maps one finite number to a clamped percentage', () => {
  for (const [raw, expected] of [['0', 0], ['0.25', 25], ['0.50', 50], ['0.75', 75], ['1', 100], ['3', 100], ['-2', 0]]) {
    assert.equal(mapOpacity(raw), expected);
  }
});

test('missing or invalid input never produces an opacity', () => {
  for (const raw of ['', '   ', 'oops', 'Infinity', 'NaN']) assert.equal(mapOpacity(raw), null);
  assert.equal(RESET_AFTER_MS, 3000);
});
