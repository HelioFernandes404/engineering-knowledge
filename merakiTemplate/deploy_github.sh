#!/bin/bash

# Solicita o nome do repositório
read -p "Digite o nome do repositório: " REPO_NAME

# Solicita a descrição do repositório
read -p "Digite a descrição do repositório: " REPO_DESC

# Solicita a visibilidade do repositório (public ou private)
read -p "O repositório deve ser público ou privado? (public/private): " REPO_VISIBILITY

# Cria o repositório no GitHub usando o GitHub CLI
gh repo create "$REPO_NAME" --description "$REPO_DESC" --"$REPO_VISIBILITY" --confirm

# Inicializa um repositório Git local com branch 'main'
git init "$REPO_NAME"
cd "$REPO_NAME" || exit
git checkout -b main

# Navega até o diretório do repositório
cd "$REPO_NAME" || exit

# Cria um arquivo README.md com o nome do repositório
echo "# $REPO_NAME" > README.md

# Adiciona os arquivos ao staging
git add .

# Realiza o commit inicial
git commit -m "Commit inicial"

# Adiciona o repositório remoto
git remote add origin "https://github.com/SEU_USUARIO/$REPO_NAME.git"

# Envia os arquivos para a branch main do repositório remoto
git push -u origin main
