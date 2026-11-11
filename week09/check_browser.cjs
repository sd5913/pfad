/* Real two-page browser proof. Owns a loopback server on 8009; never touches 8765. */
const assert = require('node:assert/strict');
const { spawn } = require('node:child_process');
const fs = require('node:fs/promises');
const path = require('node:path');
const { chromium } = require('playwright');

let server;
async function startServer() {
  server = spawn(process.env.WEEK09_PYTHON || 'python', ['server.py', '--port', '8009'], {
    cwd: __dirname, stdio: ['ignore', 'ignore', 'pipe'],
  });
  let errors = '';
  server.stderr.on('data', data => { errors += data.toString(); });
  for (let i = 0; i < 100; i++) {
    await new Promise(resolve => setTimeout(resolve, 50));
    if (server.exitCode !== null) throw new Error(`Server exited: ${errors}`);
    try {
      const response = await fetch('http://127.0.0.1:8009/state');
      if (response.ok) return;
    } catch {}
  }
  throw new Error(`Server did not become ready: ${errors}`);
}
async function stopServer() {
  if (server && server.exitCode === null) {
    await new Promise((resolve, reject) => {
      const timer = setTimeout(() => { server.kill('SIGKILL'); reject(new Error('Server failed to stop')); }, 5000);
      server.once('exit', () => { clearTimeout(timer); resolve(); });
      server.kill('SIGINT');
    });
  }
}
async function state(page, x) {
  await page.waitForFunction(value => document.querySelector('#snapshot').dataset.x === String(value), x);
}
async function position(page, x) {
  await page.locator('#position').evaluate((input, value) => {
    input.value = value;
    input.dispatchEvent(new Event('input', { bubbles: true }));
  }, String(x));
}

(async () => {
  let browser, context;
  const destination = process.env.WEEK09_SCREENSHOT_DIR;
  try {
    await startServer();
    browser = await chromium.launch();
    context = await browser.newContext({ viewport: { width: 1280, height: 900 } });
    await context.tracing.start({ screenshots: true, snapshots: true });
    const a = await context.newPage(), b = await context.newPage();
    const pageErrors = [];
    a.on('pageerror', error => pageErrors.push(error.message));
    b.on('pageerror', error => pageErrors.push(error.message));
    await Promise.all([a.goto('http://127.0.0.1:8009'), b.goto('http://127.0.0.1:8009')]);
    await Promise.all([state(a, 50), state(b, 50)]);
    await position(a, 25);
    await a.getByRole('button', { name: 'Send WebSocket', exact: true }).click();
    await Promise.all([state(a, 25), state(b, 25)]);
    await a.waitForFunction(() => document.querySelector('#outcome').textContent.includes('Acknowledged'));
    await position(a, 80);
    await a.getByRole('button', { name: 'Send HTTP', exact: true }).click();
    await state(b, 80);
    await a.waitForFunction(() => document.querySelector('#outcome').textContent.includes('Acknowledged'));
    const revision = await b.locator('#snapshot').getAttribute('data-revision');
    await a.getByRole('button', { name: 'Try invalid x = 101', exact: true }).click();
    await a.waitForFunction(() => document.querySelector('#outcome').textContent.includes('Rejected'));
    assert.equal(await b.locator('#snapshot').getAttribute('data-revision'), revision);
    // Delay delivery of actual server results at the client boundary; keep the real transport/state path.
    await a.evaluate(() => {
      const receive = socket.onmessage;
      window.delayedResults = [];
      socket.onmessage = event => {
        const result = JSON.parse(event.data);
        if (result.type === 'ack' || result.type === 'rejected') window.delayedResults.push(event);
        else receive(event);
      };
      window.releaseResult = () => receive(window.delayedResults.shift());
      window.restoreResults = () => { socket.onmessage = receive; };
    });
    await a.getByRole('button', { name: 'Try invalid x = 101', exact: true }).click();
    await a.waitForFunction(() => window.delayedResults.length === 1);
    await a.waitForFunction(() => document.querySelector('#outcome').textContent.includes('Unknown'));
    await position(a, 35);
    await a.getByRole('button', { name: 'Send WebSocket', exact: true }).click();
    await state(b, 35);
    await a.waitForFunction(() => window.delayedResults.length === 2);
    const waitingForB = await a.locator('#outcome').textContent();
    assert.match(waitingForB, /Waiting for acknowledgement/);
    await a.evaluate(() => window.releaseResult());
    assert.equal(await a.locator('#outcome').textContent(), waitingForB);
    await a.waitForFunction(() => document.querySelector('#outcome').textContent.includes('Unknown'));
    await a.evaluate(() => window.releaseResult());
    await a.waitForFunction(() => document.querySelector('#outcome').textContent.includes('Acknowledged late'));
    await a.evaluate(() => window.restoreResults());
    await a.getByRole('button', { name: 'Disconnect', exact: true }).click();
    await a.waitForFunction(() => document.querySelector('#connection').textContent.includes('Disconnected'));
    await a.getByRole('button', { name: 'Connect', exact: true }).click();
    await state(a, 35);
    await position(a, 73);
    await a.getByRole('button', { name: 'Send, ignore replies, disconnect', exact: true }).click();
    await a.waitForFunction(() => document.querySelector('#outcome').textContent.includes('Unknown'));
    await state(b, 73);
    await a.getByRole('button', { name: 'Connect', exact: true }).click();
    await state(a, 73);
    assert.match(await a.locator('#outcome').textContent(), /Unknown/);
    if (destination) {
      await fs.mkdir(destination, { recursive: true });
      await a.screenshot({ path: path.join(destination, 'desktop-unknown-reconnected.png'), fullPage: true });
      await b.setViewportSize({ width: 390, height: 844 });
      await b.screenshot({ path: path.join(destination, 'mobile-shared-scene.png'), fullPage: true });
    }
    await stopServer();
    await b.waitForFunction(() => document.querySelector('#connection').textContent.includes('Disconnected'));
    assert.equal(await b.getByRole('button', { name: 'Send WebSocket', exact: true }).isDisabled(), true);
    await startServer();
    await b.getByRole('button', { name: 'Read HTTP snapshot', exact: true }).click();
    await state(b, 50);
    assert.equal(await b.locator('#snapshot').getAttribute('data-revision'), '0');
    assert.match(await b.locator('#connection').textContent(), /Disconnected.*HTTP snapshot/);
    assert.equal(await b.getByRole('button', { name: 'Send WebSocket', exact: true }).isDisabled(), true);
    if (destination) await b.screenshot({ path: path.join(destination, 'http-only-restart-recovery.png'), fullPage: true });
    await b.getByRole('button', { name: 'Connect', exact: true }).click();
    await b.waitForFunction(() => document.querySelector('#connection').textContent === 'Connected');
    await state(b, 50);
    assert.equal(await b.locator('#snapshot').getAttribute('data-revision'), '0');
    assert.deepEqual(pageErrors, []);
    console.log('PASS: two browser clients, HTTP/WS state, correlated delayed results, late ack, disconnect/reconnect, unknown ack, stopped-server UI and HTTP-only restart recovery');
  } finally {
    if (context) await context.tracing.stop(destination ? { path: path.join(destination, 'trace.zip') } : {});
    if (browser) await browser.close();
    await stopServer();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
