# Configuração OpenTelemetry Collector - Ambiente Atual

## 📋 Informações do Ambiente

### Sistema Operacional
- **OS:** Windows Server 2012 R2
- **Hostname:** DOCKERW-TT38U0P
- **IP:** 172.30.0.3
- **Acesso SSH:** `ssh -p 2222 docker@localhost` (senha: admin)

### OpenTelemetry Collector
- **Versão:** 0.88.0 (contrib)
- **Diretório:** `C:\OpenTelemetry`
- **Executável:** `C:\OpenTelemetry\otelcol-contrib.exe`
- **Configuração:** `C:\OpenTelemetry\config.yaml`

### VictoriaLogs (K3S Cluster)
- **Cluster:** K3S local (192.168.100.12)
- **Namespace:** logging
- **Helm Chart:** victoria-logs-cluster
- **vlinsert Service:** ClusterIP 10.43.23.201:9481
- **NodePort Externo:** 31281
- **Endpoint OTLP:** `http://192.168.100.12:31281/insert/opentelemetry/v1/logs`
- **Replicas:** 2 (vlinsert, vlselect, vlstorage)

---

## 🚀 Processo de Instalação Realizado

### 1. Preparação do Ambiente

```powershell
# Habilitar TLS 1.2 para download
[Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12
```

### 2. Download da Versão 0.88.0

```powershell
# Download do binário contrib compatível com Server 2012 R2
Invoke-WebRequest -Uri "https://github.com/open-telemetry/opentelemetry-collector-releases/releases/download/v0.88.0/otelcol-contrib_0.88.0_windows_amd64.tar.gz" -OutFile "C:\otelcol-contrib-0.88.0.tar.gz"
```

**Motivo da versão 0.88.0:**
- Última versão compilada com Go 1.20
- Versões 0.89+ usam Go 1.21 que não suporta Windows Server 2012 R2

### 3. Criação do Diretório

```cmd
mkdir C:\OpenTelemetry
```

### 4. Extração com 7-Zip

```cmd
# Extrair .tar.gz para .tar
"C:\Program Files\7-Zip\7z.exe" x C:\otelcol-contrib-0.88.0.tar.gz -oC:\OpenTelemetry -y

# Extrair .tar para arquivos finais
"C:\Program Files\7-Zip\7z.exe" x C:\OpenTelemetry\otelcol-contrib-0.88.0.tar -oC:\OpenTelemetry -y

# Limpeza
del C:\OpenTelemetry\*.tar
del C:\otelcol-contrib-0.88.0.tar.gz
```

### 5. Criação do Arquivo de Configuração

Arquivo criado em `C:\OpenTelemetry\config.yaml` com a configuração abaixo.

### 6. Registro como Serviço Windows

```cmd
# Criar serviço
sc.exe create otelcol displayname="OpenTelemetry Collector" start=auto binPath="\"C:\OpenTelemetry\otelcol-contrib.exe\" --config \"C:\OpenTelemetry\config.yaml\""

# Adicionar descrição
sc.exe description otelcol "Coleta logs do Windows Event Viewer e envia para VictoriaLogs"

# Configurar recovery automático
sc.exe failure otelcol reset=86400 actions=restart/5000/restart/5000/restart/5000

# Iniciar serviço
sc.exe start otelcol
```

---

## ⚙️ Configuração Atual (config.yaml)

```yaml
receivers:
  # Coletar do Event Viewer - Application
  windowseventlog/application:
    channel: application
    start_at: end
    poll_interval: 1s
    max_reads: 100

  # Coletar do Event Viewer - System
  windowseventlog/system:
    channel: system
    start_at: end
    poll_interval: 1s
    max_reads: 100

  # Coletar do Event Viewer - Security
  windowseventlog/security:
    channel: security
    start_at: end
    poll_interval: 1s

processors:
  # Detecção automática de recursos do sistema
  resourcedetection:
    detectors: [system]
    system:
      hostname_sources: ["os"]

  # Adicionar atributos customizados
  attributes:
    actions:
      - key: environment
        value: production
        action: insert
      - key: datacenter
        value: dc1
        action: insert

  # Batch processor - essencial para performance
  batch:
    send_batch_size: 8192
    timeout: 200ms
    send_batch_max_size: 10000

exporters:
  # Exporter para VictoriaLogs no K3S
  otlphttp/victorialogs:
    logs_endpoint: http://192.168.100.12:31281/insert/opentelemetry/v1/logs
    compression: gzip
    tls:
      insecure: true
    headers:
      VL-Stream-Fields: "host,environment"
    retry_on_failure:
      enabled: true
      initial_interval: 5s
      max_interval: 30s
      max_elapsed_time: 300s
    sending_queue:
      enabled: true
      num_consumers: 10
      queue_size: 5000

  # Debug exporter para troubleshooting (opcional)
  debug:
    verbosity: detailed
    sampling_initial: 5
    sampling_thereafter: 200

service:
  pipelines:
    logs:
      receivers: [windowseventlog/application, windowseventlog/system, windowseventlog/security]
      processors: [resourcedetection, attributes, batch]
      exporters: [otlphttp/victorialogs, debug]

  telemetry:
    logs:
      level: info
```

