.PHONY: help venv docker-build deploy-k3s k3s-logs k3s-clean k3s-port-forward fullstack-deploy fullstack-logs fullstack-vmselect fullstack-vmui fullstack-grafana fullstack-clean

# Display available commands
help:
	@echo "Available commands:"
	@echo ""
	@echo "  make help         - Display this help message"
	@echo "  make venv         - Create Python virtual environment"
	@echo ""
	@echo "Docker & Kubernetes (Simple):"
	@echo "  make docker-build    - Build Docker image"
	@echo "  make deploy-k3s      - Deploy to K3s (build + import + apply)"
	@echo "  make k3s-logs        - Show K3s pod logs"
	@echo "  make k3s-port-forward- Port forward to access metrics"
	@echo "  make k3s-clean       - Remove K3s deployment"
	@echo ""
	@echo "Full Stack (Victoria Metrics via Helm + App):"
	@echo "  make fullstack-deploy   - Deploy complete VM stack via Helm"
	@echo "  make fullstack-logs     - Show all pods logs"
	@echo "  make fullstack-vmui     - Open VictoriaMetrics UI (VMUI)"
	@echo "  make fullstack-vmselect - Port forward to VMSelect (query metrics)"
	@echo "  make fullstack-grafana  - Port forward to Grafana dashboard"
	@echo "  make fullstack-clean    - Remove entire Helm stack"
	@echo ""
	@echo "After creating venv, activate it with:"
	@echo "  source .venv/bin/activate"
	@echo ""

# Setup venv
venv:
	python3 -m venv .venv
	@echo ""
	@echo "Virtual environment created successfully!"
	@echo "Activate it with: source .venv/bin/activate"

# Docker build
docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t infragen:latest .

# Deploy to K3s
deploy-k3s:
	@echo "🚀 Deploying to K3s..."
	./deploy-k3s.sh

# Show K3s logs
k3s-logs:
	@echo "📋 Showing pod logs..."
	kubectl logs -f -n monitoring -l app=system-metrics-collector

# Port forward to access metrics
k3s-port-forward:
	@echo "🌐 Port forwarding to localhost:8000..."
	@echo "Access metrics at: http://localhost:8000/metrics"
	kubectl port-forward -n monitoring svc/system-metrics-collector 8000:8000

# Clean K3s deployment
k3s-clean:
	@echo "🧹 Removing K3s deployment..."
	kubectl delete -f kubernetes/system_metrics_collector/system_metrics_collector.yaml

# Deploy full stack (Victoria Metrics via Helm + App)
fullstack-deploy:
	@echo "🚀 Deploying Full Stack via Helm..."
	./deploy-fullstack-helm.sh

# Show logs from all monitoring pods
fullstack-logs:
	@echo "📋 Monitoring namespace logs..."
	@echo ""
	@echo "=== System Metrics Collector ==="
	kubectl logs -n monitoring -l app=system-metrics-collector --tail=50
	@echo ""
	@echo "=== VMAgent ==="
	kubectl logs -n monitoring -l app.kubernetes.io/name=vmagent --tail=50

# Port forward to VictoriaMetrics UI (VMUI)
fullstack-vmui:
	@echo "🌐 Port forwarding to VictoriaMetrics UI on localhost:8481..."
	@echo ""
	@echo "Access VMUI at: http://localhost:8481/select/0/vmui"
	@echo ""
	@echo "You can also use the API:"
	@echo "  http://localhost:8481/select/0/prometheus/api/v1/query?query=up"
	@echo ""
	kubectl port-forward -n monitoring svc/vmselect-vmstack-victoria-metrics-k8s-stack 8481:8481

# Port forward to VMSelect to query metrics
fullstack-vmselect:
	@echo "🌐 Port forwarding to VMSelect on localhost:8481..."
	@echo "Query metrics at: http://localhost:8481/select/0/prometheus/api/v1/query?query=up"
	kubectl port-forward -n monitoring svc/vmselect-vmstack-victoria-metrics-k8s-stack 8481:8481

# Port forward to Grafana
fullstack-grafana:
	@echo "🌐 Port forwarding to Grafana on localhost:3000..."
	@echo "Access Grafana at: http://localhost:3000"
	@echo ""
	@echo "Get admin password with:"
	@echo "  kubectl get secret -n monitoring vmstack-grafana -o jsonpath='{.data.admin-password}' | base64 -d"
	@echo ""
	kubectl port-forward -n monitoring svc/vmstack-grafana 3000:80

# Clean entire full stack
fullstack-clean:
	@echo "🧹 Removing Full Stack..."
	@echo "Removing Helm release..."
	helm uninstall vmstack -n monitoring --ignore-not-found
	@echo "Removing application..."
	kubectl delete -f kubernetes/fullstack_application/system-metrics-collector.yaml --ignore-not-found=true
	@echo "Removing namespace..."
	kubectl delete namespace monitoring --ignore-not-found=true
	@echo "✅ Full stack removed!"
