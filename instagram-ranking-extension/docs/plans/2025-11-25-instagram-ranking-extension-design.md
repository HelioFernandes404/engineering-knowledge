# Instagram Ranking Extension - Design Document

**Data:** 2025-11-25
**Objetivo:** Extensão de navegador para coletar e rankear posts do Instagram por curtidas

## 1. Visão Geral

### Propósito
Extensão Chrome/Edge que permite ao usuário coletar manualmente dados de posts de perfis públicos do Instagram e visualizar um ranking simples ordenado por número de curtidas.

### Caso de Uso Principal
- Usuário visita qualquer perfil público no Instagram Web
- Ativa a coleta manualmente através da extensão
- Rola a página para carregar posts
- Visualiza ranking em tempo real no popup
- Para a coleta quando terminar

### Escopo
- **Incluído:** Coleta manual, ranking por curtidas, armazenamento local, interface simples
- **Excluído:** Coleta automática, análise de comentários, exportação de dados, gráficos avançados

## 2. Arquitetura

### Componentes

#### 2.1 Manifest (manifest.json)
- **Versão:** Manifest V3
- **Permissões:**
  - `activeTab` - Acesso à aba atual do Instagram
  - `storage` - Armazenamento local de dados
- **Content Scripts:** Injetado em `*://www.instagram.com/*`
- **Action:** Popup da extensão

#### 2.2 Content Script (content.js)
- **Responsabilidades:**
  - Escutar comandos do popup (iniciar/pausar)
  - Observar mudanças no DOM usando MutationObserver
  - Extrair dados dos posts visíveis
  - Salvar dados no chrome.storage.local

#### 2.3 Popup (popup.html + popup.js + styles.css)
- **Responsabilidades:**
  - Interface de controle (iniciar/pausar/limpar)
  - Exibir ranking ordenado por curtidas
  - Mostrar status e logs em tempo real
  - Links para abrir posts no Instagram

### Estrutura de Arquivos
```
instagram-ranking-extension/
├── manifest.json
├── content.js
├── popup.html
├── popup.js
├── styles.css
└── icons/
    ├── icon16.png
    ├── icon48.png
    └── icon128.png
```

## 3. Coleta de Dados

### Estratégia: Leitura do DOM

**Por que DOM e não API?**
- Simplicidade: não depende de endpoints internos
- Confiabilidade: coleta apenas o que está visível
- Conformidade: não intercepta requests privadas

### Processo de Extração

1. **Identificação de Posts**
   - Buscar elementos `<article>` no DOM
   - Cada post é um article com estrutura previsível

2. **Extração de URL**
   - Seletor: `article a[href*="/p/"]`
   - Formato: `https://www.instagram.com/p/CxYz123/`
   - Post ID: extrair código após `/p/`

3. **Extração de Curtidas**
   - Buscar texto contendo "likes" ou "curtidas"
   - Usar regex para capturar número: `/([0-9,\.]+)\s*(likes|curtidas)/i`
   - Converter string para número (remover vírgulas/pontos)

4. **Extração de Thumbnail (opcional)**
   - Seletor: `article img[src]`
   - Primeira imagem do post

### Estrutura de Dados

```javascript
{
  postId: "CxYz123",           // ID único extraído da URL
  url: "https://www.instagram.com/p/CxYz123/",
  likes: 1234,                 // Número de curtidas
  timestamp: 1700000000000,    // Quando foi coletado (ms)
  thumbnail: "https://..."     // URL da imagem (opcional)
}
```

### Armazenamento

- **Chave:** `"posts"`
- **Valor:** Array de objetos
- **API:** `chrome.storage.local`
- **Atualização:** Em tempo real conforme novos posts são encontrados

### Prevenção de Duplicatas

- Manter Set de `postId` já processados na memória
- Antes de adicionar, verificar se ID já existe
- Evita reprocessar posts ao rolar para cima/baixo

