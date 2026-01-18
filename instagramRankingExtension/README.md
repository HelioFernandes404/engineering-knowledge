# Instagram Ranking Extension

Extensão de navegador para coletar e rankear posts do Instagram por curtidas.

## Descrição

Esta extensão permite que você colete manualmente dados de posts de perfis públicos do Instagram e visualize um ranking ordenado por número de curtidas. Todos os dados são armazenados localmente no seu navegador.

## Funcionalidades

- ✅ Coleta manual de posts do Instagram
- ✅ **🤖 Auto-Scroll automático** com limite configurável
- ✅ Ranking por número de curtidas
- ✅ **Detecção automática de vídeos e fotos**
- ✅ **Filtros por tipo de conteúdo** (Todos / Fotos / Vídeos)
- ✅ Interface simples e intuitiva
- ✅ Armazenamento local (sem envio de dados)
- ✅ Sistema de logs para debug
- ✅ Controle total sobre quando coletar

## Instalação

### Chrome / Edge / Brave

1. **Baixe ou clone este repositório**
   ```bash
   git clone <url-do-repositorio>
   cd screping_instagram
   ```

2. **Abra a página de extensões**
   - Chrome: `chrome://extensions/`
   - Edge: `edge://extensions/`
   - Brave: `brave://extensions/`

3. **Ative o "Modo do desenvolvedor"**
   - Toggle no canto superior direito da página

4. **Carregue a extensão**
   - Clique em "Carregar sem compactação" (ou "Load unpacked")
   - Selecione a pasta `extension/` dentro deste projeto

5. **Pronto!**
   - O ícone da extensão aparecerá na barra de ferramentas
   - Fixe a extensão para acesso rápido

## Como Usar

### Passo 1: Visite um perfil do Instagram

1. Abra o Instagram Web (`instagram.com`)
2. Faça login na sua conta
3. Navegue até qualquer perfil público

### Passo 2: Escolha o modo de coleta

**Modo Manual:**
1. Clique no ícone da extensão
2. Clique no botão "▶ Iniciar Coleta"
3. Role a página manualmente para carregar posts
4. Observe o ranking sendo atualizado em tempo real

**Modo Automático (Auto-Scroll):**
1. Clique no ícone da extensão
2. (Opcional) Digite um limite de posts no campo "Max posts"
3. Clique no botão "🤖 Auto-Scroll"
4. A página vai rolar automaticamente e coletar posts
5. Para quando atingir o limite ou fim da página

### Passo 3: Visualize o ranking

- Os posts aparecem ordenados por curtidas
- Top 3 recebem medalhas 🥇 🥈 🥉
- Cada post mostra um badge indicando se é 📷 Foto ou 🎥 Vídeo
- Clique em "Ver Post" para abrir no Instagram

### Passo 4: Use os filtros

- **Todos**: Mostra fotos e vídeos juntos
- **📷 Fotos**: Filtra apenas posts com fotos
- **🎥 Vídeos**: Filtra apenas posts com vídeos

### Passo 5: Pause e limpe

- Clique "⏸ Pausar Coleta" quando terminar
- Use "🗑 Limpar Dados" para resetar e analisar outro perfil

