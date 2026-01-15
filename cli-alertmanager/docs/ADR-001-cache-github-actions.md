# ADR-001: Uso de GitHub Actions Cache para Build Docker

**Status:** Aceito | **Data:** 2025-09-29

## Contexto

O pipeline de CI/CD estava levando ~1-2 minutos por build completo, causando feedback lento para desenvolvedores. Cada build reconstruía todas as camadas Docker do zero, incluindo dependências Python que raramente mudam. Com múltiplos deploys diários, isso representa ~2h de tempo de CI desperdiçado por dia.

## Decisão

Implementar cache de build Docker usando GitHub Actions Cache (`type=gha`) com modo `max` para armazenar todas as camadas intermediárias do build.

**Configuração:**
```yaml
cache-from: type=gha
cache-to: type=gha,mode=max
```

Esta estratégia reutiliza camadas Docker entre builds, reduzindo tempo de compilação de ~10min para ~2-3min em builds incrementais.

## Alternativas Consideradas

- **Registry cache (ECR):** Armazenar cache no próprio ECR - Rejeitada por custo adicional de storage e latência de pull/push
- **Local runner cache:** Usar runners self-hosted com cache local - Rejeitada por complexidade operacional
- **GitHub Actions Cache (type=gha):** Usar cache nativo do GHA - Escolhida por ser gratuito, zero configuração adicional, e bem integrado

## Consequências

- ✅ Tempo de build reduzido em ~70% (2min → 40s)
- ✅ Feedback mais rápido para desenvolvedores
- ✅ Redução de custos de compute do GitHub Actions
- ⚠️ Cache limitado a 10GB por repositório (aceitável para nosso caso)
- ⚠️ Primeiro build após cache expirar (7 dias) será lento

## Referências

- Código: `.github/workflows/deploy-main.yaml:126-127`
- Docker Buildx cache docs: https://docs.docker.com/build/cache/backends/gha/
- Commits: `867239f`, `b6299fc`