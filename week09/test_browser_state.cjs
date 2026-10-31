/* Actual production script with controlled DOM/network/timer boundaries; no browser/network proof. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { test } = require('node:test');
const vm = require('node:vm');

const script = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf8').match(/<script>([\s\S]*?)<\/script>/)[1];

function controller() {
  const elements = new Map(), timers = new Map(), sockets = [], fetches = [];
  let sequence = 0, timerNumber = 0;
  function element(id) {
    if (!elements.has(id)) elements.set(id, { textContent: '', dataset: {}, style: {}, value: '25' });
    return elements.get(id);
  }
  class Socket {
    static CONNECTING = 0; static OPEN = 1; static CLOSING = 2;
    constructor() { this.readyState = Socket.CONNECTING; this.sent = []; sockets.push(this); }
    send(data) { this.sent.push(JSON.parse(data)); }
    close() { this.readyState = 3; this.onclose(); }
  }
  const context = vm.createContext({
    document: { getElementById: element }, WebSocket: Socket,
    location: { protocol: 'http:', host: '127.0.0.1:8009' },
    crypto: { randomUUID: () => `action-${++sequence}` },
    setTimeout: callback => { timers.set(++timerNumber, callback); return timerNumber; },
    clearTimeout: () => {}, // Retain cancelled callbacks to exercise late callback isolation.
    AbortSignal: { timeout: () => ({}) },
    fetch: (url, options) => new Promise((resolve, reject) => fetches.push({ url, options, resolve, reject })),
  });
  vm.runInContext(script, context, { filename: 'index.html' });
  function open(socket = sockets.at(-1)) { socket.readyState = Socket.OPEN; socket.onopen(); return socket; }
  open();
  return {
    element, sockets, fetches, open,
    click: id => element(id).onclick(),
    receive: (message, socket = sockets.at(-1)) => socket.onmessage({ data: JSON.stringify(message) }),
    timeout: (number = timerNumber) => timers.get(number)(),
    outcome: () => element('outcome').textContent,
    reply: (number, body, status = 200) => fetches[number].resolve({ ok: status < 400, status, json: async () => body }),
  };
}

test('delayed rejected A and uncorrelated replies leave B pending until its own acknowledgement', () => {
  const ui = controller();
  ui.click('invalid');
  const a = ui.sockets[0].sent.at(-1);
  ui.timeout();
  ui.click('send-ws');
  const b = ui.sockets[0].sent.at(-1);
  const waiting = ui.outcome();
  ui.receive({ type: 'rejected', id: a.id, error: 'x is outside the range' });
  assert.equal(ui.outcome(), waiting);
  ui.receive({ type: 'rejected', error: 'unidentifiable malformed message' });
  assert.equal(ui.outcome(), waiting);
  ui.receive({ type: 'ack', id: a.id, revision: 1 });
  assert.equal(ui.outcome(), waiting);
  ui.timeout(1);
  assert.equal(ui.outcome(), waiting);
  ui.receive({ type: 'state', x: 25, revision: 1 });
  ui.receive({ type: 'ack', id: b.id, revision: 1 });
  assert.match(ui.outcome(), new RegExp(`Acknowledged ${b.id}`));
  assert.equal(ui.element('snapshot').textContent, 'x = 25 / revision 1');
});

test('late HTTP failure and completion for A cannot time out or settle B', async () => {
  const ui = controller();
  const first = ui.click('send-http');
  ui.timeout();
  ui.click('send-ws');
  const b = ui.sockets[0].sent.at(-1);
  const waiting = ui.outcome();
  ui.fetches[0].reject(new Error('late aborted request'));
  await first;
  assert.equal(ui.outcome(), waiting);
  ui.receive({ type: 'ack', id: b.id, revision: 1 });
  const second = ui.click('send-http');
  const c = JSON.parse(ui.fetches[1].options.body);
  ui.timeout();
  ui.click('send-ws');
  const nextWaiting = ui.outcome();
  ui.reply(1, { type: 'rejected', id: c.id, error: 'late rejection' }, 422);
  await second;
  assert.equal(ui.outcome(), nextWaiting);
});

test('latest timed-out action can receive its own late acknowledgement', () => {
  const ui = controller();
  ui.click('send-ws');
  const action = ui.sockets[0].sent.at(-1);
  ui.timeout();
  assert.match(ui.outcome(), /Unknown/);
  ui.receive({ type: 'ack', id: action.id, revision: 1 });
  assert.match(ui.outcome(), /Acknowledged late/);
  assert.match(ui.outcome(), new RegExp(action.id));
});

test('HTTP result cannot claim another action ID even when that action is pending', async () => {
  const ui = controller();
  const first = ui.click('send-http');
  ui.timeout();
  ui.click('send-ws');
  const b = ui.sockets[0].sent.at(-1);
  const waiting = ui.outcome();
  ui.reply(0, { type: 'ack', id: b.id, revision: 1 });
  await first;
  assert.equal(ui.outcome(), waiting);
  ui.receive({ type: 'ack', id: b.id, revision: 1 });
  assert.match(ui.outcome(), new RegExp(`Acknowledged ${b.id}`));
});

test('callbacks from an old socket do not change the new connection or its pending action', () => {
  const ui = controller();
  const old = ui.sockets[0];
  ui.click('disconnect');
  ui.click('connect');
  const fresh = ui.open();
  ui.click('send-ws');
  const b = fresh.sent.at(-1);
  const waiting = ui.outcome();
  old.onclose();
  ui.receive({ type: 'rejected', id: b.id, error: 'old connection' }, old);
  assert.equal(ui.outcome(), waiting);
  assert.equal(ui.element('connection').textContent, 'Connected');
  ui.receive({ type: 'ack', id: b.id, revision: 1 });
  assert.match(ui.outcome(), new RegExp(`Acknowledged ${b.id}`));
});

test('manual HTTP snapshot recovers revision zero while WebSocket remains disconnected', async () => {
  const ui = controller();
  ui.receive({ type: 'state', x: 25, revision: 5 });
  ui.click('disconnect');
  const reading = ui.click('read-http');
  ui.reply(0, { type: 'state', x: 50, revision: 0 });
  await reading;
  assert.equal(ui.element('snapshot').textContent, 'x = 50 / revision 0');
  assert.match(ui.element('connection').textContent, /Disconnected.*HTTP snapshot/);
  assert.equal(ui.sockets.length, 1);
  assert.equal(ui.sockets[0].sent.length, 0);
});

test('HTTP response from before a newer live state cannot roll the scene back', async () => {
  const ui = controller();
  ui.receive({ type: 'state', x: 25, revision: 1 });
  const reading = ui.click('read-http');
  ui.receive({ type: 'state', x: 70, revision: 2 });
  ui.reply(0, { type: 'state', x: 25, revision: 1 });
  await reading;
  assert.equal(ui.element('snapshot').textContent, 'x = 70 / revision 2');
});

test('overlapping HTTP reads accept the newest request and ignore an earlier delayed response', async () => {
  const ui = controller();
  ui.receive({ type: 'state', x: 25, revision: 3 });
  ui.click('disconnect');
  const earlier = ui.click('read-http'), later = ui.click('read-http');
  ui.reply(1, { type: 'state', x: 80, revision: 4 });
  await later;
  ui.reply(0, { type: 'state', x: 25, revision: 3 });
  await earlier;
  assert.equal(ui.element('snapshot').textContent, 'x = 80 / revision 4');
});

test('an HTTP snapshot started before reconnect cannot replace the new connection snapshot', async () => {
  const ui = controller();
  ui.receive({ type: 'state', x: 25, revision: 3 });
  ui.click('disconnect');
  const reading = ui.click('read-http');
  ui.click('connect');
  ui.open();
  ui.receive({ type: 'state', x: 50, revision: 0 });
  ui.reply(0, { type: 'state', x: 25, revision: 3 });
  await reading;
  assert.equal(ui.element('snapshot').textContent, 'x = 50 / revision 0');
});