---

## 📊 Status Atual do Serviço

### Informações do Serviço

```
SERVICE_NAME: otelcol
TYPE: WIN32_OWN_PROCESS
STATE: RUNNING
START_TYPE: AUTO_START
BINARY_PATH: "C:\OpenTelemetry\otelcol-contrib.exe" --config "C:\OpenTelemetry\config.yaml"
SERVICE_START_NAME: LocalSystem
```

### Processo em Execução

```
Nome: otelcol-contrib.exe
PID: 1020
Memória: ~113 MB
Status: Running
```

### Portas em Uso

```
Porta 8888 (Telemetria/Métricas)
- TCP 0.0.0.0:8888 LISTENING
- TCP [::]:8888 LISTENING
```

---

## 🔄 Pipeline de Dados Configurado

### Fluxo de Logs

```
┌─────────────────────────────────────────────────┐
│         Windows Event Viewer                     │
│  ┌───────────┐ ┌────────┐ ┌──────────┐         │
│  │Application│ │ System │ │ Security │         │
│  └─────┬─────┘ └────┬───┘ └────┬─────┘         │
└────────┼────────────┼──────────┼───────────────┘
         │            │          │
         ▼            ▼          ▼
┌─────────────────────────────────────────────────┐
│      OpenTelemetry Receivers                     │
│  windowseventlog/application                     │
│  windowseventlog/system                          │
│  windowseventlog/security                        │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│      Processors (Pipeline)                       │
│  1. resourcedetection → Adiciona hostname        │
│  2. attributes → Adiciona environment, datacenter│
│  3. batch → Agrupa em batches de 8192            │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│      Exporters                                   │
│  ┌─────────────────────────────────────┐        │
│  │ otlphttp/victorialogs               │        │
│  │ → http://10.0.0.50:9428             │        │
│  │ → Compression: gzip                 │        │
│  │ → Queue: 5000 logs                  │        │
│  │ → Retry: Habilitado                 │        │
│  └─────────────────────────────────────┘        │
│  ┌─────────────────────────────────────┐        │
│  │ debug (para troubleshooting)        │        │
│  └─────────────────────────────────────┘        │
└─────────────────────────────────────────────────┘
```

---

## 🎯 Detalhamento das Configurações

### Receivers (Coletores)

#### windowseventlog/application
- **Canal:** Application Event Log
- **Início:** `end` (somente novos logs, não histórico)
- **Intervalo:** Verifica a cada 1 segundo
- **Batch:** Lê até 100 logs por verificação

#### windowseventlog/system
- **Canal:** System Event Log
- **Início:** `end` (somente novos logs)
- **Intervalo:** Verifica a cada 1 segundo
- **Batch:** Lê até 100 logs por verificação

#### windowseventlog/security
- **Canal:** Security Event Log
- **Início:** `end` (somente novos logs)
- **Intervalo:** Verifica a cada 1 segundo
- **Observação:** Pode requerer privilégios administrativos elevados

### Processors (Processadores)

#### 1. resourcedetection
**Função:** Adiciona informações do sistema automaticamente

**Campos adicionados:**
- `host.name`: Nome do servidor (DOCKERW-TT38U0P)
- `os.type`: windows
- `os.description`: Windows Server 2012 R2

#### 2. attributes
**Função:** Adiciona metadados customizados aos logs

**Atributos adicionados:**
- `environment`: production
- `datacenter`: dc1

**Propósito:** Facilitar filtragem e agregação no VictoriaLogs

#### 3. batch
**Função:** Agrupa logs em batches para envio eficiente

**Configuração:**
- **send_batch_size:** 8192 logs (envia quando atingir esse número)
- **timeout:** 200ms (envia se passar esse tempo, mesmo sem completar batch)
- **send_batch_max_size:** 10000 logs (limite máximo de segurança)

