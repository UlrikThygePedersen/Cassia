# Python version
FROM python:3.10-slim

# Install curl to get rye and setup container
RUN apt-get update && apt-get install -y curl libssl-dev

# Install Rye
RUN curl -sSf https://install.rye-up.com | bash
ENV PATH="/root/.rye/bin:$PATH"

# Workdic to api for FastAPI
WORKDIR /api

# Copy files into dir
COPY . .

# Install pyproject.toml with rye
RUN rye sync

# Port expose
EXPOSE 8000

# Docker run
CMD ["rye", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
