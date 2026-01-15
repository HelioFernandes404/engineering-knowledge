# SMO - SYSTEM METRICS COLLECTOR

Sistema de coleta e exportação de métricas de sistema construído com arquitetura hexagonal em Python.

## 📋 Descrição

InfranGen é uma aplicação que coleta métricas do sistema (CPU, memória, disco) e as exporta em formato JSON. A aplicação foi desenvolvida seguindo os princípios da arquitetura hexagonal (ports and adapters), garantindo baixo acoplamento e alta testabilidade.

## 🏗️ Arquitetura

```
src/
├── domain/          # Lógica de negócio
│   ├── models.py    # Modelos de dados
│   ├── services.py  # Serviços do domínio
│   └── types.py     # Definições de tipos
├── ports/           # Interfaces/contratos
│   ├── config_port.py
│   ├── metrics_collector_port.py
│   └── metrics_exporter_port.py
└── adapters/        # Integrações externas
    ├── input/
    │   └── cli_adapter.py
    └── out/
        ├── config_adapter.py
        ├── system_metrics_adapter.py
        └── file_exporter_adapter.py
```

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.11+
- Docker (opcional)

### Instalação

1. Clone o repositório:
```bash
git clone <repository-url>
cd InfranGen
```

2. Crie um ambiente virtual:
```bash
make cav
# ou
python3 -m venv venv
```

3. Ative o ambiente virtual:
```bash
make aav
# ou
source venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

5. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env conforme necessário
```

## 🖥️ Uso

### Execução Local

```bash
# Modo contínuo (coleta métricas em intervalos regulares)
python main.py

# Execução única
python main.py --once
```

### Execução com Docker

```bash
# Build e execução com Makefile
make run

# Ou manualmente
docker build -t infragen:latest .
docker run infragen:latest
```

### Execução com Docker Compose

```bash
docker-compose up
```

### Execução com Kubernetes

O projeto inclui suporte completo para deployment no Kubernetes com monitoramento via VictoriaMetrics:

```bash
# Deploy completo (aplicação + monitoramento)
kubectl apply -f InfranGen.yaml

# Verificar status do deployment
kubectl get pods -n monitoring

# Acessar métricas do VictoriaMetrics
kubectl port-forward -n monitoring svc/victoriametrics 8428:8428
# Acesse http://localhost:8428
```

O deployment do Kubernetes inclui:
- **Namespace** `monitoring` para organização
- **VictoriaMetrics** para armazenamento de métricas
- **VMAgent** para coleta de métricas do cluster
- **InfranGen** com endpoint `/metrics` para Prometheus
- **RBAC** configurado para descoberta automática de serviços

## ⚙️ Configuração

A aplicação utiliza variáveis de ambiente para configuração. As principais opções incluem:

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `APP_NAME` | Nome da aplicação | MetricsApp |
| `METRICS_INTERVAL_SECONDS` | Intervalo de coleta (segundos) | 60 |
| `METRICS_OUTPUT_FILE` | Arquivo de saída | metrics.json |
| `COLLECT_CPU_METRICS` | Coletar métricas de CPU | true |
| `COLLECT_MEMORY_METRICS` | Coletar métricas de memória | true |
| `COLLECT_DISK_METRICS` | Coletar métricas de disco | true |
| `LOG_LEVEL` | Nível de log | INFO |

Veja `.env.example` para a lista completa de configurações disponíveis.

## 📊 Formato de Saída

As métricas são exportadas em formato JSON:

```json
{
  "timestamp": "2025-09-20T22:30:00.123456",
  "app_name": "MetricsApp",
  "app_version": "1.0.0",
  "app_environment": "development",
  "cpu_percent": 15.2,
  "cpu_count": 8,
  "memory_total": 16777216000,
  "memory_available": 8388608000,
  "memory_percent": 50.0,
  "disk_total": 1000000000000,
  "disk_used": 500000000000,
  "disk_free": 500000000000,
  "disk_percent": 50.0
}
```

## 🔧 Desenvolvimento

### Comandos Úteis

```bash
# Criar ambiente virtual
make cav

# Ativar ambiente virtual
make aav

# Executar aplicação
python main.py

# Build e execução Docker
make run
```

### Estrutura de Dados

- **SystemMetrics**: Métricas do sistema (CPU, memória, disco)
- **ApplicationMetrics**: Métricas da aplicação (nome, versão, ambiente)
- **MetricsSnapshot**: Snapshot completo das métricas em um momento específico

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Faça commit das suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Faça push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request
