# Plano: Sistema de Commits Automáticos GitHub

## 📋 Visão Geral

Sistema automatizado que realiza commits diários no GitHub de segunda a sábado, rodando em uma VM dentro de um container Docker.

### Objetivos
- Automatizar commits diários em repositórios GitHub
- Executar em ambiente containerizado e isolado
- Manter consistência de atividade no perfil GitHub
- Garantir segurança e confiabilidade

## 🏗️ Arquitetura do Sistema

```
┌─────────────────┐
│   Host System   │
│                 │
│  ┌───────────┐  │
│  │  Docker   │  │
│  │           │  │
│  │ ┌───────┐ │  │
│  │ │  VM   │ │  │
│  │ │       │ │  │
│  │ │ Git + │ │  │
│  │ │ Script│ │  │
│  │ └───────┘ │  │
│  └───────────┘  │
└─────────────────┘
```

## 📁 Estrutura do Projeto

```
gitgardener/
├── README.md
├── requirements.txt
├── entrypoint.py
├── Dockerfile
├── docker-compose.yml
├── scripts/
│   ├── __init__.py
│   ├── commit_bot.py
│   ├── git_config.py
│   ├── health_check.py
│   └── scheduler.py
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── git_manager.py
│   │   ├── commit_generator.py
│   │   └── config_manager.py
│   └── utils/
│       ├── __init__.py
│       ├── logger.py
│       └── ssh_helper.py
├── config/
│   ├── config.yaml
│   ├── crontab
│   └── config.template.yaml
├── tests/
│   ├── __init__.py
│   ├── test_git_manager.py
│   ├── test_commit_generator.py
│   ├── test_config_manager.py
│   └── integration/
│       ├── __init__.py
│       └── test_full_workflow.py
├── logs/
│   └── .gitkeep
└── secrets/
    ├── ssh-keys/
    │   ├── id_rsa
    │   └── id_rsa.pub
    └── config.yaml
```

## 🐳 Configuração Docker

### Dockerfile
```dockerfile
FROM python:3.11-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    git \
    cron \
    openssh-client \
    curl \
    vim \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Criar usuário para git
RUN useradd -m -s /bin/bash gitbot

# Definir diretório de trabalho
WORKDIR /home/gitbot

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar scripts Python
COPY scripts/ /home/gitbot/scripts/
COPY config/ /home/gitbot/config/

# Criar diretórios necessários
RUN mkdir -p /home/gitbot/logs /home/gitbot/repositories

# Configurar permissões
RUN chown -R gitbot:gitbot /home/gitbot/
RUN chmod +x /home/gitbot/scripts/*.py

# Mudar para usuário gitbot
USER gitbot

# Configurar cron
COPY config/crontab /tmp/crontab
RUN crontab /tmp/crontab

# Script de inicialização
COPY entrypoint.py /home/gitbot/entrypoint.py
RUN chmod +x /home/gitbot/entrypoint.py

CMD ["python3", "/home/gitbot/entrypoint.py"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  gitgardener:
    build: 
      context: .
      dockerfile: Dockerfile
    container_name: gitgardener-bot
    restart: unless-stopped
    volumes:
      - ./logs:/home/gitbot/logs
      - ./secrets:/home/gitbot/secrets:ro
      - ./repositories:/home/gitbot/repositories
      - ./config/config.yaml:/home/gitbot/config/config.yaml:ro
    environment:
      - TZ=America/Sao_Paulo
      - PYTHONPATH=/home/gitbot
    networks:
      - gitgardener-network
    healthcheck:
      test: ["CMD", "python3", "/home/gitbot/scripts/health_check.py"]
      interval: 30m
      timeout: 10s
      retries: 3
      start_period: 1m

networks:
  gitgardener-network:
    driver: bridge
```

## 🔧 Scripts Principais

