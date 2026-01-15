# Full Stack Deployment - Victoria Metrics + InfranGen

Este diretório contém os manifestos para deploy completo da stack de observabilidade com Victoria Metrics e a aplicação InfranGen.

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    Namespace: monitoring                     │
│                                                              │
│  ┌──────────────┐      ┌─────────────────┐                 │
│  │  InfranGen   │─────▶│    VMAgent      │                 │
│  │  (metrics)   │      │   (scraper)     │                 │
│  └──────────────┘      └────────┬────────┘                 │
│                                  │                           │
│                                  ▼                           │
│                         ┌────────────────┐                  │
│                         │   VMCluster    │                  │
│                         │                │                  │
│                         │ ┌────────────┐ │                  │
│                         │ │ VMInsert   │ │                  │
│                         │ └────────────┘ │                  │
│                         │ ┌────────────┐ │                  │
│                         │ │ VMStorage  │ │                  │
│                         │ └────────────┘ │                  │
│                         │ ┌────────────┐ │                  │
│                         │ │ VMSelect   │ │                  │
│                         │ └────────────┘ │                  │
│                         └────────┬───────┘                  │
│                                  │                           │
│                                  ▼                           │
│                         ┌────────────────┐                  │
│                         │    Grafana     │                  │
│                         │  (dashboard)   │                  │
│                         └────────────────┘                  │
└─────────────────────────────────────────────────────────────┘
```

## 📦 Componentes

### Victoria Metrics Stack (via Helm)
- **VMCluster**: Cluster distribuído para armazenamento de métricas
  - VMInsert: Recebe e distribui métricas
  - VMStorage: Armazena métricas com replicação
  - VMSelect: Query engine para consultas
- **VMAgent**: Scraper Prometheus-compatible
- **Grafana**: Dashboards e visualização
- **AlertManager**: Gerenciamento de alertas
- **Kube-State-Metrics**: Métricas do cluster K8s
- **Node-Exporter**: Métricas dos nodes

### InfranGen (Aplicação Custom)
- Coleta métricas do sistema (CPU, memória, disco, rede)
- Expõe endpoint Prometheus `/metrics`
- VMServiceScrape para integração automática

## 🚀 Deploy Rápido

### Opção 1: Usando Makefile (Recomendado)

```bash
# Deploy completo da stack
make fullstack-deploy

# Ver logs
make fullstack-logs

# Acessar Grafana
make fullstack-grafana

# Acessar VMSelect (query metrics)
make fullstack-vmselect

# Remover tudo
make fullstack-clean
```

### Opção 2: Script Manual

```bash
# Deploy via Helm
./deploy-fullstack-helm.sh

# Limpar
helm uninstall vmstack -n monitoring
kubectl delete -f kubernetes/fullstack_application/04-system-metrics-collector.yaml
kubectl delete namespace monitoring
```

## 📊 Acessando os Serviços

### Grafana Dashboard

```bash
# Port forward
kubectl port-forward -n monitoring svc/vmstack-grafana 3000:80

# Acessar: http://localhost:3000
# User: admin
# Password:
kubectl get secret -n monitoring vmstack-grafana -o jsonpath='{.data.admin-password}' | base64 -d
```

### VMSelect (Query Metrics)

```bash
# Port forward
kubectl port-forward -n monitoring svc/vmselect-vmstack-victoria-metrics-k8s-stack 8481:8481

# Queries de exemplo:
curl 'http://localhost:8481/select/0/prometheus/api/v1/query?query=up'
curl 'http://localhost:8481/select/0/prometheus/api/v1/query?query=system_cpu_percent'
curl 'http://localhost:8481/select/0/prometheus/api/v1/query?query=system_memory_percent'
```

### InfranGen Metrics

```bash
# Port forward
kubectl port-forward -n monitoring svc/system-metrics-collector 8000:8000

# Ver métricas raw
curl http://localhost:8000/metrics

# Health check
curl http://localhost:8000/health
```

## 🔍 Verificação e Debug

### Verificar status dos recursos

```bash
# Helm releases
helm list -n monitoring

# Pods
kubectl get pods -n monitoring

# Services
kubectl get svc -n monitoring

# VMServiceScrapes (scrape configs)
kubectl get vmservicescrape -n monitoring

# VMAgent targets
kubectl port-forward -n monitoring svc/vmagent-vmstack-victoria-metrics-k8s-stack 8429:8429
# Acessar: http://localhost:8429/targets
```

### Logs

```bash
# InfranGen
kubectl logs -f -n monitoring -l app=system-metrics-collector

# VMAgent
kubectl logs -f -n monitoring -l app.kubernetes.io/name=vmagent

# VMSelect
kubectl logs -f -n monitoring -l app.kubernetes.io/name=vmselect