**Benefícios:**
- Reduz overhead de rede
- Melhora throughput
- Diminui latência de processamento

### Exporters (Exportadores)

#### otlphttp/victorialogs

**Endpoint:**
```
http://10.0.0.50:9428/insert/opentelemetry/v1/logs
```

**Compressão:**
- **Tipo:** gzip
- **Redução:** ~70-80% do tamanho dos dados

**TLS:**
- **insecure:** true (não valida certificados)
- ⚠️ **Atenção:** Trocar para `false` com certificados válidos em produção

**Headers Customizados:**
```yaml
VL-Stream-Fields: "host,environment"
```
Define quais campos identificam streams únicos no VictoriaLogs.

**Retry (Tentativas):**
- **Habilitado:** Sim
- **Intervalo inicial:** 5 segundos
- **Intervalo máximo:** 30 segundos
- **Tempo máximo total:** 300 segundos (5 minutos)

**Comportamento:** Se falhar o envio, tenta novamente com backoff exponencial.

**Sending Queue (Fila de Envio):**
- **Habilitada:** Sim
- **Consumidores:** 10 workers paralelos
- **Tamanho:** 5000 logs em buffer

**Comportamento:** Se VictoriaLogs estiver lento ou indisponível, mantém logs em memória.

#### debug

**Função:** Exibe logs no console para troubleshooting

**Configuração:**
- **verbosity:** detailed (máximo detalhe)
- **sampling_initial:** 5 (mostra primeiros 5 logs completos)
- **sampling_thereafter:** 200 (depois mostra 1 a cada 200)

**Uso:** Útil para validar que logs estão sendo coletados.

---

## 🔍 Comandos de Gerenciamento

### Verificar Status

```cmd
# Status do serviço
sc.exe query otelcol

# Processo rodando
tasklist | findstr otelcol

# Porta de telemetria
netstat -ano | findstr 8888
```

### Controlar Serviço

```cmd
# Parar
sc.exe stop otelcol

# Iniciar
sc.exe start otelcol

# Reiniciar
sc.exe stop otelcol && timeout /t 2 /nobreak && sc.exe start otelcol
```

### Acessar via SSH

```bash
# Do host Linux/Mac
ssh -p 2222 docker@localhost
# Senha: admin

# Comandos Windows via SSH
ssh -p 2222 docker@localhost "sc.exe query otelcol"
ssh -p 2222 docker@localhost "tasklist | findstr otelcol"
```

### Visualizar Logs

```cmd
# Logs do OpenTelemetry no Event Viewer
wevtutil qe Application /c:10 /rd:true /f:text /q:"*[System[Provider[@Name='otelcol']]]"

# Logs de erro do Service Control Manager
wevtutil qe System /c:10 /rd:true /f:text /q:"*[System[Provider[@Name='Service Control Manager'] and EventID=7023]]"
```

### Acessar Métricas

```powershell
# Via PowerShell
Invoke-WebRequest -Uri "http://localhost:8888/metrics" | Select-Object -ExpandProperty Content

# Via curl (se instalado)
curl http://localhost:8888/metrics

# Via navegador
# http://172.30.0.3:8888/metrics
```

---

## 📈 Métricas Importantes

### Receiver Metrics

```
# Total de logs recebidos do Event Viewer
otelcol_receiver_accepted_log_records_total{receiver="windowseventlog/application"}
otelcol_receiver_accepted_log_records_total{receiver="windowseventlog/system"}
otelcol_receiver_accepted_log_records_total{receiver="windowseventlog/security"}

# Logs recusados/com erro
otelcol_receiver_refused_log_records_total
```

### Processor Metrics

```
# Logs processados pelo batch processor
otelcol_processor_batch_batch_send_size_bucket
otelcol_processor_batch_timeout_trigger_send_total
```

### Exporter Metrics

```
# Logs enviados com sucesso ao VictoriaLogs
otelcol_exporter_sent_log_records_total{exporter="otlphttp/victorialogs"}

# Falhas de envio
otelcol_exporter_send_failed_log_records_total{exporter="otlphttp/victorialogs"}

# Tamanho da queue
otelcol_exporter_queue_size{exporter="otlphttp/victorialogs"}

# Capacidade da queue
otelcol_exporter_queue_capacity{exporter="otlphttp/victorialogs"}
```

### Verificar Saúde do Sistema

```bash
# Via SSH do Linux
curl -s http://172.30.0.3:8888/metrics | grep -E "accepted_log_records_total|sent_log_records_total|send_failed"
```