### commit_bot.py
```python
#!/usr/bin/env python3

import os
import json
import subprocess
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import yaml


class CommitBot:
    def __init__(self, config_path: str = "/home/gitbot/config/config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        self.logger = self._setup_logging()
        
    def _load_config(self) -> Dict:
        """Carrega configuração do arquivo YAML"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise Exception(f"Erro ao carregar configuração: {e}")
            
    def _setup_logging(self) -> logging.Logger:
        """Configura sistema de logging"""
        log_dir = Path(self.config['logging']['log_dir'])
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"commit-{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s] %(levelname)s: %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
        
    def _is_weekday(self) -> bool:
        """Verifica se é dia de semana (segunda a sábado)"""
        day_of_week = datetime.now().weekday()
        return day_of_week < 6  # 0-6 = segunda a domingo
        
    def _setup_ssh_agent(self) -> None:
        """Configura SSH agent com as chaves"""
        try:
            ssh_key_path = Path(self.config['ssh']['private_key_path'])
            if not ssh_key_path.exists():
                raise FileNotFoundError(f"Chave SSH não encontrada: {ssh_key_path}")
                
            # Adicionar chave ao ssh-agent
            subprocess.run(['ssh-add', str(ssh_key_path)], check=True)
            self.logger.info("SSH agent configurado com sucesso")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Erro ao configurar SSH agent: {e}")
            raise
            
    def _clone_or_update_repo(self, repo_config: Dict) -> Path:
        """Clona ou atualiza um repositório"""
        repo_name = repo_config['name']
        repo_url = repo_config['url']
        repos_dir = Path(self.config['git']['repositories_dir'])
        repo_path = repos_dir / repo_name
        
        try:
            if not repo_path.exists():
                self.logger.info(f"Clonando repositório: {repo_name}")
                subprocess.run(
                    ['git', 'clone', repo_url, str(repo_path)], 
                    check=True
                )
            else:
                self.logger.info(f"Atualizando repositório: {repo_name}")
                subprocess.run(
                    ['git', '-C', str(repo_path), 'pull', 'origin', 'main'], 
                    check=True
                )
            return repo_path
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Erro ao processar repositório {repo_name}: {e}")
            raise
            
    def _create_commit_content(self, commit_type: str, repo_path: Path) -> Dict:
        """Cria conteúdo do commit baseado no tipo"""
        commit_generators = {
            'daily': self._create_daily_commit,
            'code': self._create_code_commit,
            'docs': self._create_docs_commit
        }
        
        generator = commit_generators.get(commit_type, self._create_daily_commit)
        return generator(repo_path)
        
    def _create_daily_commit(self, repo_path: Path) -> Dict:
        """Cria commit diário simples"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Criar ou atualizar arquivo de log diário
        daily_log = repo_path / "daily_activity.md"
        content = f"\n## {today}\n- Atividade automática diária\n- Sistema funcionando corretamente\n"
        
        with open(daily_log, 'a', encoding='utf-8') as f:
            f.write(content)
            
        return {
            'files': [str(daily_log)],
            'message': f"feat: atividade diária {today}"
        }
        
    def _create_code_commit(self, repo_path: Path) -> Dict:
        """Cria commit relacionado a código"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Criar arquivo de exemplo ou snippet
        code_dir = repo_path / "src" / "examples"
        code_dir.mkdir(parents=True, exist_ok=True)
        
        code_file = code_dir / f"example_{today.replace('-', '_')}.py"
        code_content = f'''#!/usr/bin/env python3
"""
Exemplo de código gerado automaticamente - {today}
"""

def hello_world():
    """Função de exemplo"""
    return "Hello, World! - {today}"

if __name__ == "__main__":
    print(hello_world())
'''
        
        with open(code_file, 'w', encoding='utf-8') as f:
            f.write(code_content)
            
        return {
            'files': [str(code_file)],
            'message': f"add: exemplo de código {today}"
        }
        
    def _create_docs_commit(self, repo_path: Path) -> Dict:
        """Cria commit relacionado à documentação"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        docs_dir = repo_path / "docs"
        docs_dir.mkdir(exist_ok=True)
        
        doc_file = docs_dir / f"notes_{today}.md"
        doc_content = f"""# Notas - {today}

## Atividades Realizadas
- Manutenção automática do repositório
- Verificação de integridade dos arquivos
- Atualização de documentação

## Status do Sistema
- ✅ Sistema funcionando corretamente
- ✅ Backups atualizados
- ✅ Logs monitorados

---
*Documento gerado automaticamente*
"""
        
        with open(doc_file, 'w', encoding='utf-8') as f:
            f.write(doc_content)
            
        return {
            'files': [str(doc_file)],
            'message': f"docs: atualização de documentação {today}"
        }
        
    def _commit_and_push(self, repo_path: Path, commit_data: Dict) -> None:
        """Realiza commit e push das alterações"""
        try:
            # Adicionar arquivos ao git
            for file_path in commit_data['files']:
                subprocess.run(['git', '-C', str(repo_path), 'add', file_path], check=True)
                
            # Realizar commit
            subprocess.run([
                'git', '-C', str(repo_path), 'commit', 
                '-m', commit_data['message']
            ], check=True)
            
            # Push para o repositório remoto
            subprocess.run(['git', '-C', str(repo_path), 'push', 'origin', 'main'], check=True)
            
            self.logger.info(f"Commit realizado: {commit_data['message']}")
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Erro ao realizar commit: {e}")
            raise
            
    def process_repositories(self) -> None:
        """Processa todos os repositórios configurados"""
        if not self._is_weekday():
            self.logger.info("Domingo - não executando commits")
            return
            
        try:
            self._setup_ssh_agent()
            
            for repo_config in self.config['repositories']:
                if not repo_config.get('enabled', True):
                    continue
                    
                repo_name = repo_config['name']
                commit_type = repo_config.get('commit_type', 'daily')
                
                self.logger.info(f"Processando repositório: {repo_name}")
                
                # Clonar/atualizar repositório
                repo_path = self._clone_or_update_repo(repo_config)
                
                # Criar conteúdo do commit
                commit_data = self._create_commit_content(commit_type, repo_path)
                
                # Realizar commit e push
                self._commit_and_push(repo_path, commit_data)
                
            self.logger.info("Execução concluída com sucesso")
            
        except Exception as e:
            self.logger.error(f"Erro durante execução: {e}")
            raise


def main():
    """Função principal"""
    try:
        bot = CommitBot()
        bot.process_repositories()
    except Exception as e:
        logging.error(f"Erro fatal: {e}")
        exit(1)


if __name__ == "__main__":
    main()
```

