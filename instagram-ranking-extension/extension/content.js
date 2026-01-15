// Instagram Ranking Extension - Content Script
// Responsável por coletar dados de posts do Instagram

console.log('[Instagram Ranking] Content script loaded on instagram.com');

// Estado da coleta
let isCollecting = false;
let processedPosts = new Set();

// Listener para mensagens do popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('[Instagram Ranking] Received message:', request.action);

  if (request.action === 'START_COLLECTING') {
    startCollecting();
    sendResponse({ status: 'started' });
  } else if (request.action === 'STOP_COLLECTING') {
    stopCollecting();
    sendResponse({ status: 'stopped' });
  } else if (request.action === 'GET_STATUS') {
    sendResponse({ isCollecting: isCollecting });
  }
  return true;
});

// Iniciar coleta (agora automático)
async function startCollecting() {
  if (isCollecting) {
    console.log('[Instagram Ranking] Collection already running');
    return;
  }

  console.log('[Instagram Ranking] 🚀 Collection started - MODO AUTOMÁTICO');
  isCollecting = true;

  // Iniciar coleta automática dos posts visíveis
  await collectAllPostsAutomatically();
}

// Coletar todos os posts automaticamente
async function collectAllPostsAutomatically() {
  console.log('[Instagram Ranking] 🤖 Iniciando coleta automática de todos os posts...');

  let previousPostCount = 0;
  let noNewPostsCount = 0;
  const maxAttemptsWithoutNewPosts = 3;

  while (isCollecting) {
    // Pegar todos os posts visíveis na página atual
    const profilePosts = document.querySelectorAll('a[href*="/p/"]');
    const currentPostCount = profilePosts.length;

    console.log('[Instagram Ranking] 📊 Posts encontrados na página:', currentPostCount);

    if (currentPostCount > 0) {
      // Processar apenas os posts ainda não processados
      await processProfileGridPosts(profilePosts);
    }

    // Verificar se encontrou novos posts
    if (currentPostCount === previousPostCount) {
      noNewPostsCount++;
      console.log('[Instagram Ranking] ⚠️ Nenhum post novo encontrado. Tentativa:', noNewPostsCount);

      if (noNewPostsCount >= maxAttemptsWithoutNewPosts) {
        console.log('[Instagram Ranking] ✅ Fim da coleta - sem novos posts após', maxAttemptsWithoutNewPosts, 'tentativas');
        break;
      }
    } else {
      noNewPostsCount = 0;
      previousPostCount = currentPostCount;
    }

    // Scroll para baixo para carregar mais posts
    console.log('[Instagram Ranking] 📜 Scrolling para carregar mais posts...');
    window.scrollTo({
      top: document.documentElement.scrollHeight,
      behavior: 'smooth'
    });

    // Aguardar carregar novos posts
    await sleep(3000);
  }

  console.log('[Instagram Ranking] 🏁 Coleta automática finalizada!');
  console.log('[Instagram Ranking] 📊 Total de posts coletados:', processedPosts.size);

  // Parar a coleta
  stopCollecting();
}

// Parar coleta
function stopCollecting() {
  console.log('[Instagram Ranking] ⏸ Collection stopped');
  isCollecting = false;
}

// Processar posts da grade de perfil (clicando e voltando)
async function processProfileGridPosts(postLinks) {
  console.log('[Instagram Ranking] Processando', postLinks.length, 'links. Posts já processados:', processedPosts.size);

  // Guardar URL atual para poder voltar
  const originalUrl = window.location.href;

  for (const link of postLinks) {
    try {
      const postUrl = link.href;
      const postId = extractPostId(postUrl);

      if (!postId) {
        console.log('[Instagram Ranking] ❌ Post ID inválido para', postUrl);
        continue;
      }

      if (processedPosts.has(postId)) {
        console.log('[Instagram Ranking] ⏭ Post', postId, 'já foi processado anteriormente');
        continue;
      }

      console.log('[Instagram Ranking] 🔄 Abrindo post', postId);

      // Guardar thumbnail antes de navegar
      const thumbnail = extractThumbnailFromGrid(link);

      // Clicar no link para abrir o post
      link.click();

      // Aguardar a página carregar
      await sleep(2000);

      // Extrair dados do post aberto
      const postData = await extractDataFromOpenPost(postId, postUrl, thumbnail);

      if (postData) {
        processedPosts.add(postId);
        savePost(postData);
        console.log('[Instagram Ranking] ✅ Post processado:', postId, '-', postData.likes, 'likes', `(${postData.type})`);
      } else {
        console.warn('[Instagram Ranking] ❌ Não conseguiu extrair dados do post', postId);
      }

      // Voltar para a página de perfil
      console.log('[Instagram Ranking] ⬅ Voltando para o perfil');
      window.history.back();

      // Aguardar voltar à página de perfil
      await sleep(2000);

      // Aguardar um pouco mais para não sobrecarregar
      await sleep(500);

    } catch (error) {
      console.warn('[Instagram Ranking] Erro ao processar post da grade:', error);

      // Tentar voltar em caso de erro
      if (window.location.href !== originalUrl) {
        window.history.back();
        await sleep(2000);
      }
    }
  }
}