### MutationObserver

```javascript
const observer = new MutationObserver((mutations) => {
  // A cada mudança no DOM
  const articles = document.querySelectorAll('article');
  articles.forEach(article => {
    // Extrair e salvar dados
  });
});

observer.observe(document.body, {
  childList: true,
  subtree: true
});
```

## 4. Interface do Usuário

### Layout do Popup (300x450px)

```
┌─────────────────────────────┐
│  Instagram Ranking          │
│  ───────────────────────    │
│                             │
│  Status: ✅ Coletando...    │
│  Posts coletados: 15        │
│  Último post: há 2s         │
│                             │
│  [⏸ Pausar Coleta]          │
│  [🗑 Limpar Dados]          │
│  [📋 Ver Logs]              │
│  ───────────────────────    │
│                             │
│  🥇 #1 - 1,234 likes        │
│     [Ver Post]              │
│                             │
│  🥈 #2 - 987 likes          │
│     [Ver Post]              │
│                             │
│  🥉 #3 - 756 likes          │
│     [Ver Post]              │
│                             │
│  ... (scroll para mais)     │
└─────────────────────────────┘
```

### Componentes da Interface

1. **Cabeçalho de Status**
   - Status atual (coletando/pausado/erro)
   - Contador de posts coletados
   - Timestamp do último post encontrado

2. **Botões de Controle**
   - **Iniciar/Pausar:** Toggle entre estados
     - Iniciar: Botão azul "▶ Iniciar Coleta"
     - Pausar: Botão verde "⏸ Pausar Coleta"
   - **Limpar Dados:** Botão vermelho, reseta tudo
   - **Ver Logs:** Expande área de debug

3. **Lista de Ranking**
   - Ordenada por curtidas (decrescente)
   - Mostra top posts (scroll se necessário)
   - Cada item: posição + curtidas + link

4. **Área de Logs (expansível)**
   - Últimas 10 ações/eventos
   - Útil para debug sem DevTools

### Estados Visuais

| Estado | Indicador | Descrição |
|--------|-----------|-----------|
| Coletando | ✅ Verde | MutationObserver ativo |
| Pausado | ⏸ Cinza | Coleta parada |
| Erro | ⚠️ Amarelo | Não está no Instagram |
| Inativo | ❌ Vermelho | Extensão não inicializada |

### Fluxo de Interação

1. Usuário navega para `instagram.com/perfil_qualquer`
2. Clica no ícone da extensão → Popup abre
3. Clica "Iniciar Coleta" → Botão muda para "Pausar"
4. Rola a página do Instagram → Posts aparecem no ranking
5. Observa ranking sendo atualizado em tempo real
6. Clica "Pausar" quando terminar
7. Clica "Ver Post" para abrir em nova aba
8. Clica "Limpar Dados" para analisar outro perfil

## 5. Comunicação Entre Componentes

### Popup → Content Script

```javascript
// popup.js
chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
  chrome.tabs.sendMessage(tabs[0].id, {
    action: "START_COLLECTING"  // ou "STOP_COLLECTING"
  });
});
```

### Content Script → Storage

```javascript
// content.js
chrome.storage.local.get(['posts'], (result) => {
  const posts = result.posts || [];
  posts.push(newPost);
  chrome.storage.local.set({posts: posts});
});
```

### Popup ← Storage

```javascript
// popup.js
chrome.storage.local.get(['posts'], (result) => {
  const posts = result.posts || [];
  renderRanking(posts);
});

// Listener para mudanças em tempo real
chrome.storage.onChanged.addListener((changes) => {
  if (changes.posts) {
    renderRanking(changes.posts.newValue);
  }
});
```

## 6. Logging e Debug

### Sistema de Logs

#### Console do DevTools (Desenvolvimento)
```javascript
console.log('[Instagram Ranking] Coleta iniciada');
console.log('[Instagram Ranking] Novo post encontrado:', postId);
console.log('[Instagram Ranking] Posts salvos:', posts.length);
console.warn('[Instagram Ranking] Erro ao extrair curtidas:', error);
```

