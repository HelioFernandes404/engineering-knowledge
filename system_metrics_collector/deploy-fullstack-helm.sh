#!/bin/bash

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

IMAGE_NAME="infragen"
IMAGE_TAG="latest"
IMAGE_FULL="${IMAGE_NAME}:${IMAGE_TAG}"
TAR_FILE="/tmp/${IMAGE_NAME}.tar"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}🚀 Deploy Full Stack - Victoria Metrics (Helm) + InfranGen${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

# 1. Build da imagem Docker
echo -e "${YELLOW}📦 Step 1/6: Building Docker image...${NC}"
docker build -t ${IMAGE_FULL} .

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Build concluído com sucesso${NC}\n"
else
    echo -e "${RED}❌ Erro no build da imagem${NC}"
    exit 1
fi

# 2. Salvar imagem para tar
echo -e "${YELLOW}💾 Step 2/6: Salvando imagem Docker para tar...${NC}"
docker save ${IMAGE_FULL} -o ${TAR_FILE}

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Imagem salva em ${TAR_FILE}${NC}\n"
else
    echo -e "${RED}❌ Erro ao salvar imagem${NC}"
    exit 1
fi

# 3. Importar para K3s
echo -e "${YELLOW}📥 Step 3/6: Importando imagem para K3s...${NC}"
sudo k3s ctr images import ${TAR_FILE}

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Imagem importada com sucesso${NC}\n"
else
    echo -e "${RED}❌ Erro ao importar imagem para K3s${NC}"
    exit 1
fi

# 4. Limpar arquivo tar
rm -f ${TAR_FILE}

# 5. Adicionar repositório Helm do Victoria Metrics
echo -e "${YELLOW}📋 Step 4/6: Configurando Helm repository...${NC}"

# Verificar se o repo já existe
if helm repo list | grep -q "^vm"; then
    echo -e "${BLUE}  → Repositório VM já existe, atualizando...${NC}"
    helm repo update vm
else
    echo -e "${BLUE}  → Adicionando repositório VM...${NC}"
    helm repo add vm https://victoriametrics.github.io/helm-charts/
    helm repo update
fi

echo -e "${GREEN}✅ Repositório Helm configurado${NC}\n"

# 6. Criar namespace monitoring se não existir
echo -e "${YELLOW}🏗️  Step 5/6: Criando namespace monitoring...${NC}"
kubectl create namespace monitoring --dry-run=client -o yaml | kubectl apply -f -
echo -e "${GREEN}✅ Namespace pronto${NC}\n"

# 7. Instalar Victoria Metrics Stack via Helm
echo -e "${YELLOW}☸️  Step 6/6: Instalando Victoria Metrics Stack via Helm...${NC}"

helm upgrade --install vmstack vm/victoria-metrics-k8s-stack \
  -n monitoring \
  -f kubernetes/victoria_metrics/vmstack/vmstack-values.yaml \
  --wait \
  --timeout 5m

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Victoria Metrics Stack instalado com sucesso${NC}\n"
else
    echo -e "${RED}❌ Erro ao instalar Victoria Metrics Stack${NC}"
    exit 1
fi

# 8. Aplicar aplicação InfranGen
echo -e "${YELLOW}📦 Aplicando aplicação InfranGen...${NC}"
kubectl apply -f kubernetes/fullstack_application/system-metrics-collector.yaml

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Aplicação InfranGen instalada${NC}\n"
else
    echo -e "${RED}❌ Erro ao instalar aplicação${NC}"
    exit 1
fi

# 9. Aguardar pods ficarem prontos
echo -e "${YELLOW}⏳ Aguardando pods ficarem prontos...${NC}"
sleep 10

kubectl wait --for=condition=ready pod -l app=system-metrics-collector -n monitoring --timeout=120s 2>/dev/null || true
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=vmselect -n monitoring --timeout=120s 2>/dev/null || true

# 10. Mostrar status final
echo -e "\n${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Deploy Full Stack concluído!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

echo -e "${BLUE}📊 Status dos Recursos:${NC}\n"

echo -e "${YELLOW}Victoria Metrics Stack (Helm):${NC}"
helm list -n monitoring
echo ""

echo -e "${YELLOW}Pods (namespace: monitoring):${NC}"
kubectl get pods -n monitoring
echo ""

echo -e "${YELLOW}Services (namespace: monitoring):${NC}"
kubectl get svc -n monitoring
echo ""

echo -e "${YELLOW}VMServiceScrapes:${NC}"
kubectl get vmservicescrape -n monitoring
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}💡 Comandos Úteis:${NC}\n"

echo -e "${BLUE}# Ver logs do sistema de coleta:${NC}"
echo -e "  kubectl logs -f -n monitoring -l app=system-metrics-collector\n"

echo -e "${BLUE}# Ver logs do VMAgent:${NC}"
echo -e "  kubectl logs -f -n monitoring -l app.kubernetes.io/name=vmagent\n"

echo -e "${BLUE}# Acessar métricas da aplicação:${NC}"
echo -e "  kubectl port-forward -n monitoring svc/system-metrics-collector 8000:8000"
echo -e "  curl http://localhost:8000/metrics\n"

echo -e "${BLUE}# Acessar VMSelect (consulta de métricas):${NC}"
echo -e "  kubectl port-forward -n monitoring svc/vmselect-vmstack-victoria-metrics-k8s-stack 8481:8481"
echo -e "  curl 'http://localhost:8481/select/0/prometheus/api/v1/query?query=up'\n"

echo -e "${BLUE}# Acessar Grafana:${NC}"
echo -e "  kubectl port-forward -n monitoring svc/vmstack-grafana 3000:80"
echo -e "  http://localhost:3000 (user: admin, password: veja abaixo)\n"

echo -e "${BLUE}# Pegar senha do Grafana:${NC}"
echo -e "  kubectl get secret -n monitoring vmstack-grafana -o jsonpath='{.data.admin-password}' | base64 -d\n"

echo -e "${BLUE}# Remover toda a stack:${NC}"
echo -e "  make fullstack-clean\n"

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
