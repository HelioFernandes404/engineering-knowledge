# K9s Multi-Context Manager

Gerenciador de múltiplos clusters Kubernetes com túneis SSH seguros.

---

## 🚀 Quick Start

```bash
# 1. Setup inicial (primeira vez)
./init.sh

# 2. (Opcional) Customizar config
# Editor: ~/.k9s-config/config.yaml
# Docs: docs/CONFIG.md

# 3. Adicionar cluster
source venv/bin/activate
python3 fetch_k3s_config.py

# 4. Abrir k9s
./k9s-with-tunnel.sh
```

---

## ⚙️ Configuration

### Default Config (Auto-created by `init.sh`)

**Location:** `~/.k9s-config/config.yaml`

**Default values:**
```yaml
remote_k3s_config_path: /etc/rancher/k3s/k3s.yaml
ssh_key_path: ~/.ssh/id_ed25519
k3s_api_port: 6443
port_range_start: 16443
port_range_size: 10000
```

### Environment Variable Overrides

```bash
# Use custom K3s port for specific cluster
export K3S_API_PORT=7443
python3 fetch_k3s_config.py

# Use larger port range for many clusters
export PORT_RANGE_START=10000
export PORT_RANGE_SIZE=50000
python3 fetch_k3s_config.py

# Enable file logging
export K9S_LOG_FILE=~/.local/state/k9s/k9s-config.log
python3 fetch_k3s_config.py
```

**Full documentation:** See [docs/CONFIG.md](docs/CONFIG.md)

---

## 📖 Guia Completo

### 1️⃣ Primeira Vez: Setup

```bash
# Clonar (se ainda não tiver)
git clone https://github.com/HelioFernandes404/k9s-config.git
cd k9s-config

# Rodar setup automático
./init.sh
```

Isso cria o ambiente virtual e instala dependências.

### 2️⃣ Adicionar Novo Cluster

```bash
# Ativar ambiente
source venv/bin/activate

# Executar script
python3 fetch_k3s_config.py
```

**O script pergunta:**
1. Qual empresa? (lista do `inventory/`)
2. Qual host? (mostra `[VPN]` se necessário)

**O script faz:**
- ✅ Conecta via SSH
- ✅ Busca kubeconfig do K3s
- ✅ Cria túnel SSH seguro
- ✅ Adiciona contexto no `~/.kube/config`

**Saída esperada:**
```
✓ Context 'empresa-host' added to ~/.kube/config
✓ Set as current context
✓ SSH tunnel created (PID: 123456)

You can now use kubectl/k9s directly!
  kubectl get nodes
  k9s -l debug
```

### 3️⃣ Abrir K9s

```bash
./k9s-with-tunnel.sh
```

Isso verifica se o túnel está ativo e abre k9s em modo debug.

**Logs:** `tail -f ~/.local/state/k9s/k9s.log`

---

## 🔄 Trocar de Cluster

### Opção 1: Reconfigurar tudo

```bash
source venv/bin/activate
python3 fetch_k3s_config.py
# → Escolher nova empresa/host
./k9s-with-tunnel.sh
```

### Opção 2: Usar contexto existente

```bash
# Listar contextos
kubectl config get-contexts

# Trocar
kubectl config use-context empresa-host

# Abrir k9s
./k9s-with-tunnel.sh
```

---

## 🛠️ Comandos Úteis

### Gerenciar Túneis

```bash
# Ver túneis ativos
./k9s-with-tunnel.sh list

# Matar túnel específico
./k9s-with-tunnel.sh kill empresa-host

# Matar todos
./k9s-with-tunnel.sh kill-all
```

### Gerenciar Contextos

```bash
# Ver contextos
kubectl config get-contexts

# Ver contexto atual
kubectl config current-context

# Trocar contexto
kubectl config use-context empresa-host

# Deletar contexto
kubectl config delete-context empresa-host
```

---

## 📁 Estrutura

```
k9s-config/
├── fetch_k3s_config.py      # Script principal
├── k9s-with-tunnel.sh        # Helper k9s + túneis
├── init.sh                   # Setup venv
├── inventory/                # Inventários (Ansible-style)
│   ├── empresa_hosts.yml
│   └── ...
├── venv/                     # Ambiente Python
└── README.md                 # Este arquivo
```

---

## 🏢 Adicionar Nova Empresa

### Criar inventário: `inventory/empresa_hosts.yml`

```yaml
all:
  vars:
    customer: empresa
    ansible_user: ubuntu

  children:
    k3s_cluster:
      vars:
        # argocd_use_socks5_proxy: true  # Se precisar VPN
      hosts:
        meu-servidor:
          ansible_host: 192.168.1.100
```

### Configurar SSH: `~/.ssh/config`

```
Host meu-servidor
  HostName 192.168.1.100
  User ubuntu
  IdentityFile ~/.ssh/chave
```

### Executar

```bash
source venv/bin/activate
python3 fetch_k3s_config.py
```

---

## 🔒 Segurança

- ✅ Túneis SSH (não expõe K3s na internet)
- ✅ Porta única por cluster
- ✅ Inventários não versionados (`.gitignore`)
- ✅ Backup automático de configs

---

## 🐛 Troubleshooting

### "No tunnel found"
```bash
# Ver túneis
./k9s-with-tunnel.sh list

# Recriar
source venv/bin/activate
python3 fetch_k3s_config.py
```

### "Connection refused"
```bash
# Verificar SSH
ssh <host> 'systemctl status k3s'

# Verificar túnel
./k9s-with-tunnel.sh list

# Recriar contexto
python3 fetch_k3s_config.py
```

### Limpar tudo
```bash
./k9s-with-tunnel.sh kill-all
kubectl config delete-context <nome>
python3 fetch_k3s_config.py
```

---

## 💡 Workflow Típico

```bash
# Dia 1: Setup
./init.sh
source venv/bin/activate
python3 fetch_k3s_config.py  # Adicionar cluster A

# Trabalhar no cluster A
./k9s-with-tunnel.sh

# Adicionar cluster B
python3 fetch_k3s_config.py

# Trabalhar no cluster B
./k9s-with-tunnel.sh

# Voltar para A
kubectl config use-context empresa-A
./k9s-with-tunnel.sh
```

---

## 📞 Onde Buscar Ajuda

- **Logs do fetch**: Saída do `python3 fetch_k3s_config.py`
- **Logs do k9s**: `tail -f ~/.local/state/k9s/k9s.log`
- **Túneis**: `ls ~/.local/state/k9s-tunnels/`
- **Kubeconfig**: `cat ~/.kube/config`

---

**Desenvolvido com ❤️ para gerenciar múltiplos clusters K3s de forma segura**
