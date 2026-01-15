# CV Template Renaming Design

**Data:** 2025-12-19
**Objetivo:** Simplificar nomenclatura do CV para padrão autodescritivo e preparar para múltiplas variações de idioma

## Problema Atual

- Template chamado `cv.tex` (genérico, não indica de quem é)
- Output `Helio_Fernandes_CV_2025.pdf` (inclui ano que precisa atualizar)
- Lógica complexa de renomeação no `.latexmkrc`

## Solução Proposta

### 1. Estrutura de Arquivos

```
templates/cv/
├── helio_fernandes_pt.tex      # CV em português (principal)
├── .latexmkrc                  # Configuração: gera helio_fernandes_pt.pdf
├── Makefile                    # Comandos específicos do CV
└── [outros arquivos auxiliares]
```

**Mudanças:**
- `cv.tex` → `helio_fernandes_pt.tex`
- Output: `helio_fernandes_pt.pdf` (sem ano)
- Padrão para idiomas: `helio_fernandes_{idioma}.tex`

### 2. Configuração LaTeXmk

**Arquivo `.latexmkrc` atualizado:**
```perl
# Configuração para gerar helio_fernandes_pt.pdf
$pdf_mode = 1;
$pdflatex = 'pdflatex -interaction=nonstopmode';
$out_dir = '.';

# Define o nome do arquivo de saída
$jobname = 'helio_fernandes_pt';
```

**Como funciona:**
- `$jobname` força geração direta do PDF com nome correto
- Sem necessidade de renomeação pós-compilação
- Mais simples e direto

### 3. Makefile Raiz

**Comando `make cv`:**
```makefile
.PHONY: cv
cv:
	@if [ -f "helio_fernandes_pt.tex" ]; then \
		$(LATEXMK) -pdf helio_fernandes_pt.tex; \
	elif [ -f "templates/cv/helio_fernandes_pt.tex" ]; then \
		cd templates/cv && $(LATEXMK) -pdf helio_fernandes_pt.tex; \
	else \
		echo "No helio_fernandes_pt.tex found in current directory or templates/cv/"; \
	fi
```

**Comando `make clean`:**
```makefile
# Atualizar linha de limpeza de PDFs:
@find . -name "helio_fernandes_*.pdf" -delete 2>/dev/null || true
```

### 4. Documentação

**CLAUDE.md - Atualizar seção "CV Template Specific Commands":**
- Remover referências a `cv.tex` e `Helio_Fernandes_CV_2025.pdf`
- Adicionar novo padrão `helio_fernandes_pt.tex` → `helio_fernandes_pt.pdf`
- Documentar padrão de idiomas

**README.md:**
- Atualizar exemplos com novo nome de arquivo

### 5. Preparação para Futuras Variações

**Quando criar versão em inglês:**
1. Copiar `helio_fernandes_pt.tex` → `helio_fernandes_en.tex`
2. Traduzir conteúdo mantendo estrutura
3. Compilar: `latexmk -pdf helio_fernandes_en.tex` → `helio_fernandes_en.pdf`
4. `.latexmkrc` infere automaticamente o nome

**Padrão estabelecido:**
- Nomenclatura: `helio_fernandes_{idioma}.tex`
- Output automático: `helio_fernandes_{idioma}.pdf`
- `make cv` compila versão _pt (principal)

## Benefícios

1. **Autodescritivo:** Nome do arquivo indica claramente de quem é o CV
2. **Atemporal:** Sem ano no nome do PDF
3. **Escalável:** Padrão consistente para múltiplos idiomas
4. **Simples:** Geração direta do PDF sem renomeação
5. **Flexível:** Fácil adicionar variações (_en, _es, etc)

## Tarefas de Implementação

1. Renomear `templates/cv/cv.tex` → `templates/cv/helio_fernandes_pt.tex`
2. Atualizar `templates/cv/.latexmkrc` com novo `$jobname`
3. Atualizar `/Makefile` (comandos cv e clean)
4. Atualizar `/CLAUDE.md` (seção CV commands)
5. Atualizar `/README.md` (exemplos)
6. Testar compilação: `make cv` deve gerar `helio_fernandes_pt.pdf`
7. Testar limpeza: `make clean` deve remover PDFs
