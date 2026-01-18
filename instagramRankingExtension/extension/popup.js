// Instagram Ranking Extension - Popup Script
// Responsável pela interface e controle da extensão

console.log('[Instagram Ranking] Popup loaded');

// Estado
let isCollecting = false;
let logs = [];
const MAX_LOGS = 10;
let currentFilter = 'all'; // 'all', 'photo', 'video'
let allPosts = []; // Cache de todos os posts

// Elementos do DOM
const toggleButton = document.getElementById('toggle-collection');
const clearButton = document.getElementById('clear-data');
const toggleLogsButton = document.getElementById('toggle-logs');
const statusIcon = document.getElementById('status-icon');
const statusText = document.getElementById('status-text');
const postsCount = document.getElementById('posts-count');
const lastPostTime = document.getElementById('last-post-time');
const rankingContainer = document.getElementById('ranking-container');
const logsSection = document.getElementById('logs-section');
const logsContainer = document.getElementById('logs-container');

// Botões de filtro
const filterAllBtn = document.getElementById('filter-all');
const filterPhotosBtn = document.getElementById('filter-photos');
const filterVideosBtn = document.getElementById('filter-videos');

// Inicializar
init();

function init() {
  // Carregar dados salvos
  loadPosts();

  // Event listeners
  toggleButton.addEventListener('click', toggleCollection);
  clearButton.addEventListener('click', clearData);
  toggleLogsButton.addEventListener('click', toggleLogsPanel);

  // Filtros
  filterAllBtn.addEventListener('click', () => setFilter('all'));
  filterPhotosBtn.addEventListener('click', () => setFilter('photo'));
  filterVideosBtn.addEventListener('click', () => setFilter('video'));

  // Listener para mudanças no storage
  chrome.storage.onChanged.addListener((changes) => {
    if (changes.posts) {
      allPosts = changes.posts.newValue || [];
      applyFilter();
      updateStats(allPosts);
    }
  });

  // Verificar status da coleta
  checkCollectionStatus();

  // Adicionar log inicial
  addLog('info', 'Popup aberto');
}

// Carregar posts do storage
function loadPosts() {
  chrome.storage.local.get(['posts'], (result) => {
    allPosts = result.posts || [];
    applyFilter();
    updateStats(allPosts);
  });
}

// Definir filtro ativo
function setFilter(filter) {
  currentFilter = filter;

  // Atualizar UI dos botões
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.classList.remove('active');
  });

  if (filter === 'all') {
    filterAllBtn.classList.add('active');
  } else if (filter === 'photo') {
    filterPhotosBtn.classList.add('active');
  } else if (filter === 'video') {
    filterVideosBtn.classList.add('active');
  }

  // Aplicar filtro
  applyFilter();

  // Log
  addLog('info', `Filtro alterado para: ${filter}`);
}

// Aplicar filtro atual
function applyFilter() {
  let filteredPosts = allPosts;

  if (currentFilter === 'photo') {
    filteredPosts = allPosts.filter(post => post.type === 'photo');
  } else if (currentFilter === 'video') {
    filteredPosts = allPosts.filter(post => post.type === 'video');
  }

  renderRanking(filteredPosts);
}

// Toggle coleta
function toggleCollection() {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const currentTab = tabs[0];

    // Verificar se está no Instagram
    if (!currentTab.url.includes('instagram.com')) {
      alert('Por favor, abra uma página do Instagram primeiro');
      addLog('warning', 'Tentativa de coletar fora do Instagram');
      return;
    }

    const action = isCollecting ? 'STOP_COLLECTING' : 'START_COLLECTING';

    chrome.tabs.sendMessage(currentTab.id, { action: action }, (response) => {
      if (chrome.runtime.lastError) {
        console.error('[Instagram Ranking] Erro ao enviar mensagem:', chrome.runtime.lastError);
        addLog('error', 'Erro de comunicação com a página');
        return;
      }

      isCollecting = !isCollecting;
      updateCollectionUI();

      const logMsg = isCollecting ? 'Coleta iniciada' : 'Coleta pausada';
      addLog('info', logMsg);
    });
  });
}

// Verificar status atual da coleta
function checkCollectionStatus() {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const currentTab = tabs[0];

    if (!currentTab.url.includes('instagram.com')) {
      return;
    }

    chrome.tabs.sendMessage(currentTab.id, { action: 'GET_STATUS' }, (response) => {
      if (response && response.isCollecting !== undefined) {
        isCollecting = response.isCollecting;
        updateCollectionUI();
      }
    });
  });
}

