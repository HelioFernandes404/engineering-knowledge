# Instalação OpenTelemetry Collector 0.88.0 - Windows Server 2012 R2

## 📌 Contexto e Compatibilidade

### Por que versão 0.88.0?

**Windows Server 2012 R2 requer OpenTelemetry Collector versão 0.88.0 ou anterior.**

- **Go 1.21+** exige Windows 10/Server 2016+
- **Go 1.20** é a última versão compatível com Server 2012 R2
- OpenTelemetry Collector migrou para **Go 1.21 a partir da versão 0.89+**
- **Versões 0.89+** não funcionarão no Server 2012 R2

### Requisitos do Sistema

- Windows Server 2012 R2
- 7-Zip instalado (para extrair .tar.gz)
- TLS 1.2 habilitado
- Acesso de Administrador

---

## 🔧 Pré-requisitos

### 1. Habilitar TLS 1.2

O Windows Server 2012 R2 usa TLS 1.0/1.1 por padrão. Habilite TLS 1.2:

```powershell
# Habilitar TLS 1.2 para .NET Framework
[Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12

# Habilitar globalmente (requer reboot)
Set-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\.NETFramework\v4.0.30319' -Name 'SchUseStrongCrypto' -Value 1 -Type DWord
Set-ItemProperty -Path 'HKLM:\SOFTWARE\Wow6432Node\Microsoft\.NETFramework\v4.0.30319' -Name 'SchUseStrongCrypto' -Value 1 -Type DWord
```

### 2. Instalar 7-Zip

Se não estiver instalado:

```powershell
# Download do instalador
Invoke-WebRequest -Uri "https://www.7-zip.org/a/7z2201-x64.exe" -OutFile "7z-installer.exe"

# Instalar
.\7z-installer.exe /S
```

---

## 📥 Instalação do OpenTelemetry Collector

### Passo 1: Download da Versão 0.88.0

```powershell
# Habilitar TLS 1.2 temporariamente na sessão
[Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12

# Baixar OpenTelemetry Collector Contrib 0.88.0
Invoke-WebRequest -Uri "https://github.com/open-telemetry/opentelemetry-collector-releases/releases/download/v0.88.0/otelcol-contrib_0.88.0_windows_amd64.tar.gz" -OutFile "C:\otelcol-contrib-0.88.0.tar.gz"
```

### Passo 2: Criar Diretório de Instalação

```cmd
mkdir C:\OpenTelemetry
```

### Passo 3: Extrair com 7-Zip

```cmd
# Extrair arquivo .tar.gz (resulta em .tar)
"C:\Program Files\7-Zip\7z.exe" x C:\otelcol-contrib-0.88.0.tar.gz -oC:\OpenTelemetry -y

# Extrair arquivo .tar (resulta nos arquivos finais)
"C:\Program Files\7-Zip\7z.exe" x C:\OpenTelemetry\otelcol-contrib-0.88.0.tar -oC:\OpenTelemetry -y

# Limpar arquivos temporários
del C:\OpenTelemetry\*.tar
del C:\otelcol-contrib-0.88.0.tar.gz
```

### Passo 4: Verificar Extração

```cmd
dir C:\OpenTelemetry
```

**Arquivos esperados:**
- `otelcol-contrib.exe` - Executável principal
- `LICENSE` - Licença
- `README.md` - Documentação

---

## ⚙️ Configuração

### Criar arquivo config.yaml

Crie o arquivo `C:\OpenTelemetry\config.yaml` com o seguinte conteúdo:

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
  # Exporter para VictoriaLogs
  otlphttp/victorialogs:
    endpoint: http://10.0.0.50:9428/insert/opentelemetry/v1/logs
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

### Ajustar Configuração

**Alterar endpoint do VictoriaLogs:**
```yaml
endpoint: http://SEU_IP:9428/insert/opentelemetry/v1/logs
```

**Ajustar atributos customizados:**
```yaml
attributes:
  actions:
    - key: environment
      value: seu_ambiente  # production, staging, development
      action: insert
    - key: datacenter
      value: seu_datacenter
      action: insert
```

---

## 🚀 Criar e Iniciar Serviço Windows

### Passo 1: Criar Serviço

```cmd
sc.exe create otelcol displayname="OpenTelemetry Collector" start=auto binPath="\"C:\OpenTelemetry\otelcol-contrib.exe\" --config \"C:\OpenTelemetry\config.yaml\""
```

