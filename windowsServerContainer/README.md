# Windows Server 2012 R2 + OpenTelemetry + VictoriaLogs K3S

Ambiente de laboratório para executar Windows Server 2012 R2 em container Docker, coletando logs via OpenTelemetry Collector e armazenando no VictoriaLogs Cluster em K3S.

## 📐 Arquitetura

```
┌──────────────────────────────────────────────────────┐
│  Windows Server 2012 R2 (Docker Container)           │
│  IP: 172.30.0.3                                      │
│  ┌────────────────────────────────────────────────┐ │
│  │  OpenTelemetry Collector 0.88.0 (contrib)     │ │
│  │  ┌──────────────────────────────────────────┐ │ │
│  │  │  Receivers:                              │ │ │
│  │  │  • Windows Event Log - Application       │ │ │
│  │  │  • Windows Event Log - System            │ │ │
│  │  │  • Windows Event Log - Security          │ │ │
│  │  └──────────────────────────────────────────┘ │ │
│  │  ┌──────────────────────────────────────────┐ │ │
│  │  │  Processors:                             │ │ │
│  │  │  • Resource Detection (hostname)         │ │ │
│  │  │  • Attributes (environment, datacenter)  │ │ │
│  │  │  • Batch (8192 logs, gzip compression)   │ │ │
│  │  └──────────────────────────────────────────┘ │ │
│  │                       │                        │ │
│  │                       │ OTLP/HTTP              │ │
│  │                       │ Port: 8888 (metrics)   │ │
│  └───────────────────────┼────────────────────────┘ │
└────────────────────────┼──────────────────────────┘
                         │
                         │ http://192.168.100.12:31281
                         │ /insert/opentelemetry/v1/logs
                         ▼
┌─────────────────────────────────────────────────────┐
│  Host Linux (192.168.100.12)                        │
│  ┌────────────────────────────────────────────────┐ │
│  │  K3S Cluster - Namespace: logging             │ │
│  │  ┌──────────────────────────────────────────┐ │ │
│  │  │  VictoriaLogs Cluster                    │ │ │
│  │  │                                          │ │ │
│  │  │  ┌─────────────┐  ┌─────────────┐      │ │ │
│  │  │  │  vlinsert   │  │  vlinsert   │      │ │ │
│  │  │  │  (replica)  │  │  (replica)  │      │ │ │
│  │  │  └──────┬──────┘  └──────┬──────┘      │ │ │
│  │  │         │                 │             │ │ │
│  │  │         └────────┬────────┘             │ │ │
│  │  │                  │                      │ │ │
│  │  │         ┌────────▼────────┐             │ │ │
│  │  │         │   vlstorage     │             │ │ │
│  │  │         │  (StatefulSet)  │             │ │ │
│  │  │         │  • Pod 0 (PV)   │             │ │ │
│  │  │         │  • Pod 1 (PV)   │             │ │ │
│  │  │         └────────┬────────┘             │ │ │
│  │  │                  │                      │ │ │
│  │  │         ┌────────▼────────┐             │ │ │
│  │  │         │   vlselect      │             │ │ │
│  │  │         │  (replica x2)   │             │ │ │
│  │  │         │  Port: 9471     │             │ │ │
│  │  │         └─────────────────┘             │ │ │
│  │  │                                          │ │ │
│  │  │  NodePort: 31281 → vlinsert:9481       │ │ │
│  │  └──────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

## 🧩 Componentes

### 1. Windows Server 2012 R2 Container
- **Imagem**: `dockurr/windows`
- **Versão**: Windows Server 2012 R2
- **Recursos**:
  - RAM: 8GB
  - CPU: 4 cores
  - Disco: 80GB
- **Portas expostas**:
  - `8006`: Interface web de gerenciamento
  - `3389`: RDP (Remote Desktop)
  - `2222`: SSH para PowerShell remoting

### 2. OpenTelemetry Collector
- **Versão**: 0.88.0 (contrib)
- **Localização**: `C:\OpenTelemetry\` (dentro do Windows)
- **Serviço**: `otelcol` (auto-start com recovery)
- **Receivers**: Windows Event Logs (Application, System, Security)
- **Processors**: Resource detection, attributes, batch
- **Exporter**: OTLP/HTTP para VictoriaLogs
- **Porta Telemetria**: 8888

### 3. VictoriaLogs Cluster (K3S)
- **Helm Chart**: `victoria-logs-cluster`
- **Namespace**: `logging`
- **Componentes**:
  - **vlinsert**: Ingestão de logs (2 replicas)
    - Port: 9481 (interno), 31281 (NodePort)
  - **vlstorage**: Armazenamento persistente (2 pods)
    - Persistent Volumes (20Gi cada)
    - Retenção: 7 dias
  - **vlselect**: Consulta de logs (2 replicas)
    - Port: 9471
    - Interface VMUI disponível

## 📁 Estrutura de Diretórios

```
/home/helio/sf/lab/win/
├── docker-compose.yaml               # Docker Compose (Windows Server)
├── README.md                         # Este arquivo
├── OTEL_INSTALL_WIN2012R2.md        # Guia de instalação OpenTelemetry
├── OTEL_CONFIGURACAO_ATUAL.md       # Configuração atual em produção
├── shared/                           # Pasta compartilhada com o Windows
│   └── (arquivos compartilhados)
└── win2012/                          # Storage persistente do Windows (VM disk)
```

### Documentação

| Arquivo | Descrição |
|---------|-----------|
| `README.md` | Overview geral do projeto |
| `OTEL_INSTALL_WIN2012R2.md` | Procedimento completo de instalação do OpenTelemetry 0.88.0 |
| `OTEL_CONFIGURACAO_ATUAL.md` | Configuração detalhada do ambiente em produção |

## 🚀 Como Usar

### 1. Iniciar Windows Server

```bash
cd /home/helio/sf/lab/win
docker-compose up -d
```

Aguarde alguns minutos para o Windows inicializar completamente.

### 2. Verificar VictoriaLogs no K3S

```bash
# Verificar se os pods estão rodando
kubectl get pods -n logging

