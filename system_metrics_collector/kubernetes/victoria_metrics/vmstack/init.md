
1. Adicione o repositório Helm do Victoria Metrics:
```shell
# Stack básico
helm install vmstack vm/victoria-metrics-k8s-stack \
  -n monitoring \
  --create-namespace
```

2. Para uma instalação personalizada, crie um arquivo `vmstack-values.yaml` com as configurações desejadas e execute:
```shell
  helm install vmstack vm/victoria-metrics-k8s-stack \
  -n monitoring \
  --create-namespace \
  -f vmstack-values.yaml
```