### git_config.py
```python
#!/usr/bin/env python3

import os
import subprocess
import logging
from pathlib import Path
from typing import Dict
import yaml


class GitConfigurator:
    def __init__(self, config_path: str = "/home/gitbot/config/config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        self.logger = self._setup_logging()
        
    def _load_config(self) -> Dict:
        """Carrega configuração do arquivo YAML"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise Exception(f"Erro ao carregar configuração: {e}")
            
    def _setup_logging(self) -> logging.Logger:
        """Configura sistema de logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s] %(levelname)s: %(message)s'
        )
        return logging.getLogger(__name__)
        
    def setup_git_global_config(self) -> None:
        """Configura Git globalmente"""
        try:
            git_config = self.config['git']
            
            # Configurar nome e email
            subprocess.run([
                'git', 'config', '--global', 'user.name', git_config['user_name']
            ], check=True)
            
            subprocess.run([
                'git', 'config', '--global', 'user.email', git_config['user_email']
            ], check=True)
            
            # Configurar branch padrão
            subprocess.run([
                'git', 'config', '--global', 'init.defaultBranch', 'main'
            ], check=True)
            
            self.logger.info("Configuração global do Git realizada com sucesso")
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Erro ao configurar Git: {e}")
            raise
            
    def setup_ssh_keys(self) -> None:
        """Configura permissões das chaves SSH"""
        try:
            ssh_config = self.config['ssh']
            private_key = Path(ssh_config['private_key_path'])
            public_key = Path(ssh_config['public_key_path'])
            
            if not private_key.exists():
                raise FileNotFoundError(f"Chave privada não encontrada: {private_key}")
                
            if not public_key.exists():
                raise FileNotFoundError(f"Chave pública não encontrada: {public_key}")
            
            # Configurar permissões corretas
            private_key.chmod(0o600)
            public_key.chmod(0o644)
            
            self.logger.info("Permissões das chaves SSH configuradas")
            
        except Exception as e:
            self.logger.error(f"Erro ao configurar SSH: {e}")
            raise
            
    def setup_known_hosts(self) -> None:
        """Adiciona GitHub aos known_hosts"""
        try:
            ssh_dir = Path.home() / ".ssh"
            ssh_dir.mkdir(mode=0o700, exist_ok=True)
            
            known_hosts = ssh_dir / "known_hosts"
            
            # Verificar se GitHub já está nos known_hosts
            if known_hosts.exists():
                with open(known_hosts, 'r') as f:
                    if 'github.com' in f.read():
                        self.logger.info("GitHub já está nos known_hosts")
                        return
            
            # Adicionar GitHub aos known_hosts
            subprocess.run([
                'ssh-keyscan', 'github.com'
            ], stdout=open(known_hosts, 'a'), check=True)
            
            self.logger.info("GitHub adicionado aos known_hosts")
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Erro ao configurar known_hosts: {e}")
            raise
            
    def verify_ssh_connection(self) -> bool:
        """Verifica conexão SSH com GitHub"""
        try:
            result = subprocess.run([
                'ssh', '-T', 'git@github.com'
            ], capture_output=True, text=True, timeout=10)
            
            if 'successfully authenticated' in result.stderr:
                self.logger.info("Conexão SSH com GitHub verificada com sucesso")
                return True
            else:
                self.logger.warning("Falha na verificação SSH com GitHub")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error("Timeout na verificação SSH")
            return False
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Erro na verificação SSH: {e}")
            return False
            
    def setup_all(self) -> None:
        """Executa toda a configuração"""
        try:
            self.logger.info("Iniciando configuração do Git e SSH")
            
            self.setup_git_global_config()
            self.setup_ssh_keys()
            self.setup_known_hosts()
            
            if self.verify_ssh_connection():
                self.logger.info("Configuração concluída com sucesso")
            else:
                self.logger.warning("Configuração concluída, mas verificação SSH falhou")
                
        except Exception as e:
            self.logger.error(f"Erro na configuração: {e}")
            raise


def main():
    """Função principal"""
    try:
        configurator = GitConfigurator()
        configurator.setup_all()
    except Exception as e:
        logging.error(f"Erro fatal: {e}")
        exit(1)


if __name__ == "__main__":
    main()
```

