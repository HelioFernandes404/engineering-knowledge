#!/bin/bash

# Navega para o diretório do projeto A
cd MeuMinimalApi_a/

# Constrói a imagem Docker para o projeto A
docker build -t public-api_a:latest .

# Marca a imagem para o repositório no Docker Hub (ou outro registro)
docker tag public-api_a:latest heliofernandes/public-api_a:latest

# Faz o push da imagem para o Docker Hub (ou outro registro)
docker push heliofernandes/public-api_a:latest

# Retorna ao diretório raiz
cd ..

# Navega para o diretório do projeto B
cd MeuMinimalApi_b/

# Constrói a imagem Docker para o projeto B
docker build -t public-api_b:latest .

# Marca a imagem para o repositório no Docker Hub (ou outro registro)
docker tag public-api_b:latest heliofernandes/public-api_b:latest

# Faz o push da imagem para o Docker Hub (ou outro registro)
docker push heliofernandes/public-api_b:latest

# Retorna ao diretório raiz
cd ..

# Echo the Docker Hub links for the pushed images
echo "Docker Hub links:"
echo "heliofernandes/public-api_a:latest"
echo "heliofernandes/public-api_b:latest"