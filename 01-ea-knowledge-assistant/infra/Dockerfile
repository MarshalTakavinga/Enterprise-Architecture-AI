FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app

COPY pyproject.toml ./
COPY src ./src
RUN pip install ".[ui,pgvector,llm]"

COPY app ./app
COPY data/corpus ./data/corpus

# Run as a non-root user (mirrors STD-CTR-012 in the corpus).
RUN useradd --uid 10001 --create-home eaka && mkdir -p /app/.index /app/logs && chown -R eaka /app
USER eaka

EXPOSE 8000 8501
CMD ["uvicorn", "eaka.api:app", "--host", "0.0.0.0", "--port", "8000"]