# Verificar serviços
kubectl get svc -n logging

# Verificar o NodePort do vlinsert
kubectl get svc vlinsert-external -n logging
# OUTPUT: NodePort 31281
```

### 3. Acessar o Windows

**Via SSH:**
```bash
ssh -p 2222 docker@localhost
# Senha: admin
```

**Via RDP:**
```bash
# Conectar em: localhost:3389
# Usuário: docker
# Senha: admin
```

### 4. Verificar OpenTelemetry

```bash
# Via SSH no Windows
ssh -p 2222 docker@localhost "sc.exe query otelcol"

# Verificar processo
ssh -p 2222 docker@localhost "tasklist | findstr otelcol"

# Ver métricas (do host Linux)
curl http://172.30.0.3:8888/metrics | grep -E "sent_log_records|queue"
```

### 5. Consultar Logs no VictoriaLogs

**Via Port-Forward:**
```bash
# Iniciar port-forward para vlselect
kubectl port-forward -n logging svc/vlc-victoria-logs-cluster-vlselect 9471:9471 &

# Acessar interface web
# http://localhost:9471/select/vmui/

# Queries via curl
curl 'http://localhost:9471/select/logsql/query?query=host.name:DOCKERW*'
```

**Via LogQL:**
```bash
# Logs de produção
curl 'http://localhost:9471/select/logsql/query?query=environment:production'

# Logs do canal Application
curl 'http://localhost:9471/select/logsql/query?query=channel:application'