---

## 🔄 Modificar Configuração

### 1. Editar config.yaml

```cmd
# Via notepad
notepad C:\OpenTelemetry\config.yaml

# Via PowerShell ISE
powershell_ise C:\OpenTelemetry\config.yaml
```

### 2. Validar Sintaxe

```cmd
# Testar execução manual
cd C:\OpenTelemetry
otelcol-contrib.exe --config config.yaml
```

Se houver erro, será exibido no console. Pressione **Ctrl+C** para parar.

### 3. Aplicar Mudanças

```cmd
# Reiniciar serviço
sc.exe stop otelcol
timeout /t 2 /nobreak
sc.exe start otelcol

# Verificar se iniciou corretamente
sc.exe query otelcol
```

### 4. Verificar Logs

```cmd
# Verificar últimos logs do serviço
wevtutil qe Application /c:5 /rd:true /f:text /q:"*[System[Provider[@Name='otelcol']]]"
```

---

## 🎨 Customizações Aplicadas

### Atributos Customizados

Os seguintes atributos são adicionados a **todos** os logs:

| Atributo    | Valor      | Origem                  |
|-------------|------------|-------------------------|
| environment | production | attributes processor    |
| datacenter  | dc1        | attributes processor    |
| host.name   | DOCKERW... | resourcedetection       |
| os.type     | windows    | resourcedetection       |

**Benefício:** Facilita filtragem no VictoriaLogs:
```
# Buscar logs de produção
environment:production

# Buscar logs deste host
host.name:DOCKERW-TT38U0P

# Buscar logs Windows de produção no DC1
os.type:windows AND environment:production AND datacenter:dc1
```

### VictoriaLogs Stream Fields

```yaml
headers:
  VL-Stream-Fields: "host,environment"
```

**Significado:** VictoriaLogs criará streams separados para cada combinação de:
- `host.name` (servidor)
- `environment` (ambiente)

**Resultado:**
- Stream 1: `host=DOCKERW-TT38U0P, environment=production`

Isso otimiza queries e compressão no VictoriaLogs.

---

## 🚨 Troubleshooting Específico

### Problema: Serviço não inicia

```cmd
# 1. Verificar erro específico
wevtutil qe System /c:1 /rd:true /f:text /q:"*[System[Provider[@Name='Service Control Manager'] and EventID=7023]]"

# 2. Testar manualmente
cd C:\OpenTelemetry
otelcol-contrib.exe --config config.yaml
```

**Erros comuns:**
- Sintaxe YAML incorreta
- Arquivo config.yaml não encontrado
- Porta 8888 já em uso

### Problema: Logs não chegam no VictoriaLogs

```powershell
# 1. Verificar conectividade
Test-NetConnection -ComputerName 10.0.0.50 -Port 9428

# 2. Verificar métricas de envio
Invoke-WebRequest -Uri "http://localhost:8888/metrics" | Select-String "exporter_sent_log_records_total"

# 3. Verificar erros de envio
Invoke-WebRequest -Uri "http://localhost:8888/metrics" | Select-String "send_failed"
```

**Se send_failed > 0:**
- VictoriaLogs pode estar offline
- Firewall bloqueando conexão
- Endpoint incorreto no config.yaml

### Problema: Alta utilização de memória

```cmd
# Verificar tamanho da queue
curl http://localhost:8888/metrics | findstr queue_size
```

**Se queue_size próximo de 5000:**
- VictoriaLogs não está processando rápido o suficiente
- Aumentar `queue_size` no config.yaml
- Ou aumentar `num_consumers` para processar mais rápido

**Ajuste:**
```yaml
sending_queue:
  num_consumers: 20  # Aumentar de 10 para 20
  queue_size: 10000  # Aumentar de 5000 para 10000
```

### Problema: Logs do Security channel não aparecem

**Causa:** Falta de permissões para ler Security Event Log.

**Solução:**
```cmd
# 1. Verificar se serviço roda como LocalSystem
sc.exe qc otelcol
# SERVICE_START_NAME deve ser LocalSystem

# 2. Se necessário, mudar para NetworkService ou criar conta dedicada
sc.exe config otelcol obj= "NT AUTHORITY\NetworkService"
```

Ou adicionar `ignore_errors: true` no receiver:
```yaml
windowseventlog/security:
  channel: security
  start_at: end
  ignore_errors: true  # Não falha se não tiver acesso
```

---

## 📦 Backup da Configuração

### Criar Backup Manual

