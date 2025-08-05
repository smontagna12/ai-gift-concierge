// main.js – client‑side logic for AI‑Gift Concierge

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('giftForm');
  const resultsContainer = document.getElementById('results');

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    // Collect form data
    const occasion = document.getElementById('occasion').value.trim();
    const budget = document.getElementById('budget').value.trim();
    const interests = document.getElementById('interests').value.trim();
    if (!occasion || !budget || !interests) {
      return;
    }
    // Clear previous results
    resultsContainer.innerHTML = '';
    // Add loading indicator
    const loading = document.createElement('p');
    loading.textContent = 'Geschenke werden geladen…';
    resultsContainer.appendChild(loading);

    try {
      const response = await fetch('/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ occasion, budget, interests })
      });
      const data = await response.json();
      displaySuggestions(data.suggestions || []);
    } catch (error) {
      console.error('Error generating suggestions', error);
      resultsContainer.innerHTML = '<p>Beim Erstellen der Vorschläge ist ein Fehler aufgetreten.</p>';
    }
  });

  function displaySuggestions(suggestions) {
    resultsContainer.innerHTML = '';
    if (!Array.isArray(suggestions) || suggestions.length === 0) {
      resultsContainer.innerHTML = '<p>Keine Vorschläge gefunden.</p>';
      return;
    }
    suggestions.forEach((item) => {
      const card = document.createElement('div');
      card.className = 'result-item';
      const title = document.createElement('h3');
      title.textContent = item.name;
      const desc = document.createElement('p');
      desc.textContent = item.description;
      const link = document.createElement('a');
      // Provide a basic search URL for the search term; this can be replaced
      // with affiliate links or a custom search provider.
      const query = encodeURIComponent(item.search_term);
      link.href = `https://www.amazon.de/s?k=${query}`;
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      link.textContent = 'Jetzt suchen';
      card.appendChild(title);
      card.appendChild(desc);
      card.appendChild(link);
      resultsContainer.appendChild(card);
    });
  }
});