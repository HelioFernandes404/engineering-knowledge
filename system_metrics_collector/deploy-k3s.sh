#!/bin/bash

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

IMAGE_NAME="infragen"
IMAGE_TAG="latest"
IMAGE_FULL="${IMAGE_NAME}:${IMAGE_TAG}"
TAR_FILE="/tmp/${IMAGE_NAME}.tar"
MANIFEST="kubernetes/system_metrics_collector/system_metrics_collector.yaml"

echo -e "${YELLOW}🚀 Deploy InfranGen para K3s${NC}"
echo "======================================"

# 1. Build da imagem Docker
echo -e "\n${YELLOW}📦 Building Docker image...${NC}"
docker build -t ${IMAGE_FULL} .

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Build concluído com sucesso${NC}"
else
    echo -e "${RED}❌ Erro no build da imagem${NC}"
    exit 1
fi

# 2. Salvar imagem para tar
echo -e "\n${YELLOW}💾 Salvando imagem Docker para tar...${NC}"
docker save ${IMAGE_FULL} -o ${TAR_FILE}

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Imagem salva em ${TAR_FILE}${NC}"
else
    echo -e "${RED}❌ Erro ao salvar imagem${NC}"
    exit 1
fi

# 3. Importar para K3s
echo -e "\n${YELLOW}📥 Importando imagem para K3s...${NC}"
sudo k3s ctr images import ${TAR_FILE}

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Imagem importada com sucesso${NC}"
else
    echo -e "${RED}❌ Erro ao importar imagem para K3s${NC}"
    exit 1
fi

# 4. Limpar arquivo tar
echo -e "\n${YELLOW}🧹 Limpando arquivo temporário...${NC}"
rm -f ${TAR_FILE}

# 5. Verificar se imagem existe no K3s
echo -e "\n${YELLOW}🔍 Verificando imagem no K3s...${NC}"
if sudo k3s ctr images ls | grep -q ${IMAGE_NAME}; then
    echo -e "${GREEN}✅ Imagem encontrada no K3s:${NC}"
    sudo k3s ctr images ls | grep ${IMAGE_NAME}
else
    echo -e "${RED}❌ Imagem não encontrada no K3s${NC}"
    exit 1
fi

# 6. Aplicar manifesto Kubernetes
echo -e "\n${YELLOW}☸️  Aplicando manifesto Kubernetes...${NC}"
kubectl apply -f ${MANIFEST}

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Manifesto aplicado com sucesso${NC}"
else
    echo -e "${RED}❌ Erro ao aplicar manifesto${NC}"
    exit 1
fi

# 7. Aguardar pods ficarem ready
echo -e "\n${YELLOW}⏳ Aguardando pods ficarem prontos...${NC}"
kubectl wait --for=condition=ready pod -l app=system-metrics-collector -n monitoring --timeout=60s

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Pods prontos!${NC}"
else
    echo -e "${YELLOW}⚠️  Timeout aguardando pods. Verifique manualmente.${NC}"
fi

# 8. Mostrar status
echo -e "\n${GREEN}======================================"
echo "✅ Deploy concluído!"
echo -e "======================================${NC}\n"

echo "📊 Status dos recursos:"
echo ""
kubectl get pods -n monitoring -l app=system-metrics-collector
echo ""
kubectl get svc -n monitoring -l app=system-metrics-collector

echo -e "\n${YELLOW}💡 Comandos úteis:${NC}"
echo "  # Ver logs:"
echo "  kubectl logs -f -n monitoring -l app=system-metrics-collector"
echo ""
echo "  # Testar métricas localmente:"
echo "  kubectl port-forward -n monitoring svc/system-metrics-collector 8000:8000"
echo "  curl http://localhost:8000/metrics"
echo ""
echo "  # Deletar deployment:"
echo "  kubectl delete -f ${MANIFEST}"