```cmd
# Backup da configuração
copy C:\OpenTelemetry\config.yaml C:\OpenTelemetry\config.yaml.backup

# Com timestamp
copy C:\OpenTelemetry\config.yaml C:\OpenTelemetry\config.yaml.%date:~-4,4%%date:~-10,2%%date:~-7,2%
```

### Restaurar Backup

```cmd
# Parar serviço
sc.exe stop otelcol

# Restaurar configuração
copy C:\OpenTelemetry\config.yaml.backup C:\OpenTelemetry\config.yaml

# Iniciar serviço
sc.exe start otelcol
```

---

## 🔐 Segurança

### Permissões de Arquivos

```cmd
# Verificar permissões
icacls C:\OpenTelemetry

# Ajustar permissões (apenas administradores e sistema)
icacls C:\OpenTelemetry /inheritance:r
icacls C:\OpenTelemetry /grant:r "SYSTEM:(OI)(CI)F"
icacls C:\OpenTelemetry /grant:r "Administrators:(OI)(CI)F"
```

### Conta de Serviço

**Atual:** LocalSystem (máximo privilégio)

**Alternativas mais seguras:**
- NetworkService (privilégios reduzidos)
- Conta dedicada com permissões mínimas

```cmd
# Mudar para NetworkService
sc.exe config otelcol obj= "NT AUTHORITY\NetworkService"
```

### TLS para VictoriaLogs

**⚠️ Importante:** Configuração atual usa `insecure: true`.

**Para produção, configurar TLS:**
```yaml
exporters:
  otlphttp/victorialogs:
    endpoint: https://10.0.0.50:9428/insert/opentelemetry/v1/logs
    tls:
      insecure: false
      cert_file: C:\OpenTelemetry\certs\client.crt
      key_file: C:\OpenTelemetry\certs\client.key
      ca_file: C:\OpenTelemetry\certs\ca.crt
```

---

## 📊 Integração com VictoriaLogs no K3S

### Arquitetura de Deployment

```
Windows Server (172.30.0.3)
     │
     │ OTLP/HTTP
     ▼
Host Network (192.168.100.12:31281) - NodePort
     │
     ▼
K3S Cluster - Namespace: logging
     │
     ├─ vlinsert (ClusterIP 10.43.23.201:9481)
     │      │
     │      ├─ Replica 1
     │      └─ Replica 2
     │
     ├─ vlstorage (Headless Service)
     │      │
     │      ├─ Pod 0 (Persistent Volume)
     │      └─ Pod 1 (Persistent Volume)
     │
     └─ vlselect (ClusterIP 10.43.154.91:9471)
            │
            ├─ Replica 1
            └─ Replica 2
```

### Endpoint Configurado

**Externo (Windows → K3S):**
```
http://192.168.100.12:31281/insert/opentelemetry/v1/logs
```

**Interno (Dentro do K3S):**
```
http://vlc-victoria-logs-cluster-vlinsert.logging.svc.cluster.local:9481/insert/opentelemetry/v1/logs
```

### Acessar VictoriaLogs

#### Via Port-Forward

```bash
# API de queries (vlselect)
kubectl port-forward -n logging svc/vlc-victoria-logs-cluster-vlselect 9471:9471

# Interface Web (VMUI)
# http://localhost:9471/select/vmui/
```

#### Via NodePort (Criar se necessário)

```bash
# Expor vlselect como NodePort para queries externas
kubectl expose service vlc-victoria-logs-cluster-vlselect --type=NodePort --name=vlselect-external --port=9471 -n logging

# Verificar porta atribuída
kubectl get svc vlselect-external -n logging
```

### Queries no VictoriaLogs

```bash
# Todos os logs deste Windows
kubectl port-forward -n logging svc/vlc-victoria-logs-cluster-vlselect 9471:9471 &
curl 'http://localhost:9471/select/logsql/query?query=host.name:DOCKERW-TT38U0P'

# Logs de produção
curl 'http://localhost:9471/select/logsql/query?query=environment:production'

# Logs do Event Viewer Application
curl 'http://localhost:9471/select/logsql/query?query=host.name:DOCKERW* AND channel:application'

# Logs de erro (Level 2)
curl 'http://localhost:9471/select/logsql/query?query=level:2'
```

### Verificar Ingestão

```bash
# Verificar pods
kubectl get pods -n logging

# Logs do vlinsert (verificar ingestão)
kubectl logs -n logging -l app=vlinsert --tail=50

# Logs do vlstorage (verificar armazenamento)
kubectl logs -n logging -l app=vlstorage --tail=50

# Métricas do vlinsert
kubectl port-forward -n logging svc/vlc-victoria-logs-cluster-vlinsert 9481:9481 &
curl 'http://localhost:9481/metrics' | grep vl_rows_ingested_total
```

