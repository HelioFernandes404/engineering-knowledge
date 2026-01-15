# K9s Multi-Context Manager

## WHAT — Stack e Estrutura

**Stack**: Python 3 (venv), SSH (paramiko), YAML (PyYAML), Bash

**Propósito**: Gerenciar múltiplos clusters K3s via túneis SSH seguros

**Estrutura**:
```
fetch_k3s_config.py      # Script principal (SSH + kubeconfig merge)
k9s-with-tunnel.sh       # Helper para k9s + gerenciamento de túneis
init.sh                  # Setup venv + deps
inventory/               # Inventários Ansible-style (não versionados)
  └── empresa_hosts.yml  # Hosts por empresa
```

## WHY — Propósito

- Múltiplos clusters K3s em diferentes empresas/redes
- Acesso seguro via túneis SSH (sem expor API na internet)
- Detecção automática de VPN/sshuttle para redes privadas
- Contextos organizados no `~/.kube/config` padrão

## HOW — Workflow

### Setup (primeira vez)
```bash
./init.sh
```

### Adicionar cluster
```bash
source venv/bin/activate
python3 fetch_k3s_config.py
# Seleciona empresa → host → cria túnel + contexto
```

### Usar k9s
```bash
./k9s-with-tunnel.sh  # Verifica túnel e abre k9s -l debug
```

### Trocar cluster
```bash
kubectl config use-context empresa-host
./k9s-with-tunnel.sh
```

## Requisitos de Rede

Script detecta automaticamente:
- **IPs públicos**: Túnel SSH direto
- **IPs privados** (192.168.x.x, 10.x.x.x): Avisa sobre sshuttle
- **Inventários com VPN**: Flag `argocd_use_socks5_proxy: true`

Exemplo sshuttle:
```bash
sshuttle -v -r helio@100.64.5.10 192.168.90.0/24
```

## Segurança

- Túneis SSH (localhost:porta) em vez de IPs externos
- Inventários não versionados (`.gitignore`)
- Portas determinísticas por contexto (hash do nome)
- Backups automáticos de `~/.kube/config`

## Documentação

Ver `README.md` para guia completo e troubleshooting.