## ⚙️ Arquivos de Configuração

### config.yaml
```yaml
# Configuração principal do GitGardener

# Configurações Git
git:
  user_name: "Seu Nome"
  user_email: "seu.email@example.com"
  repositories_dir: "/home/gitbot/repositories"

# Configurações SSH
ssh:
  private_key_path: "/home/gitbot/secrets/ssh-keys/id_rsa"
  public_key_path: "/home/gitbot/secrets/ssh-keys/id_rsa.pub"

# Configurações de Logging
logging:
  log_dir: "/home/gitbot/logs"
  level: "INFO"
  format: "[%(asctime)s] %(levelname)s: %(message)s"
  max_log_age_days: 30

# Configurações do Scheduler
scheduler:
  enabled: true
  weekdays_only: true  # Segunda a sábado
  run_time: "09:00"    # Horário de execução
  health_check_time: "08:00"

# Repositórios a serem gerenciados
repositories:
  - name: "daily-commits"
    url: "git@github.com:username/daily-commits.git"
    commit_type: "daily"
    enabled: true
    branch: "main"
    
  - name: "code-practice"
    url: "git@github.com:username/code-practice.git"
    commit_type: "code"
    enabled: true
    branch: "main"
    
  - name: "documentation"
    url: "git@github.com:username/documentation.git"
    commit_type: "docs"
    enabled: true
    branch: "main"

# Configurações dos tipos de commit
commit_types:
  daily:
    message_template: "feat: atividade diária {date}"
    file_pattern: "daily_activity.md"
    content_template: |
      
      ## {date}
      - Atividade automática diária
      - Sistema funcionando corretamente
      
  code:
    message_template: "add: exemplo de código {date}"
    file_pattern: "src/examples/example_{date_underscore}.py"
    content_template: |
      #!/usr/bin/env python3
      """
      Exemplo de código gerado automaticamente - {date}
      """
      
      def hello_world():
          """Função de exemplo"""
          return "Hello, World! - {date}"
      
      if __name__ == "__main__":
          print(hello_world())
          
  docs:
    message_template: "docs: atualização de documentação {date}"
    file_pattern: "docs/notes_{date}.md"
    content_template: |
      # Notas - {date}
      
      ## Atividades Realizadas
      - Manutenção automática do repositório
      - Verificação de integridade dos arquivos
      - Atualização de documentação
      
      ## Status do Sistema
      - ✅ Sistema funcionando corretamente
      - ✅ Backups atualizados
      - ✅ Logs monitorados
      
      ---
      *Documento gerado automaticamente*

# Configurações de Monitoramento
monitoring:
  disk_usage_threshold: 80    # Percentual
  memory_usage_threshold: 80  # Percentual
  log_cleanup_days: 30
  health_check_enabled: true

# Configurações de Segurança
security:
  ssh_timeout: 10  # segundos
  git_timeout: 30  # segundos
  max_retries: 3

# Configurações do Container
container:
  timezone: "America/Sao_Paulo"
  user: "gitbot"
  home_dir: "/home/gitbot"
```

