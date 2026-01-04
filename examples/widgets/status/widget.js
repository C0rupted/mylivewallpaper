// Status widget - shows system uptime, temp, battery (demo values)
(function() {
  const uptimeEl = document.getElementById('status-uptime');
  const tempEl = document.getElementById('status-temp');
  const batteryEl = document.getElementById('status-battery');
  
  if (!uptimeEl || !tempEl || !batteryEl) return;
  
  function update() {
    // Demo uptime (hours since page loaded)
    const uptime = Math.floor(Math.random() * 240) + 'h';
    uptimeEl.textContent = uptime;
    
    // Demo temp
    const temp = Math.floor(Math.random() * 20 + 35);
    tempEl.textContent = temp + '°C';
    
    // Demo battery
    const battery = Math.floor(Math.random() * 30 + 70);
    batteryEl.textContent = battery + '%';
  }
  
  update();
  setInterval(update, 5000);
})();
