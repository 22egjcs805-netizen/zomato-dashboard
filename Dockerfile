# ── Stage 1: Build ─────────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build

# Install dependencies into an isolated prefix so we can copy them cleanly
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ── Stage 2: Runtime ───────────────────────────────────────────────────────────
FROM python:3.11-slim

# Non-root user for security
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application source
COPY app/       ./app/
COPY requirements.txt .

# Ownership
RUN chown -R appuser:appuser /app
USER appuser

# Expose the port Gunicorn will listen on
EXPOSE 5000

# Health check (used by Kubernetes liveness probe)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

# Start with Gunicorn (production WSGI server, 2 workers)
CMD ["gunicorn", "--workers=2", "--bind=0.0.0.0:5000", "--timeout=60", "app.app:app"]
