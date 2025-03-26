FROM python:3.11-slim AS python-base

# Python setup
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Create working directory
WORKDIR /app

# Copy only requirements first to leverage Docker cache
FROM python-base AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements /app/requirements
RUN pip install --no-cache-dir -r requirements/base.txt

# Test image
FROM builder AS test
RUN pip install --no-cache-dir -r requirements/test.txt
COPY . /app/
RUN chmod +x /app/run_tests.sh
CMD ["./run_tests.sh"]

# Development image
FROM builder AS dev
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*
    
RUN pip install --no-cache-dir -r requirements/dev.txt

COPY . /app/
CMD ["python", "-m", "src.main"]

# Production image
FROM python-base AS prod

# Install curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY . /app/

# Create non-root user
RUN adduser --disabled-password --gecos "" appuser && \
    chown -R appuser:appuser /app
USER appuser

CMD ["python", "-m", "src.main"]