**Parâmetros:**
- `otelcol` - Nome do serviço
- `displayname` - Nome exibido no Services
- `start=auto` - Inicia automaticamente com o Windows
- `binPath` - Caminho completo do executável com argumentos

### Passo 2: Adicionar Descrição

```cmd
sc.exe description otelcol "Coleta logs do Windows Event Viewer e envia para VictoriaLogs"
```

### Passo 3: Configurar Recovery Automático

```cmd
sc.exe failure otelcol reset=86400 actions=restart/5000/restart/5000/restart/5000
```

**Comportamento:**
- Reinicia automaticamente após 5 segundos se falhar
- Até 3 tentativas de restart
- Reset do contador de falhas após 24h (86400 segundos)

### Passo 4: Iniciar Serviço

```cmd
sc.exe start otelcol
```

### Passo 5: Verificar Status

```cmd
sc.exe query otelcol
```

**Saída esperada:**
```
SERVICE_NAME: otelcol
        TYPE               : 10  WIN32_OWN_PROCESS
        STATE              : 4  RUNNING
        WIN32_EXIT_CODE    : 0  (0x0)
        SERVICE_EXIT_CODE  : 0  (0x0)
```

---

## ✅ Verificação da Instalação

### 1. Verificar Processo Rodando

```cmd
tasklist | findstr otelcol
```

**Saída esperada:**
```
otelcol-contrib.exe           1020 Services                   0    113,580 K
```

### 2. Verificar Porta de Telemetria

```cmd
netstat -ano | findstr 8888
```

**Saída esperada:**
```
TCP    0.0.0.0:8888           0.0.0.0:0              LISTENING       1020
TCP    [::]:8888              [::]:0                 LISTENING       1020
```

### 3. Verificar Event Log

```cmd
wevtutil qe Application /c:5 /rd:true /f:text /q:"*[System[Provider[@Name='otelcol']]]"
```

Deve mostrar eventos do OpenTelemetry Collector.

### 4. Verificar Configuração do Serviço

```cmd
sc.exe qc otelcol
```

---

## 🔍 Troubleshooting

### Serviço não inicia

**1. Testar execução manual:**
```cmd
cd C:\OpenTelemetry
otelcol-contrib.exe --config config.yaml
```

Se houver erro de configuração, será exibido no console.

**2. Verificar logs de erro:**
```cmd
wevtutil qe System /c:20 /rd:true /f:text /q:"*[System[Provider[@Name='Service Control Manager'] and EventID=7023]]"
```

**3. Verificar sintaxe do config.yaml:**
- Use editor com syntax highlighting
- Verifique indentação (deve ser espaços, não tabs)
- Valide YAML online: https://www.yamllint.com/

### Processo consome muita memória

**Ajustar batch processor:**
```yaml
batch:
  send_batch_size: 4096  # Reduzir de 8192
  timeout: 500ms         # Aumentar timeout
  send_batch_max_size: 5000
```

### Logs não chegam no VictoriaLogs

**1. Verificar conectividade:**
```powershell
Test-NetConnection -ComputerName 10.0.0.50 -Port 9428
```

**2. Habilitar debug temporariamente:**
```yaml
service:
  telemetry:
    logs:
      level: debug  # Mudar de info para debug
```

**3. Verificar debug exporter:**
O debug exporter mostra os logs sendo coletados. Se aparecerem no debug mas não no VictoriaLogs, o problema é no exporter/rede.

### Serviço para após algum tempo

**Verificar Event Log:**
```cmd
wevtutil qe System /c:10 /rd:true /f:text /q:"*[System[Provider[@Name='Service Control Manager']]]"
```

**Aumentar queue size:**
```yaml
sending_queue:
  queue_size: 10000  # Aumentar de 5000
```

---

## 🛠️ Gerenciamento do Serviço

### Comandos Úteis

```cmd
# Parar serviço
sc.exe stop otelcol

# Iniciar serviço
sc.exe start otelcol

# Reiniciar serviço (parar + iniciar)
sc.exe stop otelcol && timeout /t 2 /nobreak && sc.exe start otelcol

# Verificar status
sc.exe query otelcol

# Ver configuração
sc.exe qc otelcol

# Remover serviço
sc.exe stop otelcol
sc.exe delete otelcol
```

### Atualizar Configuração

```cmd
# 1. Editar config.yaml
notepad C:\OpenTelemetry\config.yaml

# 2. Validar sintaxe (execução manual)
cd C:\OpenTelemetry
otelcol-contrib.exe --config config.yaml
# Pressione Ctrl+C para parar após validar

# 3. Reiniciar serviço para aplicar
sc.exe stop otelcol
timeout /t 2 /nobreak
sc.exe start otelcol
```

