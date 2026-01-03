// Clock widget isolated JavaScript
(function() {
  const timeEl = document.getElementById('clock-time');
  const dateEl = document.getElementById('clock-date');
  
  if (!timeEl || !dateEl) return;
  
  function update() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const mins = String(now.getMinutes()).padStart(2, '0');
    const secs = String(now.getSeconds()).padStart(2, '0');
    timeEl.textContent = `${hours}:${mins}:${secs}`;
    
    const dateStr = now.toLocaleDateString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric'
    });
    dateEl.textContent = dateStr;
  }
  
  update();
  setInterval(update, 1000);
})();
