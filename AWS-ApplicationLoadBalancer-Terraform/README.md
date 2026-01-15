# Documentação do Projeto MeuMinimalApi

## Instação via linux
```
sudo apt upgrade dotnet-sdk-8.0
```


## Descrição

Este projeto consiste em duas APIs mínimas desenvolvidas com .NET 6, destinadas a serem executadas em contêineres Docker. O projeto também inclui infraestrutura como código usando o Terraform para provisionar recursos na AWS.

## Tecnologias Utilizadas

- .NET 6
- Docker
- Terraform
- AWS

## Estrutura do Projeto

O projeto está dividido em duas partes principais:

- **MyMinimalApi_a** e **MyMinimalApi_b**: Duas APIs mínimas desenvolvidas com .NET 6.
- **infra/terraform**: Contém os arquivos de configuração do Terraform para provisionar a infraestrutura necessária na AWS.

## Instruções de Compilação e Execução

### Pré-requisitos

- Docker
- .NET 6 SDK
- Terraform

### Compilando e Executando as APIs

Para compilar e executar as APIs em contêineres Docker, execute o script `build_and_push.sh`. Este script cria as imagens Docker para ambas as APIs, as etiqueta e as envia para um repositório Docker.

```sh
./build_and_push.sh