# Grafana
kubectl logs -f -n monitoring -l app.kubernetes.io/name=grafana
```

## 🎯 Queries Úteis no Grafana/VMSelect

### Métricas do Sistema (InfranGen)

```promql
# CPU usage
system_cpu_percent

# Memory usage
system_memory_percent

# Disk usage
system_disk_percent{mountpoint="/"}

# Network bytes sent
rate(system_network_bytes_sent[5m])

# Network bytes received
rate(system_network_bytes_received[5m])
```

### Métricas do Kubernetes

```promql
# Pods running
kube_pod_status_phase{phase="Running"}

# Node CPU usage
1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) by (instance)

# Node memory usage
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100

# Container restarts
rate(kube_pod_container_status_restarts_total[5m])
```

## ⚙️ Configuração

### Customizar valores do Helm

Edite o arquivo: `kubernetes/victoria_metrics/vmstack/vmstack-values.yaml`

```yaml
# Exemplo: Alterar retenção de dados
vmcluster:
  spec:
    retentionPeriod: "30d"  # Aumentar para 30 dias

# Exemplo: Habilitar Alertmanager
alertmanager:
  enabled: true
  config:
    route:
      receiver: slack
    receivers:
    - name: slack
      slack_configs:
      - api_url: YOUR_SLACK_WEBHOOK_URL
        channel: '#alerts'
```

### Customizar InfranGen

Edite o ConfigMap em: `kubernetes/fullstack_application/04-system-metrics-collector.yaml`

```yaml
data:
  METRICS_INTERVAL_SECONDS: "30"  # Coletar a cada 30s
  COLLECT_NETWORK_METRICS: "true"  # Habilitar métricas de rede
  LOG_LEVEL: "DEBUG"  # Mais detalhes nos logs
```

## 🔐 Persistência de Dados

### VMStorage (dados das métricas)

```bash
# Ver PVCs
kubectl get pvc -n monitoring

# Aumentar storage (editar PVC)
kubectl edit pvc vmstorage-vmcluster-persistent-vmstack-victoria-metrics-k8s-stack-0 -n monitoring
```

### Grafana (dashboards)

```bash
# Backup de dashboards
kubectl get configmap -n monitoring -l grafana_dashboard=1 -o yaml > grafana-dashboards-backup.yaml

# Restore
kubectl apply -f grafana-dashboards-backup.yaml
```

## 🐛 Troubleshooting

### Métricas não aparecem no Grafana

1. Verificar se VMAgent está scrapando:
   ```bash
   kubectl port-forward -n monitoring svc/vmagent-vmstack-victoria-metrics-k8s-stack 8429:8429
   # Abrir: http://localhost:8429/targets
   ```

2. Verificar VMServiceScrape:
   ```bash
   kubectl get vmservicescrape -n monitoring system-metrics-collector -o yaml
   ```

3. Verificar logs do VMAgent:
   ```bash
   kubectl logs -n monitoring -l app.kubernetes.io/name=vmagent | grep -i error
   ```

### Pods crashando

```bash
# Verificar eventos
kubectl get events -n monitoring --sort-by='.lastTimestamp'

# Descrever pod com problema
kubectl describe pod -n monitoring <pod-name>

# Ver logs anteriores (se pod reiniciou)
kubectl logs -n monitoring <pod-name> --previous
```

### Storage cheio

```bash
# Ver uso de storage
kubectl exec -n monitoring vmselect-vmcluster-persistent-vmstack-victoria-metrics-k8s-stack-0 -- df -h

# Reduzir retenção (editar VMCluster)
kubectl edit vmcluster -n monitoring vmcluster
# Alterar: retentionPeriod: "7d"
```

## 📚 Recursos Adicionais

- [Victoria Metrics Docs](https://docs.victoriametrics.com/)
- [VMAgent Configuration](https://docs.victoriametrics.com/vmagent.html)
- [PromQL Query Examples](https://prometheus.io/docs/prometheus/latest/querying/examples/)
- [Grafana Dashboards](https://grafana.com/grafana/dashboards/)

## 🔄 Atualizações

### Atualizar Victoria Metrics Stack

```bash
# Atualizar repo Helm
helm repo update vm

# Upgrade release
helm upgrade vmstack vm/victoria-metrics-k8s-stack \
  -n monitoring \
  -f kubernetes/victoria_metrics/vmstack/vmstack-values.yaml
```

### Atualizar InfranGen

```bash
# Rebuild imagem
docker build -t infragen:latest .

# Importar para K3s
docker save infragen:latest -o /tmp/infragen.tar
sudo k3s ctr images import /tmp/infragen.tar

# Restart pods
kubectl rollout restart deployment -n monitoring system-metrics-collector
```
