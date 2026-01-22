FROM python:3.13-slim

WORKDIR /app

# Install uv for faster dependency management
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv pip install --system -r pyproject.toml

# Copy application code
COPY . .

# Create directory for database if it doesn't exist
RUN mkdir -p /app/data

# Expose atypical port
EXPOSE 7373

# Run the application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=7373"]
