function createTableRows(data) {
  const tbody = document.querySelector('#statsTable tbody');
  const maxValues = getMaxValues(data.players);

  data.players.forEach(player => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td class="player">${player.name}</td>
      <td>${player.stats.avg_CSPM.toFixed(2)}<div class="bar" style="width: ${(player.stats.avg_CSPM / maxValues.CSPM) * 100}%"></div></td>
      <td>${player.stats.avg_GDPM.toFixed(2)}<div class="bar" style="width: ${(player.stats.avg_GDPM / maxValues.GDPM) * 100}%"></div></td>
      <td>${player.stats.avg_DPM.toFixed(2)}<div class="bar" style="width: ${(player.stats.avg_DPM / maxValues.DPM) * 100}%"></div></td>
      <td>${player.stats.avg_KDA.toFixed(2)}<div class="bar" style="width: ${(player.stats.avg_KDA / maxValues.KDA) * 100}%"></div></td>
      <td>${player.stats["avg_KP%"].toFixed(2)}%<div class="bar" style="width: ${player.stats["avg_KP%"]}%"></div></td>
      <td>${player.stats.avg_visionScore.toFixed(2)}<div class="bar" style="width: ${(player.stats.avg_visionScore / maxValues.visionScore) * 100}%"></div></td>
    `;
    tbody.appendChild(row);

    row.querySelectorAll('.bar').forEach(bar => {
      const width = parseFloat(bar.style.width);
      const maxWidth = 100;
      const hue = (width / maxWidth) * 120;
      bar.style.backgroundColor = `hsl(${hue}, 100%, 50%)`;
    });
  });
}

function getMaxValues(players) {
  const maxValues = {
    CSPM: 0,
    GDPM: 0,
    DPM: 0,
    KDA: 0,
    visionScore: 0
  };

  players.forEach(player => {
    maxValues.CSPM = Math.max(maxValues.CSPM, player.stats.avg_CSPM);
    maxValues.GDPM = Math.max(maxValues.GDPM, player.stats.avg_GDPM);
    maxValues.DPM = Math.max(maxValues.DPM, player.stats.avg_DPM);
    maxValues.KDA = Math.max(maxValues.KDA, player.stats.avg_KDA);
    maxValues.visionScore = Math.max(maxValues.visionScore, player.stats.avg_visionScore);
  });

  return maxValues;
}

fetch('/static/summary.json')
  .then(response => response.json())
  .then(data => {
    createTableRows(data);
  })
  .catch(error => {
    console.error('Error loading data:', error);
  });