## Interface

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
│  [🤖 Auto-Scroll] [Max: 50] │
│  [🗑 Limpar Dados]          │
│  [📋 Ver Logs]              │
│  ───────────────────────    │
│                             │
│  Ranking por Curtidas       │
│  [Todos][📷 Fotos][🎥 Vídeos]│
│                             │
│  🥇 #1 - 1,234 likes 🎥     │
│     [Ver Post]              │
│                             │
│  🥈 #2 - 987 likes 📷       │
│     [Ver Post]              │
│                             │
│  🥉 #3 - 756 likes 🎥       │
│     [Ver Post]              │
│  ...                        │
└─────────────────────────────┘
```

## Debug e Logs

### Ver Logs no Popup

- Clique em "📋 Ver Logs" para expandir área de debug
- Mostra últimas 10 ações
- Útil para verificar se a coleta está funcionando

### Logs no Console (DevTools)

1. Abra DevTools (F12)
2. Vá para a aba "Console"
3. Procure por `[Instagram Ranking]`
4. Logs incluem:
   - Posts encontrados
   - Curtidas extraídas
   - Erros de extração
   - Status da coleta

## Estrutura do Projeto

```
screping_instagram/
├── extension/
│   ├── manifest.json         # Configuração da extensão
│   ├── content.js            # Script de coleta (injetado no Instagram)
│   ├── popup.html            # Interface da extensão
│   ├── popup.js              # Lógica da interface
│   ├── styles.css            # Estilos
│   └── icons/                # Ícones da extensão
│       ├── icon16.png
│       ├── icon48.png
│       └── icon128.png
├── docs/
│   └── plans/
│       └── 2025-11-25-instagram-ranking-extension-design.md
└── README.md
```

## Tecnologias

- **Manifest V3** - Versão mais recente do padrão de extensões
- **Vanilla JavaScript** - Sem dependências externas
- **Chrome Storage API** - Armazenamento local
- **MutationObserver** - Detecção de novos posts no DOM
- **Auto-Scroll** - Scroll automático com detecção de fim de página
- **Método Click & Back** - Clica no post, extrai dados, e volta para o perfil

## 🔄 Como a Extração Funciona

A extensão usa a estratégia de **"clicar e voltar"** (v1.0+):

1. 🖱️ **Clica** em cada link de post na grade do perfil
2. ⏳ **Aguarda** 2 segundos para a página do post carregar
3. 📊 **Extrai** as curtidas do post aberto usando múltiplos métodos:
   - Padrões de texto (regex)
   - Atributos `aria-label`
   - Elementos `<section>`
   - Suporta formatos: "123", "1.5K", "2M"
4. ⬅️ **Volta** para o perfil usando `window.history.back()`
5. 🔄 **Repete** para o próximo post

### Por que não usamos hover?

A versão anterior tentava fazer hover nos posts, mas:
- ❌ Instagram mudou a estrutura e o overlay não aparece mais
- ❌ Eventos de mouse são difíceis de simular
- ✅ Clicar e voltar é **muito mais confiável** e consistente

## Considerações de Privacidade

### O que esta extensão coleta

- URLs de posts públicos do Instagram
- Número de curtidas visível na interface
- Thumbnails dos posts

### O que esta extensão NÃO faz

- ❌ Não envia dados para servidores externos
- ❌ Não coleta informações pessoais de usuários
- ❌ Não bypassa autenticação ou privacidade
- ❌ Não faz scraping automatizado em massa
- ❌ Não intercepta requisições privadas

### Armazenamento

- Todos os dados ficam no `chrome.storage.local`
- Dados persistem até você limpar manualmente
- Nenhuma transmissão de dados pela rede

## Limitações

- Funciona apenas no Instagram Web (não no app mobile)
- Depende da estrutura HTML do Instagram
- Se o Instagram mudar o layout, pode precisar de ajustes
- Auto-scroll pode ser detectado pelo Instagram (use com moderação)

## Solução de Problemas

### Extensão não aparece no Instagram

- Verifique se você está em `www.instagram.com`
- Recarregue a página do Instagram (F5)
- Verifique se a extensão está ativada em `chrome://extensions/`

### Não está coletando posts

1. Abra DevTools (F12) → Console
2. Procure por erros em vermelho
3. Verifique se há logs `[Instagram Ranking]`
4. Clique em "Ver Logs" no popup para debug

### Auto-Scroll não funciona

- Certifique-se de estar na página de perfil (não no feed)
- Verifique se a página já está no topo antes de iniciar
- O auto-scroll para automaticamente ao detectar fim da página
- Use um limite de posts menor se estiver demorando muito

### Curtidas não aparecem

- Instagram pode ter mudado a estrutura HTML
- Verifique se as curtidas estão visíveis na página
- Alguns posts podem não mostrar curtidas publicamente

### "Erro de comunicação com a página"

- Recarregue a página do Instagram
- Desative e reative a extensão
- Verifique se não há conflitos com outras extensões

## Desenvolvimento

### Modificar o código

1. Edite os arquivos em `extension/`
2. Vá para `chrome://extensions/`
3. Clique no botão "Recarregar" (ícone de refresh) na extensão
4. Recarregue a página do Instagram

### Adicionar novas funcionalidades

Consulte o documento de design em:
`docs/plans/2025-11-25-instagram-ranking-extension-design.md`

## Avisos Legais

### Termos de Serviço

⚠️ Esta extensão é para **uso pessoal e educacional**. Coletar dados do Instagram, mesmo que públicos, pode violar os Termos de Serviço da plataforma.

### Uso Recomendado

- ✅ Analisar seu próprio conteúdo
- ✅ Aprender sobre extensões de navegador
- ✅ Estudar web scraping e DOM manipulation
- ❌ Uso comercial sem autorização
- ❌ Coleta massiva de dados
- ❌ Violação de privacidade

### Responsabilidade

O uso desta ferramenta é de sua total responsabilidade. O desenvolvedor não se responsabiliza por:
- Violação dos Termos de Serviço do Instagram
- Bloqueio ou suspensão de contas
- Uso indevido dos dados coletados

## Licença

Este projeto é fornecido "como está" para fins educacionais.

## Suporte

Para problemas ou sugestões:
1. Verifique a seção "Solução de Problemas"
2. Consulte os logs no console
3. Revise o documento de design

## Roadmap (Melhorias Futuras)

- [ ] Exportar dados para CSV/JSON
- [ ] Gráfico de distribuição de curtidas
- [ ] Ranking de comentários
- [ ] Filtros por data e número mínimo de curtidas
- [ ] Comparação entre múltiplos perfis
- [ ] Estatísticas agregadas (média, mediana, etc.)

---

**Desenvolvido para fins educacionais** 📚