### crontab
```
# Commit automático de segunda a sábado às 9h
0 9 * * 1-6 cd /home/gitbot && /usr/bin/python3 /home/gitbot/scripts/commit_bot.py

# Health check diário às 8h
0 8 * * * cd /home/gitbot && /usr/bin/python3 /home/gitbot/scripts/health_check.py

# Configuração inicial do Git (executar uma vez)
@reboot cd /home/gitbot && /usr/bin/python3 /home/gitbot/scripts/git_config.py
```

### requirements.txt
```
PyYAML==6.0.1
psutil==5.9.5
GitPython==3.1.37
schedule==1.2.0
requests==2.31.0
python-dotenv==1.0.0
```

## 🔒 Segurança

### Configuração de SSH
1. Gerar chave SSH dedicada:
```bash
ssh-keygen -t rsa -b 4096 -f ./secrets/ssh-keys/id_rsa -N ""
```

2. Adicionar chave pública ao GitHub:
   - Copiar conteúdo de `id_rsa.pub`
   - Adicionar em GitHub → Settings → SSH Keys

### Variáveis Sensíveis
- Armazenar credenciais em arquivos separados
- Usar volumes read-only para secrets
- Não versionar arquivos de secrets

## 🚀 Deploy e Execução

### Instalação
```bash
# 1. Clonar o projeto
git clone <repository-url>
cd gitgardener

# 2. Configurar arquivo de configuração
cp config/config.template.yaml config/config.yaml
# Editar config/config.yaml com suas informações

# 3. Gerar chaves SSH
ssh-keygen -t rsa -b 4096 -f ./secrets/ssh-keys/id_rsa -N ""

# 4. Copiar configuração para secrets
cp config/config.yaml secrets/config.yaml
# Editar secrets/config.yaml com suas credenciais

# 5. Construir e executar
docker-compose up -d --build
```

### Comandos Úteis
```bash
# Ver logs do container
docker-compose logs -f

# Executar comando no container
docker-compose exec github-bot bash

# Parar o serviço
docker-compose down

# Reiniciar
docker-compose restart
```

## 📊 Monitoramento

