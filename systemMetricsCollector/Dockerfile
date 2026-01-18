# Use uma imagem base oficial do Python
FROM python:3.11-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências especificadas em requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante dos arquivos da aplicação para o diretório de trabalho
COPY . .

# Crie diretório para saída de métricas
RUN mkdir -p /app/output

# Defina variáveis de ambiente padrão
ENV METRICS_OUTPUT_FILE=/app/output/metrics.json
ENV LOG_LEVEL=INFO

# Defina o comando padrão para executar o aplicativo
CMD ["python", "main.py"]