// Atualizar UI do botão de coleta
function updateCollectionUI() {
  if (isCollecting) {
    toggleButton.textContent = '⏸ Parar Coleta';
    toggleButton.classList.remove('btn-primary');
    toggleButton.classList.add('btn-success');
    statusIcon.textContent = '✅';
    statusText.textContent = 'Coletando automaticamente...';
  } else {
    toggleButton.textContent = '🚀 Iniciar Coleta Automática';
    toggleButton.classList.remove('btn-success');
    toggleButton.classList.add('btn-primary');
    statusIcon.textContent = '⏸';
    statusText.textContent = 'Pausado';
  }
}

// Limpar dados
function clearData() {
  if (!confirm('Tem certeza que deseja limpar todos os dados coletados?')) {
    return;
  }

  chrome.storage.local.set({ posts: [] }, () => {
    allPosts = [];
    renderRanking([]);
    updateStats([]);
    addLog('info', 'Dados limpos');
  });
}

// Renderizar ranking
function renderRanking(posts) {
  if (!posts || posts.length === 0) {
    rankingContainer.innerHTML = '<p class="ranking-empty">Visite um perfil do Instagram e inicie a coleta</p>';
    return;
  }

  // Ordenar por curtidas (decrescente)
  const sortedPosts = [...posts].sort((a, b) => b.likes - a.likes);

  // Gerar HTML
  const html = sortedPosts.map((post, index) => {
    const medal = index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : '';
    const position = index + 1;
    const typeIcon = post.type === 'video' ? '🎥' : '📷';
    const typeBadge = `<span class="type-badge type-${post.type}">${typeIcon} ${post.type === 'video' ? 'Vídeo' : 'Foto'}</span>`;

    return `
      <div class="ranking-item">
        <div class="ranking-position">
          ${medal} #${position}
        </div>
        <div class="ranking-info">
          <div class="ranking-likes">💙 ${formatNumber(post.likes)} curtidas ${typeBadge}</div>
          ${post.thumbnail ? `<img src="${post.thumbnail}" alt="Post" class="ranking-thumbnail">` : ''}
        </div>
        <div class="ranking-actions">
          <a href="${post.url}" target="_blank" class="btn btn-link">Ver Post</a>
        </div>
      </div>
    `;
  }).join('');

  rankingContainer.innerHTML = html;
}

// Atualizar estatísticas
function updateStats(posts) {
  postsCount.textContent = posts.length;

  if (posts.length > 0) {
    // Encontrar post mais recente
    const latestPost = posts.reduce((latest, current) => {
      return current.timestamp > latest.timestamp ? current : latest;
    });

    const timeAgo = getTimeAgo(latestPost.timestamp);
    lastPostTime.textContent = timeAgo;
  } else {
    lastPostTime.textContent = '-';
  }
}

// Toggle painel de logs
function toggleLogsPanel() {
  const isVisible = logsSection.style.display !== 'none';

  if (isVisible) {
    logsSection.style.display = 'none';
    toggleLogsButton.textContent = '📋 Ver Logs';
  } else {
    logsSection.style.display = 'block';
    toggleLogsButton.textContent = '📋 Ocultar Logs';
    renderLogs();
  }
}

// Adicionar log
function addLog(type, message) {
  const timestamp = new Date().toLocaleTimeString('pt-BR');
  const icon = type === 'info' ? '✅' : type === 'warning' ? '⚠️' : '❌';

  logs.unshift({ type, message, timestamp, icon });

  // Manter apenas os últimos MAX_LOGS
  if (logs.length > MAX_LOGS) {
    logs = logs.slice(0, MAX_LOGS);
  }

  renderLogs();
}

// Renderizar logs
function renderLogs() {
  if (logs.length === 0) {
    logsContainer.innerHTML = '<p class="log-empty">Nenhum log ainda</p>';
    return;
  }

  const html = logs.map(log => {
    return `
      <div class="log-item log-${log.type}">
        ${log.icon} ${log.timestamp} - ${log.message}
      </div>
    `;
  }).join('');

  logsContainer.innerHTML = html;
}

// Formatar número com separador de milhar
function formatNumber(num) {
  return num.toLocaleString('pt-BR');
}

// Calcular tempo relativo
function getTimeAgo(timestamp) {
  const seconds = Math.floor((Date.now() - timestamp) / 1000);

  if (seconds < 60) {
    return `há ${seconds}s`;
  }

  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) {
    return `há ${minutes}m`;
  }

  const hours = Math.floor(minutes / 60);
  if (hours < 24) {
    return `há ${hours}h`;
  }

  const days = Math.floor(hours / 24);
  return `há ${days}d`;
}
