# ----- Stage 1: builder -----
FROM python:3.12-slim AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /build
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

# ----- Stage 2: runtime -----
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/install/bin:$PATH" \
    PYTHONPATH="/install/lib/python3.12/site-packages"

# Non-root user
RUN groupadd --system app && useradd --system --gid app --create-home --shell /sbin/nologin app

# Bring installed packages from builder
COPY --from=builder /install /install

WORKDIR /app
COPY --chown=app:app . .

USER app

EXPOSE 5000

# gunicorn is provided by requirements.txt
CMD ["sh", "-c", "gunicorn -w ${GUNICORN_WORKERS:-2} -b 0.0.0.0:5000 app:app"]
