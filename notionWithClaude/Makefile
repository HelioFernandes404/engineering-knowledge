# Makefile para melhorar textos
.PHONY: improve install clean

# Instala dependências necessárias
install:
	@echo "Instalando xclip para clipboard..."
	@sudo apt-get update && sudo apt-get install -y xclip || echo "xclip já está instalado ou erro na instalação"

# Função para melhorar texto
# Uso: make improve TEXT="improve: seu texto aqui"
improve:
	@if [ -z "$(TEXT)" ]; then \
		echo "Erro: Use 'make improve TEXT=\"improve: seu texto\"'"; \
		exit 1; \
	fi
	@python3 improve_text.py "$(TEXT)"

# Script rápido para melhorar texto
# Uso: ./improve "improve: seu texto"
improve_script:
	@echo '#!/bin/bash' > improve
	@echo 'python3 "$(PWD)/improve_text.py" "$$@"' >> improve
	@chmod +x improve
	@echo "Script 'improve' criado! Use: ./improve \"improve: seu texto\""

# Remove arquivos temporários
clean:
	@rm -f improve
	@echo "Arquivos temporários removidos"

# Mostra ajuda
help:
	@echo "Comandos disponíveis:"
	@echo "  make install           - Instala dependências (xclip)"
	@echo "  make improve TEXT=...  - Melhora o texto fornecido"
	@echo "  make improve_script    - Cria script executável './improve'"
	@echo "  make clean            - Remove arquivos temporários"
	@echo ""
	@echo "Exemplos:"
	@echo "  make improve TEXT=\"improve: este texto precisa ser melhorado\""
	@echo "  ./improve \"improve: outro texto para melhorar\""