// Extrair dados quando o post está aberto
async function extractDataFromOpenPost(postId, postUrl, thumbnail) {
  console.log('[Instagram Ranking] Extraindo dados do post aberto...');

  // Aguardar o article aparecer
  let attempts = 0;
  let article = null;

  while (attempts < 10 && !article) {
    article = document.querySelector('article');
    if (!article) {
      await sleep(300);
      attempts++;
    }
  }

  if (!article) {
    console.warn('[Instagram Ranking] Article não encontrado após 3 segundos');
    return null;
  }

  // Extrair curtidas
  const likes = extractLikes(article);

  if (likes === null) {
    console.warn('[Instagram Ranking] Não conseguiu extrair curtidas do article');
    return null;
  }

  // Detectar tipo
  const postType = detectPostType(article);

  // Se não temos thumbnail, tentar extrair agora
  if (!thumbnail) {
    thumbnail = extractThumbnail(article);
  }

  return {
    postId: postId,
    url: postUrl,
    likes: likes,
    timestamp: Date.now(),
    thumbnail: thumbnail,
    type: postType
  };
}

// Função auxiliar para sleep
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Converter números abreviados (1K, 2.5M) para inteiros
function parseAbbreviatedNumber(str) {
  str = str.toUpperCase().trim();

  if (str.endsWith('K')) {
    return Math.round(parseFloat(str.slice(0, -1)) * 1000);
  } else if (str.endsWith('M')) {
    return Math.round(parseFloat(str.slice(0, -1)) * 1000000);
  } else {
    return parseInt(str.replace(/[,\.]/g, ''), 10);
  }
}

// Extrair thumbnail da grade
function extractThumbnailFromGrid(link) {
  const img = link.querySelector('img');
  return img ? img.src : null;
}

// Detectar tipo de post na grade
function detectPostTypeFromGrid(container) {
  // Na grade, vídeos tem um ícone específico
  const hasVideoIcon = container.querySelector('svg[aria-label*="ideo"], svg[aria-label*="ídeo"]');
  return hasVideoIcon ? 'video' : 'photo';
}

// Extrair dados de um post
function extractPostData(article) {
  // Extrair URL do post
  const postLink = article.querySelector('a[href*="/p/"]');
  if (!postLink) {
    return null;
  }

  const postUrl = postLink.href;
  const postId = extractPostId(postUrl);

  if (!postId) {
    return null;
  }

  // Extrair número de curtidas
  const likes = extractLikes(article);

  if (likes === null) {
    console.warn('[Instagram Ranking] Não foi possível extrair curtidas do post', postId);
    return null;
  }

  // Extrair thumbnail (opcional)
  const thumbnail = extractThumbnail(article);

  // Detectar tipo de post (video ou photo)
  const postType = detectPostType(article);

  return {
    postId: postId,
    url: postUrl,
    likes: likes,
    timestamp: Date.now(),
    thumbnail: thumbnail,
    type: postType
  };
}

// Extrair ID do post da URL
function extractPostId(url) {
  const match = url.match(/\/p\/([^\/]+)/);
  return match ? match[1] : null;
}

