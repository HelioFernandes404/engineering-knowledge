import os


# o pip é o instalador de pacotes do python
def comando(comando):
    os.system(command=comando)

# Instalar um pacote
comando("pip install requests")

# Listar pacotes instalados
comando("pip list")

# Gerar um arquivo de requisitos
comando("pip freeze > requirements.txt")


# 3. Conda: Ambiente e pacotes para ciencia de dados

# Criar um ambiente
comando("conda create --name myenv python=3.8")

# Ativar um ambiente
comando("conda activate myenv")

# Instalar um pacote
comando("conda install numpy")

# 4. uv: Gerenciador de pacotes em Rust

# Iniciar um novo projeto
comando("uv init my_project")

# Criar um ambiente uv e instalar pacotes
comando("uv add flask requests")

# Executar um script dentro do ambiente gerenciado
comando("uv run script.py")

# 5. Poetry: Gestão Moderna de Dependências e Empacotamento

# Iniciar um novo projeto
comando("poetry new my_project")

# Instalar as dependências do projeto
comando("poetry install requests")

# Executar um script
comando("poetry run python script.py")