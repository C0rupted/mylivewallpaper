// Clock widget isolated JavaScript
(function() {
  const hhmmEl = document.getElementById('clock-hhmm');
  const secsEl = document.getElementById('clock-secs');
  const dateEl = document.getElementById('clock-date');

  if (!hhmmEl || !dateEl) return;
  
  function update() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const mins = String(now.getMinutes()).padStart(2, '0');
    const secs = String(now.getSeconds()).padStart(2, '0');
    const hhmm = `${hours}:${mins}`;
    const s = `:${secs}`;

    const hhmmEl = document.getElementById('clock-hhmm');
    const secsEl = document.getElementById('clock-secs');
    if (hhmmEl) hhmmEl.textContent = hhmm;
    if (secsEl) secsEl.textContent = s;

    const dateStr = now.toLocaleDateString(undefined, {
      weekday: 'short',
      month: 'short',
      day: 'numeric'
    });
    dateEl.textContent = dateStr;
  }
  
  update();
  setInterval(update, 1000);
})();