### Gerenciamento do VictoriaLogs Cluster

```bash
# Status dos serviços
kubectl get svc -n logging

# Status dos pods
kubectl get pods -n logging -o wide

# Recursos (CPU/Memory)
kubectl top pods -n logging

# Descrever vlinsert
kubectl describe pod -n logging -l app=vlinsert

# Escalar vlinsert (se necessário mais throughput)
kubectl scale statefulset vlc-victoria-logs-cluster-vlinsert --replicas=3 -n logging
```

---

## 📝 Histórico de Mudanças

### 2025-10-09 - Migração para VictoriaLogs K3S
- ✅ VictoriaLogs removido do docker-compose local
- ✅ VictoriaLogs Cluster instalado no K3S (namespace: logging)
- ✅ Helm chart: victoria-logs-cluster com 2 replicas
- ✅ NodePort 31281 exposto para vlinsert
- ✅ OpenTelemetry reconfigurado para endpoint K3S (192.168.100.12:31281)
- ✅ Config.yaml atualizado com `logs_endpoint` (correção de path duplicado)
- ✅ Serviço OpenTelemetry reiniciado e validado

### 2025-10-09 - Instalação Inicial
- ✅ Instalado OpenTelemetry Collector 0.88.0
- ✅ Configurado receivers para Application, System, Security
- ✅ Configurado exporter para VictoriaLogs
- ✅ Registrado como serviço Windows (otelcol)
- ✅ Configurado recovery automático
- ✅ Iniciado e validado funcionamento

### Configurações Aplicadas
- Batch size: 8192 logs
- Queue size: 5000 logs
- Consumers: 10 workers
- Retry: Habilitado com backoff exponencial
- Compression: gzip
- Destino: VictoriaLogs K3S Cluster via NodePort

---

## ✅ Checklist de Validação

- [x] OpenTelemetry 0.88.0 instalado em `C:\OpenTelemetry`
- [x] Serviço Windows `otelcol` criado
- [x] Serviço configurado para auto-start
- [x] Recovery automático configurado
- [x] Serviço em estado RUNNING
- [x] Processo otelcol-contrib.exe ativo (PID 1020)
- [x] Porta 8888 listening (telemetria)
- [x] Receivers coletando de Application, System, Security
- [x] Exporter enviando para VictoriaLogs (10.0.0.50:9428)
- [x] Atributos customizados aplicados (environment, datacenter)
- [x] Debug exporter ativo para troubleshooting
- [x] Métricas acessíveis em http://localhost:8888/metrics

---

## 📞 Informações de Acesso

### Windows Server (SSH)
```bash
ssh -p 2222 docker@localhost
# Senha: admin
# IP: 172.30.0.3
```

### OpenTelemetry Métricas
```bash
# Interno (via SSH do Windows)
http://localhost:8888/metrics

# Externo (do host Linux)
http://172.30.0.3:8888/metrics
```

### VictoriaLogs K3S

**Interface Web (VMUI):**
```bash
# Port-forward vlselect
kubectl port-forward -n logging svc/vlc-victoria-logs-cluster-vlselect 9471:9471

# Acessar no navegador
http://localhost:9471/select/vmui/
```

**API de Ingestão (vlinsert):**
```bash
# Via NodePort (acesso externo)
http://192.168.100.12:31281/insert/opentelemetry/v1/logs

# Via Port-forward (acesso local)
kubectl port-forward -n logging svc/vlc-victoria-logs-cluster-vlinsert 9481:9481
http://localhost:9481/insert/opentelemetry/v1/logs
```

**API de Queries (vlselect):**
```bash
# Via Port-forward
kubectl port-forward -n logging svc/vlc-victoria-logs-cluster-vlselect 9471:9471
http://localhost:9471/select/logsql/query
```

### K3S Cluster
```bash
# Cluster Info
kubectl cluster-info

# Namespace logging
kubectl get all -n logging

# Logs dos pods
kubectl logs -n logging -l app=vlinsert --tail=50
kubectl logs -n logging -l app=vlselect --tail=50
kubectl logs -n logging -l app=vlstorage --tail=50
```

---

**Última atualização:** 2025-10-09
**Status:** ✅ Operacional
**Ambiente:** Lab / Development
**Responsável:** Helio
