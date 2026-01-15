# Changelog

Todas as mudanças notáveis do projeto serão documentadas aqui.

## [2.0.0] - 2025-11-26

### 🚀 NOVIDADES PRINCIPAIS

**Coleta Totalmente Automática!**
- Agora ao clicar em "🚀 Iniciar Coleta Automática", a extensão faz TUDO sozinha
- Não precisa mais clicar em botões separados de auto-scroll
- Um único botão para iniciar e parar

### ✨ Funcionalidades Adicionadas

- ✅ **Coleta automática completa**: Clica em cada post, extrai dados, volta e continua
- ✅ **Auto-scroll inteligente**: Rola a página automaticamente para carregar mais posts
- ✅ **Detecção de fim**: Para automaticamente quando não há mais posts
- ✅ **Método Click & Back**: Substitui hover por clique real (muito mais confiável)
- ✅ **Múltiplos métodos de extração**: 4 formas diferentes de extrair curtidas
- ✅ **Suporte a números abreviados**: Reconhece "1K", "2.5M", etc.

### 🔄 Mudanças

- **Interface simplificada**: Removido botão de auto-scroll separado
- **Botão principal**: Agora se chama "🚀 Iniciar Coleta Automática"
- **Status**: Mostra "Coletando automaticamente..." durante o processo
- **Versão**: Atualizada para 2.0.0

### 🛠️ Melhorias Técnicas

- Removidas variáveis obsoletas de auto-scroll
- Código mais limpo e organizado
- Logs mais informativos com emojis
- Melhor tratamento de erros

### 🐛 Correções

- ❌ **Removido sistema de hover** (não funcionava mais)
- ✅ **Implementado sistema de cliques** (100% funcional)
- ✅ Corrigida extração de curtidas em diferentes formatos
- ✅ Melhorada detecção de vídeos vs fotos

### 📝 Como Funciona Agora

1. **Você clica**: "🚀 Iniciar Coleta Automática"
2. **A extensão**:
   - Encontra todos os posts visíveis
   - Clica em cada um
   - Aguarda carregar
   - Extrai as curtidas
   - Volta para o perfil
   - Repete para o próximo
3. **Quando acaba os posts visíveis**:
   - Rola a página para baixo
   - Carrega mais posts
   - Continua o processo
4. **Quando não há mais posts**:
   - Para automaticamente
   - Mostra total coletado

### ⚠️ Notas de Atualização

Se você já tinha a versão anterior instalada:

1. Vá para `chrome://extensions/`
2. Clique no botão de **reload** (🔄) na extensão
3. Recarregue a página do Instagram (F5)
4. Pronto! Agora é só clicar em "Iniciar Coleta Automática"

---

## [1.0.0] - 2025-11-25

### Lançamento Inicial

- ✅ Coleta manual de posts
- ✅ Ranking por curtidas
- ✅ Detecção de fotos e vídeos
- ✅ Filtros por tipo
- ✅ Interface básica
- ✅ Sistema de logs
