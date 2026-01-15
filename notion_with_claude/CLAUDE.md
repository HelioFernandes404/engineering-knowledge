# Instruções para Melhoria de Texto

## Comando: improve
Quando receber input no formato `improve: texto...`, devo:

1. **Melhorar apenas a formatação e organização**
2. **NÃO alterar ou remover dados/informações**
3. **Corrigir gramática e ortografia quando necessário**
4. **Manter todo o conteúdo original intacto**

### O que fazer:
- Melhorar pontuação
- Organizar parágrafos
- Corrigir erros de português
- Formatar melhor o texto
- Deixar mais legível

### O que NÃO fazer:
- Alterar dados
- Remover informações
- Mudar o significado
- Adicionar conteúdo novo

## Scripts disponíveis:
- `python3 improve_text.py "improve: texto"` - Processa via Claude
- `make improve TEXT="improve: texto"` - Via Makefile
- `./improve "improve: texto"` - Script direto

## Funcionalidade:
O texto melhorado é automaticamente copiado para o clipboard.
