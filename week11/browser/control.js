const RESET_AFTER_MS = 3000;

function mapOpacity(raw) {
  if (raw.trim() === '') return null;
  const number = Number(raw);
  if (!Number.isFinite(number)) return null;
  return Math.round(Math.max(0, Math.min(1, number)) * 100);
}

if (typeof module !== 'undefined') module.exports = { mapOpacity, RESET_AFTER_MS };

if (typeof document !== 'undefined') {
  const form = document.querySelector('#control');
  const input = document.querySelector('#value');
  const stop = document.querySelector('#stop');
  const result = document.querySelector('#result');
  const status = document.querySelector('#status');
  const canvas = document.querySelector('#art');
  const ctx = canvas.getContext('2d');
  let resetTimer;

  function draw(opacity) {
    ctx.fillStyle = '#142c37';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.strokeStyle = '#42666b';
    ctx.lineWidth = 2;
    for (let x = 40; x < canvas.width; x += 40) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, canvas.height);
      ctx.stroke();
    }
    ctx.globalAlpha = opacity / 100;
    ctx.fillStyle = '#ffad70';
    ctx.beginPath();
    ctx.arc(400, 200, 140, 0, Math.PI * 2);
    ctx.fill();
    ctx.globalAlpha = 1;
  }

  function show(opacity, message) {
    draw(opacity);
    result.textContent = `Opacity: ${opacity}%`;
    status.textContent = message;
  }

  function reset(message) {
    clearTimeout(resetTimer);
    show(0, message);
  }

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    clearTimeout(resetTimer);
    const opacity = mapOpacity(input.value);
    if (opacity === null) {
      reset(input.value.trim() ? 'Invalid input: reset to 0%.' : 'Missing input: reset to 0%.');
      return;
    }
    show(opacity, `Received ${input.value}: showing ${opacity}% opacity.`);
    resetTimer = setTimeout(() => reset('No new value for 3 seconds: reset to 0%.'), RESET_AFTER_MS);
  });

  input.addEventListener('input', () => {
    if (mapOpacity(input.value) === null) reset(input.value.trim() ? 'Invalid input: reset to 0%.' : 'Missing input: reset to 0%.');
  });
  stop.addEventListener('click', () => reset('Stopped: reset to 0%.'));
  reset('Stopped: safe blank state.');
}
