# VictoriaLogs - Queries Úteis

Este documento contém queries úteis para consultar logs no VictoriaLogs.

## Acesso ao VictoriaLogs

- **URL**: http://localhost:9428
- **API Endpoint**: http://localhost:9428/select/logsql/query

## Queries Básicas

### Todos os logs da aplicação
```bash
curl 'http://localhost:9428/select/logsql/query' \
  -d 'query=app:system_metrics_collector'
```

### Filtrar por nível de log
```bash
# Apenas logs de INFO
curl 'http://localhost:9428/select/logsql/query' \
  -d 'query=app:system_metrics_collector level:INFO'

# Apenas erros
curl 'http://localhost:9428/select/logsql/query' \
  -d 'query=app:system_metrics_collector level:ERROR'

# Avisos e erros
curl 'http://localhost:9428/select/logsql/query' \
  -d 'query=app:system_metrics_collector (level:WARNING OR level:ERROR)'
```

### Filtrar por módulo/componente
```bash
# Logs do serviço de métricas
curl 'http://localhost:9428/select/logsql/query' \
  -d 'query=app:system_metrics_collector module:services'

# Logs do HTTP server
curl 'http://localhost:9428/select/logsql/query' \
  -d 'query=app:system_metrics_collector module:http_server_adapter'

# Logs do CLI adapter
curl 'http://localhost:9428/select/logsql/query' \
  -d 'query=app:system_metrics_collector module:cli_adapter'
```

### Filtrar por função específica
```bash
curl 'http://localhost:9428/select/logsql/query' \
  -d 'query=app:system_metrics_collector function:collect_metrics'
```

### Busca por texto na mensagem
```bash
# Logs que contêm "metrics"
curl 'http://localhost:9428/select/logsql/query' \
  -d 'query=app:system_metrics_collector _msg:*metrics*'

# Logs que contêm "error" ou "fail"
curl 'http://localhost:9428/select/logsql/query' \
  -d 'query=app:system_metrics_collector (_msg:*error* OR _msg:*fail*)'
```

## Queries Avançadas

### Filtrar por intervalo de tempo
```bash
# Últimas 5 minutos
curl 'http://localhost:9428/select/logsql/query' \
  -d 'query=app:system_metrics_collector _time:5m'

# Última 1 hora
curl 'http://localhost:9428/select/logsql/query' \
  -d 'query=app:system_metrics_collector _time:1h'

# Últimas 24 horas
curl 'http://localhost:9428/select/logsql/query' \
  -d 'query=app:system_metrics_collector _time:24h'
```

### Combinar múltiplos filtros
```bash
# Erros nos últimos 30 minutos
curl 'http://localhost:9428/select/logsql/query' \
  -d 'query=app:system_metrics_collector level:ERROR _time:30m'

# Logs do módulo services com nível INFO
curl 'http://localhost:9428/select/logsql/query' \
  -d 'query=app:system_metrics_collector module:services level:INFO'
```

### Formatação de saída com jq
```bash
# Formatar como JSON legível
curl 'http://localhost:9428/select/logsql/query' \
  -d 'query=app:system_metrics_collector' 2>/dev/null | jq '.'

# Mostrar apenas mensagem e timestamp
curl 'http://localhost:9428/select/logsql/query' \
  -d 'query=app:system_metrics_collector' 2>/dev/null | \
  jq -r '{time: ._time, level: .level, message: ._msg}'

# Últimos 10 logs
curl 'http://localhost:9428/select/logsql/query' \
  -d 'query=app:system_metrics_collector' 2>/dev/null | \
  jq -s '.[-10:]'

# Contar logs por nível
curl 'http://localhost:9428/select/logsql/query' \
  -d 'query=app:system_metrics_collector' 2>/dev/null | \
  jq -r '.level' | sort | uniq -c
```

## Campos Disponíveis

Os logs enviados para o VictoriaLogs contêm os seguintes campos:

- `_msg`: Mensagem do log
- `_time`: Timestamp no formato ISO8601
- `app`: Nome da aplicação (`system_metrics_collector`)
- `environment`: Ambiente (`production`, `development`, etc.)
- `level`: Nível do log (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`)
- `logger`: Nome completo do logger (ex: `src.domain.services`)
- `module`: Nome do módulo Python (ex: `services`)
- `function`: Nome da função que gerou o log
- `line`: Número da linha no código fonte

## Interface Web

Para uma interface mais amigável, considere usar:

- **VictoriaLogs UI**: http://localhost:9428/select/vmui
- Ou instale **Grafana** e configure o datasource do VictoriaLogs

## Referências

- [VictoriaLogs Documentation](https://docs.victoriametrics.com/victorialogs/)
- [LogsQL Query Language](https://docs.victoriametrics.com/victorialogs/logsql/)
