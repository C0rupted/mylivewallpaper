// Quote widget - displays rotating quotes
(function() {
  const quotes = [
    { text: "Every moment is a fresh beginning.", author: "Emerson" },
    { text: "The only way to do great work is to love what you do.", author: "Steve Jobs" },
    { text: "Design is not just what it looks like and feels like. Design is how it works.", author: "Steve Jobs" },
    { text: "Simplicity is the ultimate sophistication.", author: "da Vinci" },
    { text: "Life is 10% what happens and 90% how you react to it.", author: "Charles R. Swindoll" }
  ];
  
  const textEl = document.getElementById('quote-text');
  const authorEl = document.getElementById('quote-author');
  
  if (!textEl || !authorEl) return;
  
  let idx = 0;
  
  function update() {
    const quote = quotes[idx % quotes.length];
    textEl.textContent = quote.text;
    authorEl.textContent = '— ' + quote.author;
    idx++;
  }
  
  update();
  setInterval(update, 8000);
})();