### health_check.py
```python
#!/usr/bin/env python3

import os
import subprocess
import logging
import psutil
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
import yaml


class HealthChecker:
    def __init__(self, config_path: str = "/home/gitbot/config/config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        self.logger = self._setup_logging()
        
    def _load_config(self) -> Dict:
        """Carrega configuração do arquivo YAML"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise Exception(f"Erro ao carregar configuração: {e}")
            
    def _setup_logging(self) -> logging.Logger:
        """Configura sistema de logging"""
        log_dir = Path(self.config['logging']['log_dir'])
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"health-{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s] %(levelname)s: %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
        
    def check_cron_service(self) -> bool:
        """Verifica se o serviço cron está executando"""
        try:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] == 'cron':
                    self.logger.info("Serviço cron está executando")
                    return True
            
            self.logger.error("ERRO: Cron não está executando")
            return False
            
        except Exception as e:
            self.logger.error(f"Erro ao verificar cron: {e}")
            return False
            
    def check_ssh_connectivity(self) -> bool:
        """Verifica conectividade SSH com GitHub"""
        try:
            result = subprocess.run([
                'ssh', '-T', 'git@github.com'
            ], capture_output=True, text=True, timeout=10)
            
            if 'successfully authenticated' in result.stderr:
                self.logger.info("Conectividade SSH com GitHub OK")
                return True
            else:
                self.logger.error("ERRO: Falha na autenticação SSH com GitHub")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error("ERRO: Timeout na conexão SSH com GitHub")
            return False
        except Exception as e:
            self.logger.error(f"ERRO: Falha na verificação SSH: {e}")
            return False
            
    def check_disk_usage(self, threshold: int = 80) -> Tuple[bool, int]:
        """Verifica uso do disco"""
        try:
            usage = shutil.disk_usage('/home/gitbot')
            used_percent = int((usage.used / usage.total) * 100)
            
            if used_percent > threshold:
                self.logger.warning(f"AVISO: Uso de disco acima de {threshold}% ({used_percent}%)")
                return False, used_percent
            else:
                self.logger.info(f"Uso de disco OK ({used_percent}%)")
                return True, used_percent
                
        except Exception as e:
            self.logger.error(f"Erro ao verificar uso do disco: {e}")
            return False, 0
            
    def check_memory_usage(self, threshold: int = 80) -> Tuple[bool, int]:
        """Verifica uso de memória"""
        try:
            memory = psutil.virtual_memory()
            used_percent = int(memory.percent)
            
            if used_percent > threshold:
                self.logger.warning(f"AVISO: Uso de memória acima de {threshold}% ({used_percent}%)")
                return False, used_percent
            else:
                self.logger.info(f"Uso de memória OK ({used_percent}%)")
                return True, used_percent
                
        except Exception as e:
            self.logger.error(f"Erro ao verificar uso da memória: {e}")
            return False, 0
            
    def check_log_files(self) -> bool:
        """Verifica integridade dos arquivos de log"""
        try:
            log_dir = Path(self.config['logging']['log_dir'])
            
            if not log_dir.exists():
                self.logger.error("ERRO: Diretório de logs não existe")
                return False
                
            # Contar arquivos de log
            log_files = list(log_dir.glob('*.log'))
            self.logger.info(f"Encontrados {len(log_files)} arquivos de log")
            
            # Verificar se há logs muito antigos (mais de 30 dias)
            old_logs = []
            now = datetime.now()
            
            for log_file in log_files:
                file_age = now - datetime.fromtimestamp(log_file.stat().st_mtime)
                if file_age.days > 30:
                    old_logs.append(log_file)
                    
            if old_logs:
                self.logger.info(f"Encontrados {len(old_logs)} arquivos de log antigos para limpeza")
                
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao verificar arquivos de log: {e}")
            return False
            
    def check_git_repositories(self) -> bool:
        """Verifica status dos repositórios Git"""
        try:
            repos_dir = Path(self.config['git']['repositories_dir'])
            
            if not repos_dir.exists():
                self.logger.warning("Diretório de repositórios não existe ainda")
                return True
                
            repo_count = 0
            for repo_path in repos_dir.iterdir():
                if repo_path.is_dir() and (repo_path / '.git').exists():
                    repo_count += 1
                    
                    # Verificar status do repositório
                    try:
                        result = subprocess.run([
                            'git', '-C', str(repo_path), 'status', '--porcelain'
                        ], capture_output=True, text=True, check=True)
                        
                        # Se há mudanças não commitadas, não é necessariamente um erro
                        if result.stdout.strip():
                            self.logger.info(f"Repositório {repo_path.name} tem mudanças não commitadas")
                            
                    except subprocess.CalledProcessError as e:
                        self.logger.error(f"Erro ao verificar repositório {repo_path.name}: {e}")
                        return False
                        
            self.logger.info(f"Verificados {repo_count} repositórios Git")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao verificar repositórios: {e}")
            return False
            
    def cleanup_old_logs(self, days: int = 30) -> None:
        """Remove logs antigos"""
        try:
            log_dir = Path(self.config['logging']['log_dir'])
            now = datetime.now()
            removed_count = 0
            
            for log_file in log_dir.glob('*.log'):
                file_age = now - datetime.fromtimestamp(log_file.stat().st_mtime)
                if file_age.days > days:
                    log_file.unlink()
                    removed_count += 1
                    
            if removed_count > 0:
                self.logger.info(f"Removidos {removed_count} arquivos de log antigos")
            else:
                self.logger.info("Nenhum arquivo de log antigo encontrado")
                
        except Exception as e:
            self.logger.error(f"Erro ao limpar logs antigos: {e}")
            
    def run_health_check(self) -> bool:
        """Executa verificação completa de saúde"""
        self.logger.info("Iniciando health check completo")
        
        checks = [
            ("Serviço Cron", self.check_cron_service()),
            ("Conectividade SSH", self.check_ssh_connectivity()),
            ("Uso do Disco", self.check_disk_usage()[0]),
            ("Uso da Memória", self.check_memory_usage()[0]),
            ("Arquivos de Log", self.check_log_files()),
            ("Repositórios Git", self.check_git_repositories())
        ]
        
        failed_checks = [name for name, result in checks if not result]
        
        if failed_checks:
            self.logger.error(f"Health check FALHOU. Problemas encontrados em: {', '.join(failed_checks)}")
            return False
        else:
            self.logger.info("Health check OK - Todos os sistemas funcionando")
            
            # Executar limpeza de logs antigos
            self.cleanup_old_logs()
            
            return True


def main():
    """Função principal"""
    try:
        checker = HealthChecker()
        success = checker.run_health_check()
        exit(0 if success else 1)
    except Exception as e:
        logging.error(f"Erro fatal no health check: {e}")
        exit(1)


if __name__ == "__main__":
    main()
```

