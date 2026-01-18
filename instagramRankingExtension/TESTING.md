# Guia de Teste - Auto-Scroll

## Passo a Passo para Testar

### 1. Recarregar a Extensão

1. Abra `chrome://extensions/`
2. Encontre "Instagram Ranking"
3. Clique no ícone de **RELOAD** (🔄)
4. Verifique que não há erros

### 2. Recarregar a Página do Instagram

1. Vá para `instagram.com`
2. Pressione **F5** para recarregar
3. Navegue até um perfil qualquer
4. Espere a página carregar completamente

### 3. Abrir Console

1. Pressione **F12** para abrir DevTools
2. Vá para a aba **Console**
3. Procure por: `[Instagram Ranking] Content script loaded`
4. Se não aparecer, recarregue a página novamente

### 4. Testar Auto-Scroll

1. Clique no ícone da extensão
2. Clique no botão **"🤖 Auto-Scroll"**
3. Observe o console do DevTools

### O que você deve ver no Console:

```
[Instagram Ranking] Content script loaded on instagram.com
[Instagram Ranking] On Instagram: true
[Instagram Ranking] Current URL: https://www.instagram.com/...
[Instagram Ranking] Received message: START_AUTO_SCROLL
[Instagram Ranking] Starting auto-scroll with maxPosts: null
[Instagram Ranking] Starting collection for auto-scroll
[Instagram Ranking] Collection started
[Instagram Ranking] Auto-scroll started (no limit)
[Instagram Ranking] Auto-scroll: posts coletados = 0
[Instagram Ranking] Auto-scroll: posts coletados = 5
...
```

### O que você deve ver na página:

- A página deve começar a **rolar automaticamente** para baixo
- O contador de posts no popup deve **aumentar**
- Logs devem aparecer quando clicar em "Ver Logs"

## Se não funcionar:

### Erro: "Erro de comunicação com a página"

**Solução:**
1. Recarregue a página do Instagram (F5)
2. Aguarde 2-3 segundos
3. Tente novamente

### Erro: Botão não faz nada

**Solução:**
1. Abra o console do popup:
   - Clique com botão direito no ícone da extensão
   - Selecione "Inspecionar popup"
   - Vá para a aba Console
2. Clique no botão e veja os logs
3. Verifique se há erro

### Erro: Content script não carrega

**Solução:**
1. Vá em `chrome://extensions/`
2. Clique em "Detalhes" na extensão
3. Role até "Inspecionar visualizações"
4. Clique em "background page" ou "service worker"
5. Veja se há erros

## Comandos Úteis para Debug

Abra o console da página do Instagram e digite:

```javascript
// Verificar se content script está carregado
console.log('Test');

// Verificar variáveis
console.log('isCollecting:', window.isCollecting);
console.log('isAutoScrolling:', window.isAutoScrolling);
```

## Checklist de Verificação

- [ ] Extensão recarregada
- [ ] Página do Instagram recarregada
- [ ] Console do DevTools aberto
- [ ] Mensagem "Content script loaded" apareceu
- [ ] Está em uma página de perfil (não no feed)
- [ ] Botão Auto-Scroll aparece na extensão
- [ ] Cliquei no botão Auto-Scroll
- [ ] Observei os logs no console

## Resultado Esperado

✅ Página rola automaticamente
✅ Posts são coletados
✅ Logs aparecem no console
✅ Contador aumenta no popup
✅ Para automaticamente quando terminar