// Extrair número de curtidas
function extractLikes(article) {
  console.log('[Instagram Ranking] Tentando extrair curtidas do article...');

  // Método 1: Procurar por texto direto (com suporte a K/M)
  const text = article.innerText;

  const patterns = [
    /([0-9,\.]+[KMkm]?)\s*likes?/i,
    /([0-9,\.]+[KMkm]?)\s*curtidas?/i,
    /outras?\s*([0-9,\.]+[KMkm]?)\s*pessoas?/i,
    /other\s*([0-9,\.]+[KMkm]?)\s*people/i
  ];

  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match) {
      const likes = parseAbbreviatedNumber(match[1]);

      if (!isNaN(likes) && likes >= 0) {
        console.log('[Instagram Ranking] ✅ Curtidas extraídas (padrão texto):', likes);
        return likes;
      }
    }
  }

  // Método 2: Procurar por elementos com aria-label
  const elementsWithAria = article.querySelectorAll('[aria-label]');
  for (const element of elementsWithAria) {
    const ariaLabel = element.getAttribute('aria-label');

    // Tentar padrões em aria-label
    const ariaPatterns = [
      /(\d+[KMkm]?)\s*(like|curtida)/i,
      /(\d+[KMkm]?)\s*people/i,
      /(\d+[KMkm]?)\s*pessoa/i
    ];

    for (const pattern of ariaPatterns) {
      const match = ariaLabel.match(pattern);
      if (match) {
        const likes = parseAbbreviatedNumber(match[1]);
        if (!isNaN(likes) && likes >= 0) {
          console.log('[Instagram Ranking] ✅ Curtidas extraídas (aria-label):', likes);
          return likes;
        }
      }
    }
  }

  // Método 3: Procurar por section específica de curtidas
  const sections = article.querySelectorAll('section');
  for (const section of sections) {
    const sectionText = section.innerText;

    // Verificar se a section contém informação de curtidas
    if (sectionText.match(/like|curtida/i)) {
      const match = sectionText.match(/(\d+[KMkm]?)\s*(like|curtida)/i);
      if (match) {
        const likes = parseAbbreviatedNumber(match[1]);
        if (!isNaN(likes) && likes >= 0) {
          console.log('[Instagram Ranking] ✅ Curtidas extraídas (section):', likes);
          return likes;
        }
      }
    }
  }

  // Método 4: Procurar em elementos específicos (spans, buttons, links)
  const likeElements = article.querySelectorAll('span, a, button');

  for (const element of likeElements) {
    const elemText = element.innerText || element.textContent;

    if (elemText && (elemText.match(/like|curtida/i))) {
      const match = elemText.match(/(\d+[KMkm]?)\s*(like|curtida)/i);
      if (match) {
        const likes = parseAbbreviatedNumber(match[1]);
        if (!isNaN(likes) && likes >= 0) {
          console.log('[Instagram Ranking] ✅ Curtidas extraídas (elemento):', likes);
          return likes;
        }
      }
    }
  }

  console.warn('[Instagram Ranking] ❌ Nenhum método conseguiu extrair curtidas');
  console.log('[Instagram Ranking] Debug - Texto do article (primeiros 500 chars):', text.substring(0, 500));

  return null;
}

// Extrair URL da thumbnail
function extractThumbnail(article) {
  const img = article.querySelector('img[src]');
  return img ? img.src : null;
}

// Detectar tipo de post (video ou photo)
function detectPostType(article) {
  // Método 1: Procurar por elemento <video>
  const hasVideo = article.querySelector('video');
  if (hasVideo) {
    console.log('[Instagram Ranking] Tipo detectado: video');
    return 'video';
  }

  // Método 2: Procurar por ícone de vídeo (SVG com aria-label)
  const videoIcon = article.querySelector('svg[aria-label*="ideo"], svg[aria-label*="ídeo"]');
  if (videoIcon) {
    console.log('[Instagram Ranking] Tipo detectado: video (por ícone)');
    return 'video';
  }

  // Método 3: Verificar classes ou atributos comuns de vídeo
  const videoIndicators = article.querySelectorAll('[class*="video"], [class*="Video"]');
  if (videoIndicators.length > 0) {
    console.log('[Instagram Ranking] Tipo detectado: video (por classe)');
    return 'video';
  }

  // Método 4: Procurar por span com texto de duração do vídeo
  const text = article.innerText;
  if (text.match(/\d{1,2}:\d{2}/)) { // Formato MM:SS ou M:SS
    const hasTimeIndicator = article.querySelector('[style*="position: absolute"]');
    if (hasTimeIndicator) {
      console.log('[Instagram Ranking] Tipo detectado: video (por timestamp)');
      return 'video';
    }
  }

  // Default: photo
  console.log('[Instagram Ranking] Tipo detectado: photo');
  return 'photo';
}

// Salvar post no storage
function savePost(postData) {
  chrome.storage.local.get(['posts'], (result) => {
    const posts = result.posts || [];

    // Verificar se já existe (dupla verificação)
    const exists = posts.some(p => p.postId === postData.postId);

    if (!exists) {
      posts.push(postData);

      chrome.storage.local.set({ posts: posts }, () => {
        console.log('[Instagram Ranking] Post salvo. Total:', posts.length);
      });
    } else {
      console.log('[Instagram Ranking] Post', postData.postId, 'já existe no storage');
    }
  });
}

// Adicionar logs para status da página
function logPageStatus() {
  const isInstagram = window.location.hostname.includes('instagram.com');
  console.log('[Instagram Ranking] On Instagram:', isInstagram);
  console.log('[Instagram Ranking] Current URL:', window.location.href);
}

logPageStatus();