#### Feedback Visual (Usuário)
- Status em tempo real no topo do popup
- Contador de posts coletados
- Timestamp do último post
- Área de logs expansível

### Eventos Logados

| Evento | Tipo | Mensagem |
|--------|------|----------|
| Content script carregado | Info | "Content script loaded on instagram.com" |
| Coleta iniciada | Info | "Collection started" |
| Post encontrado | Success | "Post CxYz123: 1234 likes" |
| Duplicata ignorada | Debug | "Post CxYz123 already collected" |
| Salvamento | Info | "Saved 15 posts to storage" |
| Erro de extração | Warning | "Failed to extract likes from article" |
| Coleta pausada | Info | "Collection stopped" |

### Debug Console no Popup

```
[Ver Logs ▼]
───────────────────────
✅ 23:45:12 - Post encontrado: 1,234 likes
✅ 23:45:10 - Post encontrado: 987 likes
⚠️  23:45:08 - Post sem curtidas visíveis
✅ 23:45:05 - Coleta iniciada
```

## 7. Tratamento de Erros

### Cenários de Erro

1. **Usuário não está no Instagram**
   - Detectar: verificar `window.location.hostname`
   - Ação: Mostrar mensagem "Abra um perfil do Instagram"

2. **Estrutura HTML mudou**
   - Detectar: seletores não encontram elementos
   - Ação: Logar erro, não quebrar extensão

3. **Curtidas não visíveis**
   - Detectar: regex não encontra número
   - Ação: Ignorar post, logar warning

4. **Storage cheio**
   - Detectar: erro ao salvar no chrome.storage
   - Ação: Alertar usuário, sugerir limpar dados

### Validações

```javascript
// Validar URL do post
if (!postUrl || !postUrl.includes('/p/')) {
  console.warn('[Instagram Ranking] Invalid post URL');
  return;
}

// Validar número de curtidas
if (isNaN(likes) || likes < 0) {
  console.warn('[Instagram Ranking] Invalid likes count');
  return;
}

// Validar que está no Instagram
if (!window.location.hostname.includes('instagram.com')) {
  console.error('[Instagram Ranking] Not on Instagram');
  return;
}
```

## 8. Considerações de Privacidade e Ética

### Princípios

1. **Apenas dados públicos** - Coleta somente o que está visível na interface
2. **Armazenamento local** - Nenhum dado enviado para servidores externos
3. **Controle do usuário** - Coleta manual, usuário decide quando iniciar/parar
4. **Transparência** - Código aberto, usuário pode auditar

### Conformidade

- ✅ Não intercepta requisições privadas
- ✅ Não bypassa autenticação
- ✅ Não faz scraping automatizado em massa
- ✅ Uso pessoal e educacional

### Limitações Auto-impostas

- Sem coleta automática/agendada
- Sem envio de dados para APIs externas
- Sem armazenamento de informações pessoais de usuários
- Apenas perfis que o usuário visita manualmente

## 9. Próximos Passos

### Implementação

1. Criar estrutura de arquivos
2. Implementar manifest.json
3. Implementar content.js com lógica de coleta
4. Implementar popup.html/js/css
5. Criar ícones da extensão
6. Testar em diferentes perfis do Instagram
7. Ajustar seletores se necessário

### Testes

- Testar em perfis com diferentes quantidades de posts
- Verificar performance com 100+ posts coletados
- Testar mudança de perfis sem limpar dados
- Validar que duplicatas não são adicionadas
- Testar em português e inglês (Instagram muda textos)

### Melhorias Futuras (opcional)

- Exportar dados para CSV/JSON
- Gráfico de distribuição de curtidas
- Filtros (por data, por mínimo de curtidas)
- Comparação entre perfis
- Ranking de comentários também