### Logs
- **Commit logs**: `/logs/commit-YYYYMMDD.log`
- **Health logs**: `/logs/health-YYYYMMDD.log`
- **Error logs**: `/logs/error-YYYYMMDD.log`

## 🐛 Troubleshooting

### Problemas Comuns

1. **Falha na autenticação SSH**
   - Verificar se a chave pública foi adicionada ao GitHub
   - Confirmar permissões dos arquivos SSH (600 para privada, 644 para pública)

2. **Cron não executa**
   - Verificar se o serviço cron está rodando: `pgrep cron`
   - Validar sintaxe do crontab: `crontab -l`

3. **Git push falha**
   - Verificar conectividade: `ssh -T git@github.com`
   - Confirmar configuração do repositório remoto

4. **Container não inicia**
   - Verificar logs: `docker-compose logs`
   - Validar volumes e permissões

### Comandos de Debug
```bash
# Testar execução manual
docker-compose exec gitgardener python3 /home/gitbot/scripts/commit_bot.py

# Verificar cron jobs
docker-compose exec gitgardener crontab -l

# Testar conectividade SSH
docker-compose exec gitgardener ssh -T git@github.com

# Ver logs em tempo real
docker-compose exec gitgardener tail -f /home/gitbot/logs/commit-$(date +%Y%m%d).log

# Executar health check manual
docker-compose exec gitgardener python3 /home/gitbot/scripts/health_check.py

# Executar configuração inicial
docker-compose exec gitgardener python3 /home/gitbot/scripts/git_config.py
```

## 📈 Melhorias Futuras

### Funcionalidades Python Avançadas

1. **Interface Web com Flask/FastAPI**
   ```python
   # Dashboard para monitoramento e configuração
   - Visualização de estatísticas de commits
   - Configuração dinâmica de repositórios
   - Logs em tempo real via WebSocket
   - API REST para integração
   ```

2. **Sistema de Plugins**
   ```python
   # Arquitetura de plugins para tipos de commit
   - Plugin para commits de código
   - Plugin para documentação
   - Plugin para projetos específicos
   - Plugin para integração com outras ferramentas
   ```

3. **Machine Learning para Commits Inteligentes**
   ```python
   # Análise de padrões para commits mais naturais
   - Análise de histórico de commits existente
   - Geração de mensagens baseada em contexto
   - Timing inteligente baseado em atividade
   - Detecção de padrões de desenvolvimento
   ```

4. **Integração com APIs**
   ```python
   # Integração com serviços externos
   - GitHub API para estatísticas
   - Slack/Discord para notificações
   - Jira/Trello para tracking de tasks
   - Google Calendar para agendamento dinâmico
   ```