---

## 📊 Monitoramento

### Métricas Internas

O OpenTelemetry Collector expõe suas próprias métricas na porta 8888:

```powershell
# Via PowerShell
Invoke-WebRequest -Uri "http://localhost:8888/metrics" | Select-Object -ExpandProperty Content

# Via navegador
http://localhost:8888/metrics
```

### Principais Métricas

```
# Logs recebidos
otelcol_receiver_accepted_log_records_total

# Logs enviados com sucesso
otelcol_exporter_sent_log_records_total

# Logs em queue
otelcol_exporter_queue_size

# Erros de envio
otelcol_exporter_send_failed_log_records_total
```

### Health Check

```powershell
# Verificar se está respondendo
Invoke-WebRequest -Uri "http://localhost:8888/metrics" -UseBasicParsing
```

Se retornar HTTP 200, o serviço está saudável.

---

## 🔄 Desinstalação Completa

```cmd
# 1. Parar serviço
sc.exe stop otelcol

# 2. Remover serviço
sc.exe delete otelcol

# 3. Matar processos remanescentes
taskkill /F /IM otelcol-contrib.exe

# 4. Remover arquivos
rmdir /S /Q "C:\OpenTelemetry"

# 5. Verificar remoção
sc.exe query otelcol
# Deve retornar erro 1060 (serviço não existe)
```

---

## 📚 Referências

- [OpenTelemetry Collector Documentation](https://opentelemetry.io/docs/collector/)
- [OpenTelemetry Releases](https://github.com/open-telemetry/opentelemetry-collector-releases/releases)
- [Windows Event Log Receiver](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/windowseventlogreceiver)
- [OTLP HTTP Exporter](https://github.com/open-telemetry/opentelemetry-collector/tree/main/exporter/otlphttpexporter)
- [VictoriaLogs OTLP Documentation](https://docs.victoriametrics.com/victorialogs/data-ingestion/opentelemetry/)

---

## 📝 Notas Importantes

### Compatibilidade de Versões

| Versão OTEL | Go Version | Windows 2012 R2 | Windows 2016+ |
|-------------|------------|-----------------|---------------|
| ≤ 0.88.0    | Go 1.20    | ✅ Compatível   | ✅ Compatível |
| ≥ 0.89.0    | Go 1.21+   | ❌ Incompatível | ✅ Compatível |

### Segurança

**⚠️ Atenção:** A configuração usa `insecure: true` no TLS para simplificar setup inicial. **Em produção, configure TLS adequadamente:**

```yaml
exporters:
  otlphttp/victorialogs:
    endpoint: https://victorialogs.exemplo.com:9428/insert/opentelemetry/v1/logs
    tls:
      insecure: false
      cert_file: /path/to/cert.pem
      key_file: /path/to/key.pem
      ca_file: /path/to/ca.pem
```

### Performance

**Configurações para ambientes de alto volume:**

```yaml
processors:
  batch:
    send_batch_size: 16384
    timeout: 1s
    send_batch_max_size: 20000

exporters:
  otlphttp/victorialogs:
    sending_queue:
      num_consumers: 20  # Aumentar workers
      queue_size: 20000  # Aumentar buffer
```

### Backup de Configuração

Sempre faça backup do `config.yaml` antes de modificar:

```cmd
copy C:\OpenTelemetry\config.yaml C:\OpenTelemetry\config.yaml.bak
```

---

## ✅ Checklist de Instalação

- [ ] TLS 1.2 habilitado
- [ ] 7-Zip instalado
- [ ] OpenTelemetry 0.88.0 baixado
- [ ] Arquivos extraídos em `C:\OpenTelemetry`
- [ ] `config.yaml` criado e customizado
- [ ] Endpoint do VictoriaLogs configurado
- [ ] Serviço Windows criado
- [ ] Descrição e recovery configurados
- [ ] Serviço iniciado com sucesso
- [ ] Processo verificado em `tasklist`
- [ ] Porta 8888 listening verificada
- [ ] Logs aparecendo no Event Viewer
- [ ] Conectividade com VictoriaLogs testada
- [ ] Métricas acessíveis em `localhost:8888/metrics`

---

**Documento gerado em:** 2025-10-09
**Versão OpenTelemetry:** 0.88.0
**Sistema Operacional:** Windows Server 2012 R2
**Status:** ✅ Testado e Funcionando