# Logs de erro (Level 2)
curl 'http://localhost:9471/select/logsql/query?query=level:2'
```

## ⚙️ Configuração do OpenTelemetry Collector

O coletor está configurado para:

### Receivers
- **windowseventlog/application**: Canal Application (poll: 1s, max 100 logs)
- **windowseventlog/system**: Canal System (poll: 1s, max 100 logs)
- **windowseventlog/security**: Canal Security (poll: 1s, ignore errors)

### Processors
- **resourcedetection**: Detecção automática de hostname via OS
- **attributes**: Tags customizadas:
  - `environment: production`
  - `datacenter: dc1`
- **batch**: Batch de 8192 logs, timeout 200ms

### Exporters
- **otlphttp/victorialogs**: Envio via OTLP/HTTP com:
  - Endpoint: `http://192.168.100.12:31281/insert/opentelemetry/v1/logs`
  - Compressão: gzip
  - Retry: Backoff exponencial (5s → 30s, max 5min)
  - Queue: 5000 logs, 10 workers
  - Header: `VL-Stream-Fields: "host,environment"`
- **debug**: Logs detalhados (5 primeiros, depois 1 a cada 200)

## 🎯 Objetivo do Projeto

Criar um ambiente de laboratório para:

1. **Executar Windows Server 2012 R2 em container** utilizando KVM/QEMU via Docker
2. **Coletar Windows Event Logs** usando OpenTelemetry Collector 0.88.0 (última versão compatível)
3. **Armazenar logs em cluster escalável** no VictoriaLogs rodando em K3S
4. **Testar integração OTLP/HTTP** entre Windows e VictoriaLogs Cluster
5. **Demonstrar arquitetura híbrida** com container Windows + K3S

## 🔌 Conectividade

```
Windows Container (172.30.0.3)
         ↓
Host Network Interface
         ↓
K3S NodePort (192.168.100.12:31281)
         ↓
K3S Service (vlinsert ClusterIP)
         ↓
VictoriaLogs vlinsert Pods
         ↓
VictoriaLogs vlstorage (Persistent)
```

## 🛑 Parar o Ambiente

### Windows Server
```bash
docker-compose down
```

### VictoriaLogs K3S
```bash
# Deletar NodePort externo
kubectl delete svc vlinsert-external -n logging

# Desinstalar Helm release (se necessário)
helm uninstall vlc -n logging

# Remover namespace (remove tudo)
kubectl delete namespace logging
```

## 📝 Notas Importantes

### Compatibilidade
- **OpenTelemetry 0.88.0** é a última versão que roda em Windows Server 2012 R2
- Versões 0.89+ usam Go 1.21 que não suporta este sistema operacional
- Use **apenas binário contrib** para ter o receiver `windowseventlog`

### Performance
- Windows Server leva **3-5 minutos** para inicializar completamente
- OpenTelemetry inicia automaticamente como serviço Windows
- Logs começam a fluir ~30 segundos após o serviço iniciar
- VictoriaLogs suporta **milhões de logs/segundo** com o cluster atual

### Armazenamento
- Windows VM: `./win2012/` (80GB, formato QCOW2)
- VictoriaLogs: Persistent Volumes no K3S (20Gi x 2, retenção 7 dias)
- Shared folder: `./shared/` acessível em `C:\shared` no Windows

### Rede
- Windows usa rede bridge Docker (172.30.0.0/16)
- K3S usa rede host do Linux (192.168.100.12)
- NodePort 31281 expõe vlinsert para o Windows
- Certifique-se de ter suporte a **KVM** habilitado no host Linux

## 🔗 Links Úteis

- [OpenTelemetry Docs](https://opentelemetry.io/docs/collector/)
- [VictoriaLogs Docs](https://docs.victoriametrics.com/victorialogs/)
- [Windows Event Log Receiver](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/windowseventlogreceiver)
- [K3S Docs](https://docs.k3s.io/)
- [Dockurr/Windows](https://github.com/dockur/windows)

---

**Status:** ✅ Operacional
**Última atualização:** 2025-10-09
**Ambiente:** Lab / Development