5. **Sistema de Backup e Restauração**
   ```python
   # Backup automático das configurações
   - Backup incremental de repositórios
   - Sincronização com cloud storage
   - Restauração de configurações
   - Versionamento de settings
   ```

6. **Analytics e Reporting**
   ```python
   # Análise detalhada de atividade
   - Relatórios de produtividade
   - Gráficos de atividade
   - Métricas de qualidade de commits
   - Exportação de dados para análise
   ```

### Arquitetura Escalável

1. **Microserviços**
   - Separar em serviços independentes
   - Message queue para comunicação
   - Load balancing para múltiplas instâncias

2. **Base de Dados**
   - PostgreSQL para persistência
   - Redis para cache e filas
   - Histórico detalhado de operações

3. **Containerização Avançada**
   - Kubernetes para orquestração
   - Health checks automatizados
   - Auto-scaling baseado em carga

4. **CI/CD Pipeline**
   - Testes automatizados
   - Deploy automatizado
   - Rollback automático em falhas

## 🧪 Testes

### Estrutura de Testes
```python
# tests/test_git_manager.py
import pytest
from unittest.mock import Mock, patch
from src.core.git_manager import GitManager
from src.config.settings import Settings

class TestGitManager:
    def test_setup_git_config(self):
        settings = Mock(spec=Settings)
        manager = GitManager(settings)
        # Implementar testes
        
    def test_clone_or_update_repo(self):
        # Testar clonagem e atualização
        pass
        
    def test_create_commit(self):
        # Testar criação de commits
        pass

# tests/test_commit_generator.py
import pytest
from pathlib import Path
from src.core.commit_generator import CommitGenerator

class TestCommitGenerator:
    def test_generate_daily_commit(self):
        generator = CommitGenerator()
        test_path = Path("/tmp/test")
        result = generator.generate_daily_commit(test_path, "daily")
        assert "message" in result
        assert "files" in result
```

### Comandos de Teste
```bash
# Executar todos os testes
docker-compose exec github-bot python -m pytest tests/ -v

# Executar testes com cobertura
docker-compose exec github-bot python -m pytest tests/ --cov=src

# Executar testes específicos
docker-compose exec github-bot python -m pytest tests/test_git_manager.py::TestGitManager::test_setup_git_config

# Testes de integração
docker-compose exec github-bot python -m pytest tests/integration/ -v
```

## 📋 Checklist de Implementação

### Fase 1: Configuração Básica
- [ ] Estruturar diretórios do projeto Python
- [ ] Criar requirements.txt com dependências
- [ ] Implementar classes de configuração (Settings, Logger)
- [ ] Criar Dockerfile e docker-compose para Python
- [ ] Implementar health check básico

### Fase 2: Core Functionality  
- [ ] Implementar GitManager para operações Git
- [ ] Criar CommitGenerator com diferentes tipos
- [ ] Implementar Scheduler para automação
- [ ] Configurar sistema de logging robusto
- [ ] Criar script principal (main.py)

### Fase 3: Configuração e Deploy
- [ ] Gerar e configurar chaves SSH
- [ ] Criar arquivos de configuração YAML
- [ ] Configurar repositórios alvo
- [ ] Implementar entrypoint script
- [ ] Configurar cron jobs

### Fase 4: Testes e Validação
- [ ] Implementar testes unitários
- [ ] Criar testes de integração
- [ ] Testar execução manual
- [ ] Validar health checks
- [ ] Realizar testes completos

### Fase 5: Monitoramento e Produção
- [ ] Configurar logging para produção
- [ ] Implementar monitoramento
- [ ] Documentar troubleshooting
- [ ] Deploy em produção
- [ ] Monitorar primeiras execuções

### Fase 6: Melhorias (Opcional)
- [ ] Implementar dashboard web
- [ ] Adicionar notificações
- [ ] Criar sistema de plugins
- [ ] Implementar analytics
- [ ] Adicionar backup automático

---

**Nota**: Este sistema desenvolvido em Python oferece maior flexibilidade, manutenibilidade e possibilidades de extensão comparado à versão em bash. Use responsavelmente e em conformidade com os termos de serviço do GitHub.
